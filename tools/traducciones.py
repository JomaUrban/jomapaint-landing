# -*- coding: utf-8 -*-
"""Exporta e importa los textos de la web para revisión nativa (EU y FR).

  python3 tools/traducciones.py export traducciones.csv
  python3 tools/traducciones.py import traducciones-revisado.csv

El CSV tiene una fila por texto, con el castellano de referencia, el euskera y el
francés actuales y dos columnas para la versión revisada. Al importar, cada texto
revisado sustituye literalmente al actual en el archivo de origen (src/*.py); si
el texto actual aparece más de una vez o ya no existe, se avisa y no se toca.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src')
sys.path.insert(0, SRC)

import content as C  # noqa: E402
import services as SV  # noqa: E402
import guides as GD  # noqa: E402
import guides_content as GC  # noqa: E402
import zones as ZN  # noqa: E402

# Claves que no se traducen o no se tocan (URL, códigos, imágenes, configuración)
SKIP = {'slug', 'path', 'lang', 'locale', 'key', 'img', 'img_w', 'img_h', 'og_image', 'step_imgs', 'ralName', 'area', 'draft'}
LETTERS = re.compile(r'[A-Za-zÀ-ÿ]{2,}')

FILES = {
    'content': 'src/content.py', 'services': 'src/services.py', 'guides': 'src/guides.py',
    'guides_content': 'src/guides_content.py', 'zones': 'src/zones.py',
}


def leaves(obj, path=''):
    """(ruta, texto) de cada cadena de un dict/lista anidados."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in SKIP:
                continue
            yield from leaves(v, '%s.%s' % (path, k) if path else str(k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from leaves(v, '%s[%d]' % (path, i))


def rows():
    out = []

    def add(src, section, es, eu=None, fr=None):
        e = dict(leaves(es))
        u = dict(leaves(eu)) if eu is not None else {}
        f = dict(leaves(fr)) if fr is not None else {}
        for p, t in e.items():
            if not LETTERS.search(t):
                continue
            tu, tf = u.get(p, ''), f.get(p, '')
            if not tu and not tf:
                continue
            if tu == t and tf in ('', t):
                continue  # igual en todos los idiomas (nombres propios, códigos)
            out.append({'id': '%s:%s:%s' % (src, section, p), 'archivo': FILES[src], 'ES': t, 'EU': tu, 'FR': tf})

    add('content', 'portada', C.ES, C.EU, C.FR)
    for sv in SV.SERVICES:
        add('services', sv['key'], sv['es'], sv['eu'], sv['fr'])
    for key, m in GD.META.items():
        add('guides', key, m['es'], m['eu'], m['fr'])
    add('guides_content', 'secciones', GC.CERT['es']['sections'], GC.CERT['eu']['sections'], GC.CERT['fr']['sections'])
    add('guides_content', 'preguntas', GC.CERT['es']['faq'], GC.CERT['eu']['faq'], GC.CERT['fr']['faq'])
    add('guides_content', 'fuentes', GC._LABELS['es'], GC._LABELS['eu'], GC._LABELS['fr'])
    for z in ZN.ZONES:
        add('zones', z['key'], z['es'], z.get('eu'), None)
    add('zones', 'comun-pasos', ZN.HOW['es'], ZN.HOW['eu'])
    add('zones', 'comun-preguntas', ZN.FAQ_COMMON['es'], ZN.FAQ_COMMON['eu'])
    add('zones', 'comun-fotos', {k: v[0] for k, v in ZN.GAL_TXT.items()}, {k: v[1] for k, v in ZN.GAL_TXT.items()})
    add('zones', 'comun-pie-fotos', ZN.GAL_CAP['es'], ZN.GAL_CAP['eu'])
    add('zones', 'comun-enlaces', ZN.LINK_NAMES['es'], ZN.LINK_NAMES['eu'])

    # sin duplicados exactos (mismo texto en varias páginas: se revisa una vez)
    seen, uniq = {}, []
    for r in out:
        k = (r['ES'], r['EU'], r['FR'])
        if k in seen:
            seen[k]['usos'] += 1
            continue
        r['usos'] = 1
        seen[k] = r
        uniq.append(r)
    return uniq


COLS = ['id', 'archivo', 'usos', 'ES', 'EU', 'EU_revisado', 'FR', 'FR_revisado', 'comentario']


def export(path):
    rs = rows()
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter=';', quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rs:
            w.writerow({**r, 'EU_revisado': '', 'FR_revisado': '', 'comentario': ''})
    print('%d filas → %s' % (len(rs), path))


def _py_literal_forms(s):
    """Formas en que el texto puede aparecer escrito en el .py."""
    return [s, s.replace("'", "\\'"), s.replace('"', '\\"')]


def import_(path):
    root = os.path.join(HERE, '..')
    srcs = {}
    changed = skipped = 0
    with open(path, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f, delimiter=';'):
            fn = os.path.join(root, r['archivo'])
            if fn not in srcs:
                srcs[fn] = open(fn, encoding='utf-8').read()
            for lang in ('EU', 'FR'):
                old, new = r[lang], (r.get(lang + '_revisado') or '').strip().replace("'", '’')  # apóstrofo tipográfico, como en la web
                if not new or new == old:
                    continue
                n = 0
                for i, o in enumerate(_py_literal_forms(old)):
                    n = srcs[fn].count(o)
                    if n:
                        break
                if n == 0:
                    print('NO ENCONTRADO', r['id'], lang); skipped += 1; continue
                if n > 1 and int(r.get('usos') or 1) < n:
                    print('AMBIGUO (%d veces)' % n, r['id'], lang); skipped += 1; continue
                nn = _py_literal_forms(new)[i]  # mismo escapado que el original
                srcs[fn] = srcs[fn].replace(o, nn)
                changed += 1
    for fn, txt in srcs.items():
        compile(txt, fn, 'exec')  # si el resultado no es Python válido, no se escribe nada
    for fn, txt in srcs.items():
        open(fn, 'w', encoding='utf-8').write(txt)
    print('%d textos cambiados, %d sin aplicar' % (changed, skipped))


if __name__ == '__main__':
    cmd, p = sys.argv[1], sys.argv[2]
    export(p) if cmd == 'export' else import_(p)
