"""Resumen del grupo: KPIs de todas las webs en una página (estadisticas.joma.es/grupo).

Lee la base de datos de Umami en solo lectura (rol `grupo`) y pinta HTML sin
dependencias de terceros en el navegador. Acceso con usuario y contraseña
(HTTP Basic), los mismos del panel de Umami.
"""
import base64
import hmac
import html
import json
import os
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

import psycopg

TZ = ZoneInfo('Europe/Madrid')
DSN = os.environ['GRUPO_DSN']
USER = os.environ.get('GRUPO_USER', 'admin')
PASSWORD = os.environ.get('GRUPO_PASSWORD', '')
SITES = json.load(open(os.path.join(os.path.dirname(__file__), 'sites.json')))
IDS = [s['id'] for s in SITES]
BY_ID = {s['id']: s for s in SITES}
PERIODS = {'7': ('7 días', 7), '30': ('30 días', 30), '90': ('90 días', 90), '365': ('12 meses', 365)}
CONTACT_EVENTS = ('clic-telefono', 'clic-email', 'clic-whatsapp')
LEAD = 'solicitud-enviada'
COLORS = ['#2F6F8F', '#C4532F', '#6A8D3A', '#8A5A9E', '#C99A2E', '#3E8E7E', '#9C4A5A']
CHANNELS = [('buscadores', 'Buscadores'), ('directo', 'Directo'), ('redes', 'Redes'),
            ('enlaces', 'Enlaces'), ('pago', 'Pago'), ('campañas', 'Campañas')]
SEARCH = ('google.', 'bing.', 'duckduckgo.', 'yahoo.', 'ecosia.', 'qwant.', 'yandex.', 'brave.', 'startpage.',
          'chatgpt.', 'perplexity.', 'copilot.', 'gemini.')
SOCIAL = ('facebook.', 'instagram.', 'linkedin.', 'lnkd.in', 't.co', 'twitter.', 'x.com', 'youtube.',
          'tiktok.', 'pinterest.', 'whatsapp.', 'wa.me', 'threads.')


def channel(ref, medium, gclid, host):
    m = (medium or '').lower()
    if gclid or m in ('cpc', 'ppc', 'paid', 'paidsearch', 'display'):
        return 'pago'
    if m:
        return 'campañas'
    r = (ref or '').lower()
    if not r or (host and r.endswith(host.lower().removeprefix('www.'))):
        return 'directo'
    if any(k in r for k in SEARCH):
        return 'buscadores'
    if any(k in r for k in SOCIAL):
        return 'redes'
    return 'enlaces'


def query(cur, sql, params):
    cur.execute(sql, params)
    return cur.fetchall()


def load(days):
    now = datetime.now(timezone.utc)
    start = (datetime.now(TZ) - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)
    prev = start - timedelta(days=days)
    with psycopg.connect(DSN, autocommit=True) as conn, conn.cursor() as cur:
        totals_sql = """
            SELECT website_id::text,
                   count(DISTINCT session_id), count(DISTINCT visit_id),
                   count(*) FILTER (WHERE event_type = 1),
                   count(*) FILTER (WHERE event_name = %s),
                   count(*) FILTER (WHERE event_name = ANY(%s)),
                   count(*) FILTER (WHERE event_name = 'descarga')
            FROM website_event
            WHERE created_at >= %s AND created_at < %s AND website_id = ANY(%s::uuid[])
            GROUP BY 1"""
        cur_rows = query(cur, totals_sql, (LEAD, list(CONTACT_EVENTS), start, now, IDS))
        prev_rows = query(cur, totals_sql, (LEAD, list(CONTACT_EVENTS), prev, start, IDS))
        firsts = query(cur, """
            SELECT DISTINCT ON (visit_id) website_id::text, visit_id, referrer_domain, utm_medium, gclid,
                   hostname, url_path
            FROM website_event
            WHERE event_type = 1 AND created_at >= %s AND created_at < %s AND website_id = ANY(%s::uuid[])
            ORDER BY visit_id, created_at""", (start, now, IDS))
        daily = query(cur, """
            SELECT website_id::text, (created_at AT TIME ZONE 'Europe/Madrid')::date, count(DISTINCT session_id)
            FROM website_event
            WHERE created_at >= %s AND created_at < %s AND website_id = ANY(%s::uuid[])
            GROUP BY 1, 2""", (start, now, IDS))
        last = dict(query(cur, """
            SELECT website_id::text, max(created_at) FROM website_event
            WHERE website_id = ANY(%s::uuid[]) GROUP BY 1""", (IDS,)))
    keys = ('visitors', 'visits', 'views', 'leads', 'contacts', 'downloads')
    cur_m = {r[0]: dict(zip(keys, r[1:])) for r in cur_rows}
    prev_m = {r[0]: dict(zip(keys, r[1:])) for r in prev_rows}
    mix = {sid: {c: 0 for c, _ in CHANNELS} for sid in IDS}
    entries = {}
    for sid, _visit, ref, med, gclid, host, path in firsts:
        mix[sid][channel(ref, med, gclid, host)] += 1
        k = (sid, path or '/')
        entries[k] = entries.get(k, 0) + 1
    days_list = [(start + timedelta(days=i)).date() for i in range(days)]
    series = {sid: {d: 0 for d in days_list} for sid in IDS}
    for sid, d, v in daily:
        if d in series[sid]:
            series[sid][d] = v
    return {'start': start, 'now': now, 'cur': cur_m, 'prev': prev_m, 'mix': mix, 'entries': entries,
            'days': days_list, 'series': series, 'last': last}


