// Recepción de solicitudes de presupuesto de paint.joma.es.
// Sin dependencias: Node 22 (http, fetch, FormData nativos).
//
// Flujo: valida → guarda en disco (DATA_DIR) → responde al navegador → en segundo
// plano crea una iniciativa (crm.lead, tipo «lead») en Odoo con los planos adjuntos
// y publica un mensaje que Odoo envía por email al equipo de pintura. Lo que no
// entre se reintenta cada 5 minutos, así que una caída de Odoo no pierde solicitudes.
//
// Variables de entorno:
//   ODOO_URL, ODOO_DB, ODOO_LOGIN   p. ej. https://erp.joma.es, joma, txomin@joma.es
//   ODOO_API_KEY                    clave API de ese usuario (sin ella se guarda pero no se envía)
//   ODOO_TEAM_ID                    equipo de ventas (Pintura)
//   ODOO_USER_ID                    comercial asignado (Marimar)
//   ODOO_NOTIFY_PARTNER_IDS         contactos que reciben el email, separados por coma
//   ALLOWED_ORIGINS                 orígenes permitidos (por defecto https://paint.joma.es)
//   DATA_DIR                        carpeta de solicitudes (por defecto /data)
import http from 'node:http';
import { Readable, Transform } from 'node:stream';
import { createHash } from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

const PORT = Number(process.env.PORT || 3000);
const DATA_DIR = process.env.DATA_DIR || '/data';
const ODOO_URL = (process.env.ODOO_URL || 'https://erp.joma.es').replace(/\/$/, '');
const ODOO_DB = process.env.ODOO_DB || 'joma';
const ODOO_LOGIN = process.env.ODOO_LOGIN || '';
const ODOO_API_KEY = process.env.ODOO_API_KEY || '';
const ODOO_TEAM_ID = Number(process.env.ODOO_TEAM_ID || 0) || false;
const ODOO_USER_ID = Number(process.env.ODOO_USER_ID || 0) || false;
const NOTIFY = (process.env.ODOO_NOTIFY_PARTNER_IDS || '').split(',').map((s) => Number(s.trim())).filter(Boolean);
const ODOO_READY = Boolean(ODOO_LOGIN && ODOO_API_KEY);
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

/* ---------- Odoo (JSON-RPC, servicio «object») ---------- */
let uid = null;
async function rpc(service, method, args) {
  const r = await fetch(ODOO_URL + '/jsonrpc', {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: { service, method, args }, id: Date.now() }),
    signal: AbortSignal.timeout(60000),
  });
  if (!r.ok) throw new Error(`Odoo HTTP ${r.status}`);
  const j = await r.json();
  if (j.error) throw new Error(`Odoo: ${(j.error.data && j.error.data.message) || j.error.message}`);
  return j.result;
}
async function call(model, method, args, kwargs = {}) {
  if (!uid) {
    uid = await rpc('common', 'login', [ODOO_DB, ODOO_LOGIN, ODOO_API_KEY]);
    if (!uid) throw new Error('Odoo: usuario o clave API no válidos');
  }
  return rpc('object', 'execute_kw', [ODOO_DB, uid, ODOO_API_KEY, model, method, args, kwargs]);
}

function leadHtml(meta) {
  const rows = Object.entries(meta.fields).map(([k, v]) => `<tr><th style="text-align:left;vertical-align:top;padding:4px 12px 4px 0;white-space:nowrap">${esc(k)}</th><td style="padding:4px 0;white-space:pre-wrap">${esc(v)}</td></tr>`).join('');
  return `<p>Solicitud de presupuesto recibida en paint.joma.es el ${esc(meta.receivedAt.replace('T', ' ').slice(0, 16))} (UTC).</p><table>${rows}</table>`;
}

// Cada paso guarda su resultado en estado.json: un reintento continúa donde se quedó
async function deliver(dir) {
  const st = path.join(dir, 'estado.json');
  const s = JSON.parse(await fs.readFile(st, 'utf8'));
  if (s.status !== 'pendiente' || !ODOO_READY) return;
  const save = () => fs.writeFile(st, JSON.stringify(s, null, 2));
  s.attempts += 1;
  try {
    const meta = JSON.parse(await fs.readFile(path.join(dir, 'solicitud.json'), 'utf8'));
    const f = meta.fields;
    if (!s.leadId) {
      s.leadId = await call('crm.lead', 'create', [{
        type: 'lead',
        name: `Web JomaPaint · ${meta.code} · ${f['Empresa'] || f['Nombre'] || meta.email}`.slice(0, 200),
        team_id: ODOO_TEAM_ID, user_id: ODOO_USER_ID,
        partner_name: f['Empresa'] || false, contact_name: f['Nombre'] || false,
        email_from: meta.email, phone: f['Teléfono'] || false, vat: f['CIF'] || false,
        referred: 'paint.joma.es', description: leadHtml(meta),
      }], { context: { mail_auto_subscribe_no_notify: true } });
      await save();
    }
    if (!s.attachmentIds) {
      const ids = [];
      for (const a of meta.files.filter((x) => x.attach)) {
        const datas = (await fs.readFile(path.join(dir, 'adjuntos', a.stored))).toString('base64');
        ids.push(await call('ir.attachment', 'create', [{ name: a.name, datas, res_model: 'crm.lead', res_id: s.leadId }]));
      }
      s.attachmentIds = ids;
      await save();
    }
    if (!s.messageId) {
      const body = `Nueva solicitud de presupuesto desde la web (${meta.code}). Cliente: ${f['Empresa'] || '—'}, ${f['Nombre'] || ''} <${meta.email}>${f['Teléfono'] ? ', ' + f['Teléfono'] : ''}. El detalle está en las notas de la iniciativa${s.attachmentIds.length ? ' y los planos van adjuntos' : ''}.`;
      s.messageId = await call('crm.lead', 'message_post', [[s.leadId]], {
        body, subject: meta.subject, message_type: 'comment', subtype_xmlid: 'mail.mt_comment',
        partner_ids: NOTIFY, attachment_ids: s.attachmentIds,
      });
    }
    s.status = 'enviada'; s.sentAt = new Date().toISOString(); delete s.lastError;
    log('en Odoo', path.basename(dir), `lead ${s.leadId}`);
  } catch (e) {
    uid = null;
    s.lastError = String(e.message || e);
    if (s.attempts >= MAX_ATTEMPTS) s.status = 'fallida';
    log('ERROR Odoo', path.basename(dir), `intento ${s.attempts}`, s.lastError);
  }
  await save();
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
      return json(res, 200, { ok: true, odoo: ODOO_READY, pendientes: (await pendingDirs()).length });
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
  log(`api escuchando en :${PORT}`, ODOO_READY ? 'Odoo activo' : 'SIN ODOO_API_KEY: se guarda pero no se envía');
  retryAll().catch((e) => log('ERROR', e));
});
