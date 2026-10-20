// Recepción de solicitudes de presupuesto de paint.joma.es.
// Sin dependencias: Node 22 (http, fetch, FormData nativos).
//
// Flujo: valida → guarda en disco (DATA_DIR) → responde al navegador → envía el
// correo por Resend en segundo plano. Lo que no se pueda enviar se reintenta cada
// 5 minutos, así que una caída de Resend no pierde solicitudes.
//
// Variables de entorno:
//   RESEND_API_KEY   clave de Resend (sin ella se guarda pero no se envía)
//   MAIL_FROM        remitente verificado en Resend, p. ej. "JomaPaint web <paint@joma.es>"
//   MAIL_TO          destinatarios separados por coma (por defecto marimar@joma.es)
//   ALLOWED_ORIGINS  orígenes permitidos separados por coma (por defecto https://paint.joma.es)
//   DATA_DIR         carpeta de solicitudes (por defecto /data)
import http from 'node:http';
import { Readable, Transform } from 'node:stream';
import { createHash } from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

const PORT = Number(process.env.PORT || 3000);
const DATA_DIR = process.env.DATA_DIR || '/data';
const RESEND_API_KEY = process.env.RESEND_API_KEY || '';
const RESEND_URL = process.env.RESEND_URL || 'https://api.resend.com/emails'; // solo para pruebas
const MAIL_FROM = process.env.MAIL_FROM || 'JomaPaint web <paint@joma.es>';
const MAIL_TO = (process.env.MAIL_TO || 'marimar@joma.es').split(',').map((s) => s.trim()).filter(Boolean);
const ORIGINS = (process.env.ALLOWED_ORIGINS || 'https://paint.joma.es').split(',').map((s) => s.trim()).filter(Boolean);

const MAX_BODY = 12 * 1024 * 1024;      // cuerpo completo (multipart)
const MAX_FILES_BYTES = 10 * 1024 * 1024; // suma de adjuntos, igual que en la web
const MIN_FILL_MS = 3000;               // tiempo mínimo desde que se abrió la página
const RATE_MAX = 5, RATE_WINDOW = 10 * 60 * 1000;
const RETRY_EVERY = 5 * 60 * 1000, MAX_ATTEMPTS = 288; // ~24 h
const OK_EXT = new Set(['pdf', 'dwg', 'dxf', 'step', 'stp', 'igs', 'iges', 'stl', 'sat', 'x_t', 'jpg', 'jpeg', 'png', 'webp', 'heic', 'heif', 'gif', 'tif', 'tiff', 'bmp', 'zip', 'rar', '7z', 'xlsx', 'xls', 'docx', 'doc', 'odt', 'ods', 'csv', 'txt']);

const log = (...a) => console.log(new Date().toISOString(), ...a);
const json = (res, status, body, extra = {}) => {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra });
  res.end(JSON.stringify(body));
};
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const safeName = (n) => (path.basename(String(n || 'archivo')).normalize('NFC').replace(/[^\p{L}\p{N}._ -]+/gu, '_').replace(/^\.+/, '').slice(0, 120) || 'archivo');
const ext = (n) => (n.includes('.') ? n.split('.').pop().toLowerCase() : '');

/* ---------- límite por IP (en memoria, IP con hash) ---------- */
const hits = new Map();
const rateOk = (ip) => {
  const k = createHash('sha256').update(ip).digest('hex').slice(0, 16), now = Date.now();
  const arr = (hits.get(k) || []).filter((t) => now - t < RATE_WINDOW);
  if (arr.length >= RATE_MAX) { hits.set(k, arr); return false; }
  arr.push(now); hits.set(k, arr); return true;
};
setInterval(() => { const now = Date.now(); for (const [k, v] of hits) if (!v.some((t) => now - t < RATE_WINDOW)) hits.delete(k); }, RATE_WINDOW).unref();