# ---------- formato ----------

def n(x):
    return f'{int(x):,}'.replace(',', '.')


def pct(x):
    return f'{x:.1f} %'.replace('.', ',')


def delta(cur, prev):
    if not prev:
        return '<span class="d n">nuevo</span>' if cur else '<span class="d n">—</span>'
    v = (cur - prev) / prev * 100
    cls = 'up' if v > 0.5 else 'dn' if v < -0.5 else 'n'
    arrow = '▲' if cls == 'up' else '▼' if cls == 'dn' else '='
    return f'<span class="d {cls}">{arrow} {abs(v):.0f} %</span>'


def ago(ts):
    if not ts:
        return '<span class="st off">Sin datos · pendiente de instalar</span>'
    h = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
    if h < 24:
        return f'<span class="st ok">Recibiendo · hace {max(1, int(h * 60)) if h < 1 else int(h)} {"min" if h < 1 else "h"}</span>'
    if h < 24 * 7:
        return f'<span class="st warn">Último dato hace {int(h // 24)} d</span>'
    return f'<span class="st bad">Sin datos desde hace {int(h // 24)} d</span>'


def esc(s):
    return html.escape(str(s))


def chart(data):
    """Barras apiladas de visitantes por día y web (SVG)."""
    days, series = data['days'], data['series']
    totals = [sum(series[s['id']][d] for s in SITES) for d in days]
    top = max(totals + [1])
    W, H, pl, pb, pt = 960, 270, 36, 22, 12
    bw = (W - pl) / len(days)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Visitantes por día y web" class="chart">']
    for f in (0.25, 0.5, 0.75, 1):
        y = pt + (H - pb - pt) * (1 - f)
        out.append(f'<line x1="{pl}" x2="{W}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{pl - 6}" y="{y + 4:.1f}" class="ax" text-anchor="end">{n(top * f)}</text>')
    for i, d in enumerate(days):
        y = H - pb
        for j, s in enumerate(SITES):
            v = series[s['id']][d]
            if not v:
                continue
            h = v / top * (H - pb - pt)
            y -= h
            out.append(f'<rect x="{pl + i * bw + 1:.1f}" y="{y:.1f}" width="{max(bw - 2, 1):.1f}" height="{h:.1f}" '
                       f'fill="{COLORS[j]}"><title>{esc(s["name"])} · {d:%d/%m}: {n(v)}</title></rect>')
        step = max(1, len(days) // 8)
        if i % step == 0:
            out.append(f'<text x="{pl + i * bw + bw / 2:.1f}" y="{H - 6}" class="ax" text-anchor="middle">{d:%d/%m}</text>')
    out.append('</svg>')
    return ''.join(out)


def mixbar(m):
    tot = sum(m.values())
    if not tot:
        return '<div class="mix empty"></div>'
    parts = []
    for i, (c, label) in enumerate(CHANNELS):
        if m[c]:
            w = m[c] / tot * 100
            parts.append(f'<i style="width:{w:.2f}%;background:var(--ch{i})" title="{label}: {pct(w)}"></i>')
    return f'<div class="mix">{"".join(parts)}</div>'


def page(days_key):
    label, days = PERIODS[days_key]
    d = load(days)
    cur, prev = d['cur'], d['prev']
    z = dict(visitors=0, visits=0, views=0, leads=0, contacts=0, downloads=0)
    def tot(m):
        t = dict(z)
        for v in m.values():
            for k in t:
                t[k] += v[k]
        return t
    T, P = tot(cur), tot(prev)
    conv = T['leads'] / T['visits'] * 100 if T['visits'] else 0
    pconv = P['leads'] / P['visits'] * 100 if P['visits'] else 0
    allmix = {c: sum(d['mix'][sid][c] for sid in IDS) for c, _ in CHANNELS}
    mtot = sum(allmix.values())
    organic = allmix['buscadores'] / mtot * 100 if mtot else 0

    kpis = [
        ('Visitantes', n(T['visitors']), delta(T['visitors'], P['visitors']), 'personas distintas'),
        ('Visitas', n(T['visits']), delta(T['visits'], P['visits']), f'{n(T["views"])} páginas vistas'),
        ('Solicitudes', n(T['leads']), delta(T['leads'], P['leads']), 'formularios enviados'),
        ('Conversión', pct(conv), delta(conv, pconv), 'solicitudes / visitas'),
        ('Contactos directos', n(T['contacts']), delta(T['contacts'], P['contacts']), 'teléfono, email, WhatsApp'),
        ('Desde buscadores', pct(organic), '', 'de las visitas llegan de Google y similares'),
    ]
    kpi_html = ''.join(f'<div class="kpi"><div class="kl">{a}</div><div class="kv">{b}</div>'
                       f'<div class="kd">{c}<span>{e}</span></div></div>' for a, b, c, e in kpis)

    rows = []
    for g in ('Joma', 'Normo', 'Ekilabs'):
        rows.append(f'<tr class="grp"><th colspan="9">{g}</th></tr>')
        for i, s in enumerate(SITES):
            if s['group'] != g:
                continue
            c, p = cur.get(s['id'], z), prev.get(s['id'], z)
            cv = c['leads'] / c['visits'] * 100 if c['visits'] else 0
            rows.append(
                f'<tr><td><span class="dot" style="background:{COLORS[i]}"></span>'
                f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["name"])}</a>'
                f'<div class="sub">{ago(d["last"].get(s["id"]))}</div></td>'
                f'<td class="num">{n(c["visitors"])}</td><td class="num">{n(c["visits"])} {delta(c["visits"], p["visits"])}</td>'
                f'<td class="num">{n(c["leads"])}</td><td class="num">{pct(cv) if c["visits"] else "—"}</td>'
                f'<td class="num">{n(c["contacts"])}</td><td class="num">{n(c["downloads"])}</td>'
                f'<td class="mixc">{mixbar(d["mix"][s["id"]])}</td></tr>')
    legend_ch = ''.join(f'<span><i style="background:var(--ch{i})"></i>{l}</span>' for i, (_, l) in enumerate(CHANNELS))
    legend_s = ''.join(f'<span><i style="background:{COLORS[i]}"></i>{esc(s["name"])}</span>' for i, s in enumerate(SITES))

    top_entries = sorted(d['entries'].items(), key=lambda kv: -kv[1])[:12]
    ent_html = ''.join(
        f'<tr><td>{esc(BY_ID[sid]["name"])}</td><td class="path">{esc(path)}</td><td class="num">{n(v)}</td></tr>'
        for (sid, path), v in top_entries) or '<tr><td colspan="3" class="sub">Sin visitas en el periodo.</td></tr>'

    funnel_max = max(T['visits'], 1)
    funnel = ''.join(
        f'<div class="fr"><div class="fl">{l}</div><div class="fb"><i style="width:{v / funnel_max * 100:.2f}%"></i></div>'
        f'<div class="fv">{n(v)}</div></div>'
        for l, v in (('Visitas', T['visits']), ('Contactos directos', T['contacts']), ('Solicitudes', T['leads'])))

    tabs = ''.join(f'<a href="?periodo={k}" class="{"on" if k == days_key else ""}">{v[0]}</a>' for k, v in PERIODS.items())
    upd = datetime.now(TZ).strftime('%d/%m/%Y %H:%M')
    return TEMPLATE.format(tabs=tabs, label=label, kpis=kpi_html, chart=chart(d), legend_s=legend_s,
                           rows=''.join(rows), legend_ch=legend_ch, entries=ent_html, funnel=funnel,
                           start=d['start'].strftime('%d/%m/%Y'), upd=upd)


