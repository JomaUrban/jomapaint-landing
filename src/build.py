#!/usr/bin/env python3
"""Genera la web estática de JomaPaint en ES, EU y FR.

Portada + una página por servicio y por idioma (ver services.py).

Uso:
  python3 src/build.py                       # GitHub Pages, indexable
  python3 src/build.py --base https://jomapaint.es/            # dominio propio
  python3 src/build.py --noindex             # copia de pruebas sin indexar

--base   URL absoluta donde vivirá la web, con barra final. Se usa en canonical,
         hreflang, Open Graph, datos estructurados y sitemap.
--noindex  Añade noindex (para copias de prueba).
"""
import argparse
import datetime
import json
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402
import services as SV  # noqa: E402
import guides as GD  # noqa: E402

DEFAULT_BASE = 'https://jomaurban.github.io/jomapaint-landing/'
NAMES = {'es': 'Español', 'eu': 'Euskara', 'fr': 'Français'}
GEO = {'@type': 'GeoCoordinates', 'latitude': 42.9432494, 'longitude': -2.6490071}
AREA_SERVED = [
    {'@type': 'AdministrativeArea', 'name': 'Araba/Álava'},
    {'@type': 'AdministrativeArea', 'name': 'Bizkaia'},
    {'@type': 'AdministrativeArea', 'name': 'Gipuzkoa'},
    {'@type': 'AdministrativeArea', 'name': 'Navarra'},
    {'@type': 'AdministrativeArea', 'name': 'La Rioja'},
    {'@type': 'AdministrativeArea', 'name': 'Burgos'},
    {'@type': 'AdministrativeArea', 'name': 'Cantabria'},
    {'@type': 'AdministrativeArea', 'name': 'Castilla y León'},
    {'@type': 'AdministrativeArea', 'name': 'Pyrénées-Atlantiques'},
    {'@type': 'AdministrativeArea', 'name': 'Gironde'},
    {'@type': 'AdministrativeArea', 'name': 'Nouvelle-Aquitaine'},
    {'@type': 'Country', 'name': 'Switzerland'},
    {'@type': 'Country', 'name': 'Portugal'},
    {'@type': 'Country', 'name': 'Ireland'},
    {'@type': 'Country', 'name': 'United Kingdom'},
    {'@type': 'Country', 'name': 'Netherlands'},
    {'@type': 'Country', 'name': 'Slovenia'},
    {'@type': 'Country', 'name': 'Bulgaria'},
]


# Páginas retiradas: slug antiguo por idioma -> clave del servicio que las sustituye.
RETIRED = [
    ({'es': 'cataforesis/', 'eu': 'kataforesia/', 'fr': 'cataphorese/'}, 'zinc'),
]
REDIRECT_TPL = '''<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<title>%(name)s · JomaPaint</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="%(abs)s">
<meta http-equiv="refresh" content="0; url=%(rel)s">
</head>
<body><p><a href="%(rel)s">%(name)s</a></p></body>
</html>
'''


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).replace('&#160;', ' ').strip()


def has_pending(s):
    return 'class="note"' in s


def svc_path(L, S):
    return L['meta']['path'] + S['slug']


def dump(graph):
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def base_nodes(L, base):
    """Organization (Joma), LocalBusiness (JomaPaint) y WebSite, comunes a todas las páginas."""
    lang = L['meta']['lang']
    org_id, biz_id = base + '#joma', base + '#jomapaint'
    catalog = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': L['services_schema'][0]}}]
    for sv in SV.SERVICES:
        S = sv[lang]
        catalog.append({'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': S['name'], 'url': base + svc_path(L, S)}})
    catalog.append({'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': L['services_schema'][-1]}})
    return [
        {
            '@type': 'Organization', '@id': org_id,
            'name': 'Joma', 'legalName': 'José María Gallastegui y Cía., S.A.',
            'url': 'https://www.joma.es', 'foundingDate': '1942',
            'telephone': C.PHONE_TEL, 'email': C.JOMA_EMAIL,
            'department': {'@id': biz_id},
        },
        {
            '@type': 'LocalBusiness', '@id': biz_id,
            'name': 'JomaPaint',
            'description': L['meta']['description'],
            'url': base,
            'image': base + L['meta']['og_image'],
            'logo': base + 'assets/apple-touch-icon.png',
            'telephone': C.PHONE_TEL, 'email': C.EMAIL,
            'address': {
                '@type': 'PostalAddress',
                'streetAddress': 'C/ San Bartolomé 11, Pol. Ind. Goiain',
                'addressLocality': 'Legutio', 'addressRegion': 'Álava',
                'postalCode': '01170', 'addressCountry': 'ES',
            },
            'geo': GEO,
            'parentOrganization': {'@id': org_id},
            'knowsLanguage': ['es', 'eu', 'fr'],
            'areaServed': AREA_SERVED,
            'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'JomaPaint', 'itemListElement': catalog},
        },
        {
            '@type': 'WebSite', '@id': base + '#website',
            'name': 'JomaPaint', 'alternateName': 'Joma Paint', 'url': base,
            'inLanguage': ['es', 'eu', 'fr'],
            'publisher': {'@id': org_id},
        },
    ]


