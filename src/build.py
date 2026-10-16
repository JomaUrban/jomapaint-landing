#!/usr/bin/env python3
"""Genera la landing estática de JomaPaint en ES, EU y FR.

Uso:
  python3 src/build.py                       # vista previa (GitHub Pages, noindex)
  python3 src/build.py --base https://jomapaint.es/ --index   # producción

--base   URL absoluta donde vivirá la web, con barra final. Se usa en canonical,
         hreflang, Open Graph, datos estructurados y sitemap.
--index  Permite indexar (quita el noindex). Solo en el dominio definitivo.
"""
import argparse
import datetime
import json
import os
import sys

from jinja2 import Environment, FileSystemLoader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402

DEFAULT_BASE = 'https://jomaurban.github.io/jomapaint-landing/'
NAMES = {'es': 'Español', 'eu': 'Euskara', 'fr': 'Français'}


def strip_tags(s):
    import re
    return re.sub(r'<[^>]+>', '', s).replace('&#160;', ' ').strip()


def jsonld(L, base, url):
    lang = L['meta']['lang']
    org_id = base + '#joma'
    biz_id = base + '#jomapaint'
    faq_items = L['faq']['items'][:L['faq']['schema_n']]
    graph = [
        {
            '@type': 'Organization', '@id': org_id,
            'name': 'Joma', 'legalName': 'José María Gallastegui y Cía., S.A.',
            'url': 'https://joma.es', 'foundingDate': '1942',
            'telephone': C.PHONE_TEL, 'email': C.EMAIL,
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
            'parentOrganization': {'@id': org_id},
            'knowsLanguage': ['es', 'eu', 'fr'],
            'hasOfferCatalog': {
                '@type': 'OfferCatalog', 'name': 'JomaPaint',
                'itemListElement': [
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}}
                    for n in L['services_schema']
                ],
            },
        },
        {
            '@type': 'WebPage', '@id': url, 'url': url, 'inLanguage': lang,
            'name': L['meta']['title'], 'description': L['meta']['description'],
            'about': {'@id': biz_id},
            'isPartOf': {'@type': 'WebSite', 'name': 'JomaPaint', 'url': base},
        },
        {
            '@type': 'FAQPage', 'inLanguage': lang,
            'mainEntity': [
                {'@type': 'Question', 'name': q,
                 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}}
                for q, a in faq_items
            ],
        },
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=DEFAULT_BASE)
    ap.add_argument('--index', action='store_true')
    args = ap.parse_args()
    base = args.base if args.base.endswith('/') else args.base + '/'

    env = Environment(loader=FileSystemLoader(HERE), autoescape=False, trim_blocks=False, lstrip_blocks=False)
    tpl = env.get_template('page.html.j2')

    for L in C.LANGS:
        m = L['meta']
        path = m['path']
        root = '../' * path.count('/')
        url = base + path
        langs = []
        for O in C.LANGS:
            om = O['meta']
            langs.append({
                'code': om['lang'], 'name': NAMES[om['lang']], 'locale': om['locale'],
                'abs': base + om['path'],
                'rel': (root + om['path']) or './',
                'current': om['lang'] == m['lang'],
            })
        js = dict(L['js'])
        js['lang'] = m['lang']
        js['root'] = root
        js['stCaps'] = [x[3] for x in L['process']['stations']]
        jsdata = json.dumps({'t': js, 'lang': m['lang'], 'root': root}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
        html = tpl.render(L=L, root=root, base=base, url=url, langs=langs, index=args.index,
                          jsonld=jsonld(L, base, url), jsdata=jsdata,
                          phone=C.PHONE, phone_tel=C.PHONE_TEL, email=C.EMAIL)
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print('ok', os.path.join(path, 'index.html'), len(html), 'bytes')

    today = datetime.date.today().isoformat()
    urls = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (base, L['meta']['path'], today) for L in C.LANGS)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % base)
    print('ok sitemap.xml, robots.txt  base=%s  index=%s' % (base, args.index))


if __name__ == '__main__':
    main()