TEMPLATE = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Grupo · webs</title><style>
:root{{--bg:#F5F4F1;--card:#FFFFFF;--ink:#1B1C1E;--mut:#66686C;--line:#E4E2DD;--up:#2E7D4F;--dn:#B23A2E;
--ch0:#2F6F8F;--ch1:#9AA0A6;--ch2:#8A5A9E;--ch3:#C99A2E;--ch4:#C4532F;--ch5:#3E8E7E}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151618;--card:#1E2023;--ink:#ECEBE8;--mut:#A3A5A9;--line:#2E3034;--up:#5DBB82;--dn:#E2776B}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:28px 20px 60px}}
header{{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;justify-content:space-between;margin-bottom:22px}}
h1{{font-size:26px;margin:0;letter-spacing:-.01em}}h1 span{{color:var(--mut);font-weight:400}}
h2{{font-size:15px;margin:0 0 14px;font-weight:600}}
.tabs{{display:flex;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:3px}}
.tabs a{{padding:6px 12px;border-radius:7px;color:var(--mut);text-decoration:none;font-size:14px}}
.tabs a.on{{background:var(--ink);color:var(--bg)}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:16px}}
.kpi,.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}}
.kl{{color:var(--mut);font-size:13px}}.kv{{font-size:30px;font-weight:650;letter-spacing:-.02em;margin:4px 0 2px;font-variant-numeric:tabular-nums}}
.kd{{font-size:12.5px;color:var(--mut);display:flex;gap:8px;flex-wrap:wrap}}
.d{{font-weight:600;font-variant-numeric:tabular-nums}}.d.up{{color:var(--up)}}.d.dn{{color:var(--dn)}}.d.n{{color:var(--mut)}}
.card{{margin-bottom:16px}}.chart{{width:100%;height:auto;display:block}}
.chart .grid{{stroke:var(--line)}}.chart .ax{{fill:var(--mut);font-size:11px}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--mut);margin-top:10px}}
.legend i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}}
.tw{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
thead th{{color:var(--mut);font-weight:500;font-size:12.5px}}tr.grp th{{font-size:12px;color:var(--mut);text-transform:none;padding-top:16px;border-bottom:0}}
td.num,th.num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
td a{{color:var(--ink);font-weight:600;text-decoration:none}}td a:hover{{text-decoration:underline}}
.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px}}
.sub{{font-size:12px;color:var(--mut);margin-top:2px}}.st.ok{{color:var(--up)}}.st.warn{{color:#B7841F}}.st.bad{{color:var(--dn)}}
.mixc{{min-width:160px}}.mix{{display:flex;height:10px;border-radius:5px;overflow:hidden;background:var(--line);margin-top:5px}}.mix i{{display:block;height:100%}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}}@media (max-width:820px){{.two{{grid-template-columns:1fr}}}}
.path{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;word-break:break-all}}
.fr{{display:grid;grid-template-columns:150px 1fr 70px;gap:12px;align-items:center;margin:10px 0}}
.fl{{font-size:14px}}.fb{{background:var(--line);height:14px;border-radius:7px;overflow:hidden}}.fb i{{display:block;height:100%;background:var(--ch0)}}
.fv{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}}
footer{{color:var(--mut);font-size:12.5px;margin-top:8px}}footer a{{color:var(--mut)}}
</style></head><body><div class="wrap">
<header><div><h1>Webs del grupo <span>· {label}</span></h1>
<div class="sub">Desde el {start} · comparado con el periodo anterior · sin cookies</div></div>
<nav class="tabs">{tabs}</nav></header>
<section class="kpis">{kpis}</section>
<section class="card"><h2>Visitantes por día</h2>{chart}<div class="legend">{legend_s}</div></section>
<section class="card"><h2>Por web</h2><div class="tw"><table><thead><tr><th>Web</th><th class="num">Visitantes</th>
<th class="num">Visitas</th><th class="num">Solicitudes</th><th class="num">Conversión</th><th class="num">Contactos</th>
<th class="num">Descargas</th><th>De dónde llegan</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="legend">{legend_ch}</div></section>
<div class="two"><section class="card"><h2>Del interés al contacto · grupo</h2>{funnel}
<div class="sub">Contactos directos: clics en teléfono, email y WhatsApp. Solicitudes: formularios enviados.</div></section>
<section class="card"><h2>Por dónde entran</h2><div class="tw"><table><thead><tr><th>Web</th><th>Página de entrada</th>
<th class="num">Visitas</th></tr></thead><tbody>{entries}</tbody></table></div></section></div>
<footer>Actualizado {upd} · Detalle de cada web en <a href="/dashboard">el panel de Umami</a> · Joma Urban (staging) no cuenta en el grupo.</footer>
</div></body></html>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _auth(self):
        h = self.headers.get('Authorization', '')
        if h.startswith('Basic ') and PASSWORD:
            try:
                u, _, p = base64.b64decode(h[6:]).decode().partition(':')
            except Exception:
                return False
            return hmac.compare_digest(u, USER) and hmac.compare_digest(p, PASSWORD)
        return False

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/grupo/salud':
            return self._send(200, 'ok', 'text/plain')
        if url.path not in ('/grupo', '/grupo/'):
            return self._send(404, 'No encontrado', 'text/plain')
        if not self._auth():
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Grupo", charset="UTF-8"')
            self.end_headers()
            return
        key = parse_qs(url.query).get('periodo', ['30'])[0]
        key = key if key in PERIODS else '30'
        try:
            body = page(key)
            self._send(200, body, 'text/html; charset=utf-8')
        except Exception as e:  # noqa: BLE001
            print('error', repr(e))
            self._send(500, 'Error al leer los datos', 'text/plain')

    def _send(self, code, body, ctype):
        b = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Robots-Tag', 'noindex')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', 8000), H).serve_forever()