def faq_node(lang, items):
    items = [(q, a) for q, a in items if not has_pending(a)]
    return {
        '@type': 'FAQPage', 'inLanguage': lang,
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in items],
    }


def jsonld_home(L, base, url):
    lang = L['meta']['lang']
    graph = base_nodes(L, base) + [
        {
            '@type': 'WebPage', '@id': url, 'url': url, 'inLanguage': lang,
            'name': L['meta']['title'], 'description': L['meta']['description'],
            'about': {'@id': base + '#jomapaint'}, 'isPartOf': {'@id': base + '#website'},
        },
        faq_node(lang, L['faq']['items']),
    ]
    return dump(graph)


def jsonld_service(L, S, sv, base, url, home_url):
    lang = L['meta']['lang']
    svc_id = url + '#servicio'
    img = base + 'assets/img/' + sv['img'] + '-1200.webp'
    graph = base_nodes(L, base) + [
        {
            '@type': 'Service', '@id': svc_id,
            'name': S['name'], 'serviceType': S['service_type'], 'description': S['description'],
            'url': url, 'image': img,
            'provider': {'@id': base + '#jomapaint'},
        },
        {
            '@type': 'WebPage', '@id': url, 'url': url, 'inLanguage': lang,
            'name': S['title'], 'description': S['description'],
            'about': {'@id': svc_id}, 'isPartOf': {'@id': base + '#website'},
            'primaryImageOfPage': {'@type': 'ImageObject', 'url': img},
            'breadcrumb': {'@id': url + '#ruta'},
        },
        {
            '@type': 'BreadcrumbList', '@id': url + '#ruta',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'JomaPaint', 'item': home_url},
                {'@type': 'ListItem', 'position': 2, 'name': S['crumb'], 'item': url},
            ],
        },
        faq_node(lang, S['faq']),
    ]
    return dump(graph)


def jsonld_guide(L, S, base, url, home_url):
    lang = L['meta']['lang']
    graph = base_nodes(L, base) + [
        {
            '@type': 'WebPage', '@id': url, 'url': url, 'inLanguage': lang,
            'name': S['title'], 'description': S['description'],
            'about': [{'@type': 'Thing', 'name': s['h2']} for s in S['sections']],
            'isPartOf': {'@id': base + '#website'}, 'publisher': {'@id': base + '#joma'},
            'breadcrumb': {'@id': url + '#ruta'},
        },
        {
            '@type': 'BreadcrumbList', '@id': url + '#ruta',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'JomaPaint', 'item': home_url},
                {'@type': 'ListItem', 'position': 2, 'name': S['crumb'], 'item': url},
            ],
        },
        faq_node(lang, S['faq']),
    ]
    return dump(graph)


def check_meta(where, title, desc):
    if len(title) > 62:
        print('  aviso: title de %d caracteres en %s' % (len(title), where))
    if not 110 <= len(desc) <= 165:
        print('  aviso: description de %d caracteres en %s' % (len(desc), where))


CODE_RE = re.compile(r'(?<![\w-])((?:C[1-5X]|Im[1-4])-(?:VH|[LMHI])|ISO \d{4,5}(?:-\d{1,2})?|EN \d{4,5}(?:-\d)?|UNE-EN(?: ISO)? \d{4,5})(?![\w-])')


def nowrap_codes(html):
    """Evita que «C5-M», «ISO 12944-2» o «EN 15773» se partan al final de línea (solo en el texto del body)."""
    head, sep, body = html.partition('<body')
    parts = re.split(r'(<script.*?</script>)', body, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'>([^<]+)<', lambda m: '>' + CODE_RE.sub(r'<span class="nw">\1</span>', m.group(1)) + '<', parts[i])
    return head + sep + ''.join(parts)