/* ---------- correo ---------- */
async function sendMail(dir) {
  const meta = JSON.parse(await fs.readFile(path.join(dir, 'solicitud.json'), 'utf8'));
  const attachments = [];
  for (const f of meta.files.filter((x) => x.attach)) {
    attachments.push({ filename: f.name, content: (await fs.readFile(path.join(dir, 'adjuntos', f.stored))).toString('base64') });
  }
  const rows = Object.entries(meta.fields);
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n') + `\n\nRecibida: ${meta.receivedAt}`;
  const html = `<table cellpadding="6" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px">${rows
    .map(([k, v]) => `<tr><th align="left" valign="top" style="border-bottom:1px solid #ddd;white-space:nowrap">${esc(k)}</th><td style="border-bottom:1px solid #ddd;white-space:pre-wrap">${esc(v)}</td></tr>`)
    .join('')}</table><p style="font:12px Arial,sans-serif;color:#777">Recibida: ${esc(meta.receivedAt)}</p>`;
  const r = await fetch(RESEND_URL, {
    method: 'POST',
    headers: { authorization: `Bearer ${RESEND_API_KEY}`, 'content-type': 'application/json', 'idempotency-key': `jomapaint/${meta.code}` },
    body: JSON.stringify({ from: MAIL_FROM, to: MAIL_TO, reply_to: meta.email, subject: meta.subject, text, html, attachments }),
    signal: AbortSignal.timeout(30000),
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return (await r.json()).id;
}

async function deliver(dir) {
  const st = path.join(dir, 'estado.json');
  const s = JSON.parse(await fs.readFile(st, 'utf8'));
  if (s.status !== 'pendiente') return;
  if (!RESEND_API_KEY) return;
  s.attempts += 1;
  try {
    s.resendId = await sendMail(dir);
    s.status = 'enviada'; s.sentAt = new Date().toISOString(); delete s.lastError;
    log('enviada', path.basename(dir), s.resendId);
  } catch (e) {
    s.lastError = String(e.message || e);
    if (s.attempts >= MAX_ATTEMPTS) s.status = 'fallida';
    log('ERROR envío', path.basename(dir), `intento ${s.attempts}`, s.lastError);
  }
  await fs.writeFile(st, JSON.stringify(s, null, 2));
}

async function pendingDirs() {
  const out = [];
  for (const month of await fs.readdir(DATA_DIR).catch(() => [])) {
    const m = path.join(DATA_DIR, month);
    for (const code of await fs.readdir(m).catch(() => [])) {
      const d = path.join(m, code);
      try { if (JSON.parse(await fs.readFile(path.join(d, 'estado.json'), 'utf8')).status === 'pendiente') out.push(d); } catch {}
    }
  }
  return out;
}
let retrying = false;
async function retryAll() {
  if (retrying) return; retrying = true;
  try { for (const d of await pendingDirs()) await deliver(d); } finally { retrying = false; }
}
setInterval(retryAll, RETRY_EVERY).unref();

/* ---------- recepción ---------- */
function limited(req) {
  let n = 0;
  return Readable.toWeb(req.pipe(new Transform({
    transform(chunk, _e, cb) { n += chunk.length; if (n > MAX_BODY) cb(new Error('too_large')); else cb(null, chunk); },
  })));
}

async function receive(req, res) {
  const origin = req.headers.origin || '';
  if (!ORIGINS.includes(origin)) return json(res, 403, { ok: false, error: 'origin' });
  const cors = { 'access-control-allow-origin': origin, vary: 'Origin' };
  if (Number(req.headers['content-length'] || 0) > MAX_BODY) return json(res, 413, { ok: false, error: 'too_large' }, cors);
  const ip = String(req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
  if (!rateOk(ip)) return json(res, 429, { ok: false, error: 'rate' }, cors);

  let form;
  try {
    form = await new Request('http://local/', { method: 'POST', headers: { 'content-type': req.headers['content-type'] || '' }, body: limited(req), duplex: 'half' }).formData();
  } catch (e) {
    return json(res, String(e.message).includes('too_large') ? 413 : 400, { ok: false, error: 'body' }, cors);
  }

  // Trampas antispam: campo oculto relleno o envío demasiado rápido → se responde OK y se descarta.
  const t0 = Number(form.get('_t') || 0);
  if (form.get('_honey') || !t0 || Date.now() - t0 < MIN_FILL_MS) { log('descartada (antispam)'); return json(res, 200, { ok: true }, cors); }

  const email = String(form.get('email') || '').trim();
  let code = String(form.get('Código') || '');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !/^JP-\d{6}-\d{4}$/.test(code)) return json(res, 400, { ok: false, error: 'fields' }, cors);

  const fields = {}, files = [];
  for (const [k, v] of form.entries()) {
    if (k.startsWith('_') || k === 'cf-turnstile-response') continue;
    if (typeof v === 'string') fields[k] = v.slice(0, 20000);
    else if (v && v.size) files.push(v);
  }
  const total = files.reduce((a, f) => a + f.size, 0);
  if (total > MAX_FILES_BYTES) return json(res, 413, { ok: false, error: 'too_large' }, cors);

  const now = new Date();
  const month = now.toISOString().slice(0, 7);
  let dir = path.join(DATA_DIR, month, code);
  for (let i = 2; await fs.stat(dir).then(() => true, () => false); i++) dir = path.join(DATA_DIR, month, `${code}-${i}`);
  await fs.mkdir(path.join(dir, 'adjuntos'), { recursive: true });

  const saved = [];
  for (const [i, f] of files.entries()) {
    const name = safeName(f.name), stored = `${i + 1}-${name}`;
    await fs.writeFile(path.join(dir, 'adjuntos', stored), Buffer.from(await f.arrayBuffer()));
    saved.push({ name, stored, size: f.size, attach: OK_EXT.has(ext(name)) });
  }
  const skipped = saved.filter((f) => !f.attach).map((f) => f.name);
  if (skipped.length) fields['Adjuntos no enviados (tipo no admitido; guardados en el servidor)'] = skipped.join(', ');

  const subject = String(form.get('_subject') || `Solicitud de presupuesto ${code}`).slice(0, 200);
  await fs.writeFile(path.join(dir, 'solicitud.json'), JSON.stringify({ code, email, subject, receivedAt: now.toISOString(), fields, files: saved }, null, 2));
  await fs.writeFile(path.join(dir, 'estado.json'), JSON.stringify({ status: 'pendiente', attempts: 0 }, null, 2));
  log('recibida', path.basename(dir), `${saved.length} adjunto(s)`, `${Math.round(total / 1024)} KB`);

  json(res, 200, { ok: true, code }, cors);
  setImmediate(() => deliver(dir).catch((e) => log('ERROR', e)));
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://local');
    if (req.method === 'GET' && url.pathname === '/api/salud') {
      return json(res, 200, { ok: true, correo: Boolean(RESEND_API_KEY), pendientes: (await pendingDirs()).length });
    }
    if (url.pathname === '/api/solicitud') {
      if (req.method === 'OPTIONS') {
        const o = req.headers.origin || '';
        res.writeHead(ORIGINS.includes(o) ? 204 : 403, ORIGINS.includes(o) ? { 'access-control-allow-origin': o, 'access-control-allow-methods': 'POST', 'access-control-max-age': '86400', vary: 'Origin' } : {});
        return res.end();
      }
      if (req.method === 'POST') return await receive(req, res);
    }
    json(res, 404, { ok: false });
  } catch (e) {
    log('ERROR', e);
    if (!res.headersSent) json(res, 500, { ok: false, error: 'server' });
  }
});

server.requestTimeout = 120000;
server.listen(PORT, () => {
  log(`api escuchando en :${PORT}`, RESEND_API_KEY ? 'correo activo' : 'SIN RESEND_API_KEY: se guarda pero no se envía');
  retryAll().catch((e) => log('ERROR', e));
});
