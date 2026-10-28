"""Genera boards.sql: el resumen del grupo (Dashboard) y un tablero por web.

Los tableros son del repo: cada despliegue los reescribe. Para cambiarlos, editar
este archivo y volver a generar: python3 estadisticas/boards.py > estadisticas/boards.sql
"""
import json

# clave: (website_id, nombre, board_id)
W = {
    'P':  ('a3a6b5ee-66b7-4893-a295-2e6e9fe188b4', 'JomaPaint',  '5f0c1a8e-2b7d-4c1e-9a10-000000000001'),
    'U':  ('72937a60-e911-4d1e-bf34-4e358686f870', 'Joma Urban', '5f0c1a8e-2b7d-4c1e-9a10-000000000002'),
    'N':  ('7d999b89-c4ff-4e67-83cc-b6f5cd541703', 'Normo',      '5f0c1a8e-2b7d-4c1e-9a10-000000000003'),
    'E':  ('f9227910-44f9-4cc7-9834-24ef6ec1fb9b', 'Ekilabs',    '5f0c1a8e-2b7d-4c1e-9a10-000000000004'),
    'J':  ('86cc56b6-fb47-4115-87a9-3eda024bf97d', 'Joma',       '5f0c1a8e-2b7d-4c1e-9a10-000000000005'),
    'US': ('1272970f-f4e1-4967-9c29-0de23b16aee3', 'Joma Urban (staging)', '5f0c1a8e-2b7d-4c1e-9a10-000000000006'),
    'B':  ('4f420787-9477-4bcc-a5d2-08beb430530f', 'Buzonia',    '5f0c1a8e-2b7d-4c1e-9a10-000000000007'),
    'C':  ('d27dbbce-5e95-4968-b8ec-254fb596cd68', 'Buzones Costasol', '5f0c1a8e-2b7d-4c1e-9a10-000000000008'),
    'L':  ('a4b8062f-1394-4c5e-b19b-093ceac38c9e', 'Cortelaser', '5f0c1a8e-2b7d-4c1e-9a10-000000000009'),
}
ORDER = ['P', 'U', 'J', 'L', 'N', 'B', 'C', 'E', 'US']

_n = [0]
def _id(p):
    _n[0] += 1
    return f'{p}{_n[0]}'

def comp(t, title=None, props=None, site=None, desc=None):
    c = {'type': t}
    if site:
        c.update(websiteId=W[site][0], entityType='website', entityId=W[site][0])
    if title: c['title'] = title
    if desc: c['description'] = desc
    if props: c['props'] = props
    return c

def row(*cols, sizes=None):
    out = []
    for i, c in enumerate(cols):
        col = {'id': _id('c'), 'component': c}
        if sizes: col['size'] = sizes[i]
        out.append(col)
    return {'id': _id('r'), 'columns': out}

def text(t):
    return row(comp('TextBlock', props={'text': t}))

def table(title, kind, site=None, limit=10, desc=None):
    return comp('MetricsTable', title, {'type': kind, 'limit': limit}, site=site, desc=desc)

ACC = 'Solicitudes, teléfono, email, WhatsApp y descargas'

def summary():
    g1, g2, g3 = ['P', 'U', 'J', 'L'], ['N', 'B', 'C'], ['E', 'US']
    rows = [
        text('Grupo Joma · visitas de todas las webs. Elige el periodo arriba. Detalle de cada web en Boards. Resumen ejecutivo del grupo (KPIs, conversión, canales): estadisticas.joma.es/grupo'),
        row(*[comp('RealtimeActiveUsers', f'{W[k][1]} · ahora', site=k) for k in ['P', 'U', 'N', 'B']]),
        text('Joma · JomaPaint · Joma Urban · Cortelaser'),
        row(*[comp('WebsiteMetricsBar', W[k][1], site=k) for k in g1]),
        text('Normo · Buzonia · Buzones Costasol'),
        row(*[comp('WebsiteMetricsBar', W[k][1], site=k) for k in g2]),
        text('Ekilabs · pruebas'),
        row(*[comp('WebsiteMetricsBar', W[k][1], site=k) for k in g3]),
        text('Evolución de visitas'),
        row(comp('WebsiteChart', 'JomaPaint', site='P'), comp('WebsiteChart', 'Joma Urban', site='U')),
        row(comp('WebsiteChart', 'Normo', site='N'), comp('WebsiteChart', 'Buzonia', site='B')),
        row(comp('WebsiteChart', 'Buzones Costasol', site='C'), comp('WebsiteChart', 'Ekilabs', site='E')),
        text('Acciones · lo que convierte'),
        row(*[table(W[k][1], 'event', k, desc=ACC) for k in ['P', 'U', 'N']]),
        row(*[table(W[k][1], 'event', k, desc=ACC) for k in ['B', 'C', 'E']]),
        text('De dónde llegan'),
        row(*[table(W[k][1], 'channel', k) for k in ['P', 'U', 'N']]),
        row(*[table(W[k][1], 'channel', k) for k in ['B', 'C', 'E']]),
    ]
    return {'rows': rows}

def site_board(k):
    rows = [
        row(comp('WebsiteMetricsBar')),
        row(comp('WebsiteChart', 'Visitas'), comp('RealtimeActiveUsers', 'Ahora mismo'), sizes=[3, 1]),
        row(table('Acciones', 'event', desc=ACC), comp('EventsChart', 'Acciones en el tiempo'), sizes=[1, 2]),
        row(table('Páginas más vistas', 'path'), table('Páginas de entrada', 'entry'), table('Páginas de salida', 'exit')),
        row(table('Canales', 'channel', desc='Búsqueda, directo, redes, enlaces'), table('Webs que enlazan', 'referrer'), table('Campañas (UTM)', 'utmSource')),
        row(comp('WorldMap', 'Mapa'), table('Países', 'country'), table('Ciudades', 'city'), sizes=[2, 1, 1]),
        row(table('Dispositivo', 'device', limit=5), table('Navegador', 'browser', limit=5), table('Idioma', 'language', limit=5)),
        row(comp('WeeklyTraffic', 'Tráfico por día y hora')),
    ]
    return {'websiteId': W[k][0], 'rows': rows}

def q(s):
    return "'" + s.replace("'", "''") + "'"

def upsert(board_id_sql, kind, name, desc, params):
    return '\n'.join([
        'INSERT INTO board (board_id, type, name, description, parameters, user_id, updated_at)',
        f'SELECT {board_id_sql}, {q(kind)}, {q(name)}, {q(desc)}, {q(json.dumps(params, ensure_ascii=False))}::jsonb, u.user_id, now()',
        'FROM "user" u WHERE u.username = \'admin\' AND u.deleted_at IS NULL',
        'ON CONFLICT (board_id) DO UPDATE SET type = EXCLUDED.type, name = EXCLUDED.name, description = EXCLUDED.description, parameters = EXCLUDED.parameters, updated_at = now();',
        '',
    ])

out = ['-- Generado por boards.py. No editar a mano.', '-- Dashboard (portada) del usuario admin: resumen del grupo.']
out.append(upsert('u.user_id', 'dashboard', 'Grupo · resumen', 'Todas las webs del grupo', summary()))
for k in ORDER:
    out.append(f'-- {W[k][1]}')
    out.append(upsert(f'{q(W[k][2])}::uuid', 'website', W[k][1], 'Detalle de ' + W[k][1], site_board(k)))
print('\n'.join(out))