def write(rel_path, html):
    html = nowrap_codes(html)
    out_dir = os.path.join(ROOT, rel_path)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('ok', os.path.join(rel_path, 'index.html'), len(html), 'bytes')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=DEFAULT_BASE)
    ap.add_argument('--noindex', action='store_true')
    args = ap.parse_args()
    base = args.base if args.base.endswith('/') else args.base + '/'

    env = Environment(loader=FileSystemLoader(HERE), autoescape=False, trim_blocks=False, lstrip_blocks=False)
    tpl_home = env.get_template('page.html.j2')
    tpl_svc = env.get_template('service.html.j2')
    common = dict(base=base, index=not args.noindex, phone=C.PHONE, phone_tel=C.PHONE_TEL, email=C.EMAIL, tracking=C.TRACKING)
    sitemap = []  # (url, [(lang, url)...], x-default)

    for L in C.LANGS:
        m = L['meta']
        lang = m['lang']
        teaser = {k: p for t, p, k in L['services']['items'] if k}

        # ---------- portada ----------
        path = m['path']
        root = '../' * path.count('/')
        url = base + path
        langs = [{
            'code': O['meta']['lang'], 'name': NAMES[O['meta']['lang']], 'locale': O['meta']['locale'],
            'abs': base + O['meta']['path'], 'rel': (root + O['meta']['path']) or './',
            'current': O['meta']['lang'] == lang,
        } for O in C.LANGS]
        js = dict(L['js'])
        js['lang'] = lang
        js['root'] = root
        js['stCaps'] = [x[3] for x in L['process']['stations']]
        jsdata = json.dumps({'t': js, 'lang': lang, 'root': root, 'form': C.FORM_ENDPOINT, 'api': C.API_ENDPOINT, 'tracking': C.TRACKING,
                             'lim': {'mm': list(C.CABIN_MM), 'kg': C.MAX_KG}}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
        svc_href = {sv['key']: root + svc_path(L, sv[lang]) for sv in SV.SERVICES}
        svc_links = [{'href': svc_href[sv['key']], 'name': sv[lang]['name'], 'current': False} for sv in SV.SERVICES]
        guide_href = [root + svc_path(L, g[lang]) for g in GD.GUIDES]
        guide_links = [{'href': guide_href[i], 'name': g[lang]['crumb'], 'current': False} for i, g in enumerate(GD.GUIDES)]
        M = {
            'title': m['title'], 'description': m['description'], 'og_title': m['og_title'],
            'og_image': m['og_image'], 'og_alt': m['og_alt'], 'locale': m['locale'],
            'url': url, 'xdefault': base,
            'preload_img': {
                'src': root + 'assets/img/hero-pulverizado.webp',
                'srcset': '%sassets/img/hero-pulverizado-800.webp 800w, %sassets/img/hero-pulverizado-1200.webp 1200w, %sassets/img/hero-pulverizado.webp 2000w' % (root, root, root),
                'sizes': '100vw',
            },
        }
        check_meta(url, m['title'], m['description'])
        html = tpl_home.render(L=L, M=M, root=root, url=url, langs=langs, jsonld=jsonld_home(L, base, url), jsdata=jsdata,
                               home_href='#inicio', nav_prefix='', quote_href='#presupuesto',
                               svc_href=svc_href, svc_links=svc_links, guide_href=guide_href, guide_links=guide_links, guide=False, contact_p='', **common)
        write(path, html)
        sitemap.append((url, [(O['meta']['lang'], base + O['meta']['path']) for O in C.LANGS], base))

        # ---------- páginas de servicio ----------
        for sv in SV.SERVICES:
            S = sv[lang]
            spath = svc_path(L, S)
            sroot = '../' * spath.count('/')
            surl = base + spath
            slangs = [{
                'code': O['meta']['lang'], 'name': NAMES[O['meta']['lang']], 'locale': O['meta']['locale'],
                'abs': base + svc_path(O, sv[O['meta']['lang']]), 'rel': sroot + svc_path(O, sv[O['meta']['lang']]),
                'current': O['meta']['lang'] == lang,
            } for O in C.LANGS]
            home_rel = (sroot + path) or './'
            s_links = [{'href': sroot + svc_path(L, o[lang]), 'name': o[lang]['name'], 'current': o['key'] == sv['key']} for o in SV.SERVICES]
            related = [{'href': sroot + svc_path(L, o[lang]), 'name': o[lang]['name'], 'img': o['img'], 'teaser': teaser.get(o['key'], '')}
                       for o in SV.SERVICES if o['key'] != sv['key']]
            SM = {
                'title': S['title'], 'description': S['description'], 'og_title': S['og_title'],
                'og_image': 'assets/og/%s-%s.jpg' % (sv['key'], lang), 'og_alt': S['img_alt'], 'locale': m['locale'],
                'url': surl, 'xdefault': base + svc_path(C.ES, sv['es']),
                'preload_img': None,
            }
            check_meta(surl, S['title'], S['description'])
            html = tpl_svc.render(L=L, S=S, SV=sv, M=SM, root=sroot, url=surl, langs=slangs,
                                  jsonld=jsonld_service(L, S, sv, base, surl, url),
                                  home_href=home_rel, nav_prefix=home_rel, quote_href=home_rel + '#presupuesto',
                                  svc_links=s_links, guide_links=[{'href': sroot + svc_path(L, g[lang]), 'name': g[lang]['crumb'], 'current': False} for g in GD.GUIDES],
                                  guide=False, related=related, contact_p=L['svc']['cta_p'], **common)
            write(spath, html)
            sitemap.append((surl, [(O['meta']['lang'], base + svc_path(O, sv[O['meta']['lang']])) for O in C.LANGS], SM['xdefault']))

        # ---------- guías técnicas ----------
        for g in GD.GUIDES:
            S = g[lang]
            gpath = svc_path(L, S)
            groot = '../' * gpath.count('/')
            gurl = base + gpath
            glangs = [{
                'code': O['meta']['lang'], 'name': NAMES[O['meta']['lang']], 'locale': O['meta']['locale'],
                'abs': base + svc_path(O, g[O['meta']['lang']]), 'rel': groot + svc_path(O, g[O['meta']['lang']]),
                'current': O['meta']['lang'] == lang,
            } for O in C.LANGS]
            home_rel = (groot + path) or './'
            related = [{'href': groot + svc_path(L, o[lang]), 'name': o[lang]['name'], 'img': o['img'], 'teaser': teaser.get(o['key'], '')} for o in SV.SERVICES]
            GM = {
                'title': S['title'], 'description': S['description'], 'og_title': S['og_title'],
                'og_image': m['og_image'], 'og_alt': m['og_alt'], 'locale': m['locale'],
                'url': gurl, 'xdefault': base + svc_path(C.ES, g['es']),
                'preload_img': None,
            }
            check_meta(gurl, S['title'], S['description'])
            html = tpl_svc.render(L=L, S=S, SV=g, M=GM, root=groot, url=gurl, langs=glangs,
                                  jsonld=jsonld_guide(L, S, base, gurl, url),
                                  home_href=home_rel, nav_prefix=home_rel, quote_href=home_rel + '#presupuesto',
                                  svc_links=[{'href': groot + svc_path(L, o[lang]), 'name': o[lang]['name'], 'current': False} for o in SV.SERVICES],
                                  guide_links=[{'href': groot + svc_path(L, o[lang]), 'name': o[lang]['crumb'], 'current': o['key'] == g['key']} for o in GD.GUIDES],
                                  guide=True, related=related, contact_p=L['svc']['cta_p'], **common)
            write(gpath, html)
            sitemap.append((gurl, [(O['meta']['lang'], base + svc_path(O, g[O['meta']['lang']])) for O in C.LANGS], GM['xdefault']))

    # ---------- redirecciones de URL retiradas (no entran en el sitemap) ----------
    for O in C.LANGS:
        for old_slug, key in RETIRED:
            new_S = next(sv for sv in SV.SERVICES if sv['key'] == key)[O['meta']['lang']]
            old_path = O['meta']['path'] + old_slug[O['meta']['lang']]
            new_rel = '../' * old_path.count('/') + svc_path(O, new_S)
            out_dir = os.path.join(ROOT, old_path)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(REDIRECT_TPL % {'lang': O['meta']['lang'], 'abs': base + svc_path(O, new_S), 'rel': new_rel, 'name': new_S['name']})
            print('ok', old_path, '->', svc_path(O, new_S))

    today = datetime.date.today().isoformat()
    rows = []
    for loc, alts, xd in sitemap:
        links = ''.join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n' % (lg, u) for lg, u in alts)
        links += '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n' % xd
        rows.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n%s  </url>\n' % (loc, today, links))
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + ''.join(rows) + '</urlset>\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % base)
    print('ok sitemap.xml (%d URL), robots.txt  base=%s  index=%s' % (len(sitemap), base, not args.noindex))


if __name__ == '__main__':
    main()
