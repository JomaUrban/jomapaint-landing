# -*- coding: utf-8 -*-
"""Guías técnicas: «Certificaciones» y «Normas y ensayos» (ES, EU, FR).

El contenido está en guides_content.py (CERT, SOURCES). Aquí se reparte en dos
páginas, cada una con su propia URL, metadatos, secciones, preguntas y fuentes.
Las preguntas con PH('[...]') quedan fuera de FAQPage (lo filtra build.py).
"""
from guides_content import CERT, SOURCES

# Índices (desde 0) de las secciones, preguntas y fuentes de cada página.
SPLIT = {
    'certificaciones': {'sections': [0, 1, 2, 3, 4, 5, 16], 'faq': [0, 5, 6, 7], 'sources': range(0, 8)},
    'normas': {'sections': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'faq': [1, 2, 3, 4], 'sources': range(8, 18)},
}

META = {
    'certificaciones': {
        'es': {
            'slug': 'certificaciones-pintura-polvo/',
            'title': 'QUALICOAT, QUALISTEELCOAT y GSB: certificaciones del lacado',
            'description': 'Qué certifican QUALICOAT (clases 1, 1.5, 2 y 3 y SEASIDE), QUALISTEELCOAT, GSB e ISO 9001 en pintura en polvo, cómo se verifica y qué pedir al lacador.',
            'og_title': 'Certificaciones de la pintura en polvo · JomaPaint',
            'name': 'Certificaciones de la pintura en polvo', 'crumb': 'Certificaciones',
            'kicker': 'Calidad · Guía técnica',
            'h1': 'Certificaciones de la pintura en polvo',
            'lead': 'QUALICOAT, QUALISTEELCOAT, GSB e ISO 9001: qué certifica cada sello, qué te asegura y cómo se comprueba. Para leer un pliego, pedir lo correcto a un lacador y comparar ofertas con datos.',
            'facts': [('Aluminio', 'QUALICOAT', 'Clases 1 · 1.5 · 2 · 3'), ('Acero y galvanizado', 'QUALISTEELCOAT', 'Por sistema y categoría'), ('Aluminio y acero', 'GSB', 'Standard · Master · Premium')],
        },
        'eu': {
            'slug': 'hauts-pinturaren-ziurtagiriak/',
            'title': 'QUALICOAT, QUALISTEELCOAT eta GSB: lakatzearen ziurtagiriak',
            'description': 'Zer ziurtatzen duten QUALICOATek (1, 1.5, 2 eta 3 klaseak eta SEASIDE), QUALISTEELCOATek, GSBk eta ISO 9001ek, nola egiaztatzen den eta zer eskatu lakatzaileari.',
            'og_title': 'Hauts-pinturaren ziurtagiriak · JomaPaint',
            'name': 'Hauts-pinturaren ziurtagiriak', 'crumb': 'Ziurtagiriak',
            'kicker': 'Kalitatea · Gida teknikoa',
            'h1': 'Hauts-pinturaren ziurtagiriak',
            'lead': 'QUALICOAT, QUALISTEELCOAT, GSB eta ISO 9001: zigilu bakoitzak zer ziurtatzen duen, zer bermatzen dizun eta nola egiaztatzen den. Baldintza-agiri bat irakurtzeko, lakatzaileari behar dena eskatzeko eta eskaintzak datuekin alderatzeko.',
            'facts': [('Aluminioa', 'QUALICOAT', '1 · 1.5 · 2 · 3 klaseak'), ('Altzairua eta galbanizatua', 'QUALISTEELCOAT', 'Sistemaka eta kategoriaka'), ('Aluminioa eta altzairua', 'GSB', 'Standard · Master · Premium')],
        },
        'fr': {
            'slug': 'certifications-peinture-poudre/',
            'title': 'QUALICOAT, QUALISTEELCOAT et GSB : certifications du laquage',
            'description': 'Ce que certifient QUALICOAT (classes 1, 1.5, 2 et 3, SEASIDE), QUALISTEELCOAT, GSB et l’ISO 9001 en thermolaquage, comment on le vérifie et quoi exiger.',
            'og_title': 'Certifications du thermolaquage · JomaPaint',
            'name': 'Certifications du thermolaquage', 'crumb': 'Certifications',
            'kicker': 'Qualité · Guide technique',
            'h1': 'Certifications du thermolaquage',
            'lead': 'QUALICOAT, QUALISTEELCOAT, GSB et ISO 9001 : ce que certifie chaque label, ce qu’il vous garantit et comment on le vérifie. Pour lire un cahier des charges, demander ce qu’il faut à un laqueur et comparer des offres sur pièces.',
            'facts': [('Aluminium', 'QUALICOAT', 'Classes 1 · 1.5 · 2 · 3'), ('Acier et galvanisé', 'QUALISTEELCOAT', 'Par système et catégorie'), ('Aluminium et acier', 'GSB', 'Standard · Master · Premium')],
        },
    },
    'normas': {
        'es': {
            'slug': 'normas-ensayos-pintura-polvo/',
            'title': 'Normas y ensayos de pintura en polvo: ISO 12944, C5, ISO 9227',
            'description': 'ISO 12944 por partes, categorías C1 a CX, C5-M frente a C5, niebla salina ISO 9227, humedad, Kesternich, adherencia, brillo y EN 13438: qué mide cada norma.',
            'og_title': 'Normas y ensayos de la pintura en polvo · JomaPaint',
            'name': 'Normas y ensayos de la pintura en polvo', 'crumb': 'Normas y ensayos',
            'kicker': 'Calidad · Guía técnica',
            'h1': 'Normas y ensayos de la pintura en polvo',
            'lead': 'Qué dice cada norma, qué mide cada ensayo y cuánto dura: ISO 12944 parte por parte, ambientes C1 a CX, niebla salina, humedad, adherencia, brillo, preparación de superficie y normas EN. Con los ensayos del sistema C4-H.',
            'facts': [('Ambientes', 'C1 a CX', 'ISO 12944-2:2017'), ('Durabilidad', 'L · M · H · VH', 'No es una garantía'), ('Anticorrosión', 'C4-H', 'Sello en homologación')],
        },
        'eu': {
            'slug': 'hauts-pinturaren-arauak-saiakuntzak/',
            'title': 'Hauts-pinturaren arauak eta saiakuntzak: ISO 12944 eta C5',
            'description': 'ISO 12944 araua zatiz zati, C1etik CXerako kategoriak, C5-M eta C5 arteko aldea, ISO 9227 gatz-lainoaren saiakuntza, hezetasuna, Kesternich, atxikimendua, distira eta EN 13438: arau bakoitzak zer neurtzen duen.',
            'og_title': 'Hauts-pinturaren arauak eta saiakuntzak · JomaPaint',
            'name': 'Hauts-pinturaren arauak eta saiakuntzak', 'crumb': 'Arauak eta saiakuntzak',
            'kicker': 'Kalitatea · Gida teknikoa',
            'h1': 'Hauts-pinturaren arauak eta saiakuntzak',
            'lead': 'Arau bakoitzak zer dioen, saiakuntza bakoitzak zer neurtzen duen eta zenbat irauten duen: ISO 12944 zatiz zati, C1etik CXerako giroak, gatz-lainoa, hezetasuna, atxikimendua, distira, gainazalaren prestaketa eta EN arauak. C4-H sistemaren saiakuntzekin.',
            'facts': [('Giroak', 'C1etik CXera', 'ISO 12944-2:2017'), ('Iraunkortasuna', 'L · M · H · VH', 'Ez da bermea'), ('Korrosioaren aurka', 'C4-H', 'Zigilua homologatzeko bidean')],
        },
        'fr': {
            'slug': 'normes-essais-peinture-poudre/',
            'title': 'Normes et essais du thermolaquage : ISO 12944, C5, ISO 9227',
            'description': 'L’ISO 12944 expliquée partie par partie, les catégories C1 à CX, la différence entre C5-M et C5, l’essai au brouillard salin ISO 9227, l’humidité, Kesternich, l’adhérence, la brillance et l’EN 13438 : ce que mesure chaque norme.',
            'og_title': 'Normes et essais du thermolaquage · JomaPaint',
            'name': 'Normes et essais du thermolaquage', 'crumb': 'Normes et essais',
            'kicker': 'Qualité · Guide technique',
            'h1': 'Normes et essais du thermolaquage',
            'lead': 'Ce que dit chaque norme, ce que mesure chaque essai et combien de temps il dure : l’ISO 12944 partie par partie, environnements C1 à CX, brouillard salin, humidité, adhérence, brillance, préparation de surface et normes EN. Avec les essais du système C4-H.',
            'facts': [('Environnements', 'C1 à CX', 'ISO 12944-2:2017'), ('Durabilité', 'L · M · H · VH', 'Ce n’est pas une garantie'), ('Anticorrosion', 'C4-H', 'Label en cours d’homologation')],
        },
    },
}


def _page(key):
    sp = SPLIT[key]
    page = {'key': key, 'img': None}
    for lang in ('es', 'eu', 'fr'):
        src = CERT[lang]
        d = dict(META[key][lang])
        d['service_type'] = None
        d['img_alt'] = ''
        d['img_cap'] = ''
        d['sections'] = [src['sections'][i] for i in sp['sections']]
        d['faq'] = [src['faq'][i] for i in sp['faq']]
        d['sources'] = [SOURCES[lang][i] for i in sp['sources']]
        page[lang] = d
    return page


GUIDES = [_page('certificaciones'), _page('normas')]
