# -*- coding: utf-8 -*-
"""Páginas por zona: termolacado para empresas de cada territorio.

ES en las seis zonas; EU en Álava, Gipuzkoa y Bizkaia (cada zona lista los
idiomas que tiene y solo esos entran en hreflang).

Datos comunes confirmados por JomaPaint: no recogemos ni entregamos (las piezas
se traen y se recogen en Legutio, portes del cliente), plazo estándar de una
semana, presupuesto firme en menos de 24 h laborables, cabina de 6 × 2 × 0,65 m
y 165 kg por pieza. Distancias y tiempos por carretera desde la planta de
Goiain (OSRM, octubre de 2026), redondeados.

Los sectores son los habituales de cada territorio y los tipos de cliente que
ya figuran en la web («Para quién pintamos»). Sin nombres de clientes.

Bloques nuevos respecto a services.py:
  gallery  [(imagen, título, texto)]  fotos tipo; la imagen es el nombre de archivo en assets/img
"""

# Fotos tipo comunes (archivo, ES, EU)
PH_STRUCT = ('svc-zinc-800.webp', 'Estructuras y construcción', 'Egiturak eta eraikuntza')
PH_TUBE = ('svc-galvanizado-800.webp', 'Cerrajería, tubo y barandillas', 'Sarrailagintza, hodiak eta barandak')
PH_ALU = ('svc-aluminio-800.webp', 'Carpintería metálica y perfiles', 'Arotzeria metalikoa eta profilak')
PH_SHEET = ('svc-marcaje-800.webp', 'Chapa plegada y mobiliario', 'Xafla tolestua eta altzariak')
PH_LINE = ('piezas-colgadas.webp', 'Piecerío en serie', 'Seriean ekoitzitako piezak')

GAL_TXT = {
    'svc-zinc-800.webp': ('Vigas, pórticos, escaleras y entreplantas en acero, hasta 6 m de largo.', 'Habeak, portikoak, eskailerak eta solairuarteak altzairuz, 6 m-ko luzerara arte.'),
    'svc-galvanizado-800.webp': ('Barandillas, cierres y tubo, en acero o galvanizado, con imprimación si van al exterior.', 'Barandak, itxiturak eta hodiak, altzairuzkoak edo galbanizatuak, inprimazioarekin kanpoan badaude.'),
    'svc-aluminio-800.webp': ('Perfiles, chapa y piezas de aluminio para carpintería, cerramientos y fachadas.', 'Aluminiozko profilak, xaflak eta piezak, arotzeria, itxitura eta fatxadetarako.'),
    'svc-marcaje-800.webp': ('Chapa cortada y plegada, armarios, carenados y mobiliario. En la foto, buzones de Joma.', 'Xafla moztua eta tolestua, armairuak, karenatuak eta altzariak. Argazkian, Jomaren postontziak.'),
    'piezas-colgadas.webp': ('Soportes, bastidores y piezas de máquina, colgadas una a una en la cadena.', 'Euskarriak, markoak eta makina-piezak, katean banan-banan zintzilikatuta.'),
}


# Fotos de sector (Unsplash, licencia libre): referencia, no trabajos de JomaPaint
SEC_AUTOMOCION = ('sector-automocion-800.webp', 'Automoción', 'Automobilgintza')
SEC_AERONAUTICA = ('sector-aeronautica-800.webp', 'Aeronáutica', 'Aeronautika')
SEC_CNC = ('sector-cnc-800.webp', 'Máquina-herramienta', 'Makina-erremintak')
SEC_ESTRUCTURA = ('sector-estructura-800.webp', 'Estructura metálica', 'Egitura metalikoa')
SEC_SOLDADURA = ('sector-soldadura-800.webp', 'Calderería y cerrajería', 'Galdaragintza eta sarrailagintza')
SEC_TALLER = ('sector-taller-800.webp', 'Carpintería metálica', 'Arotzeria metalikoa')
SEC_EOLICA = ('sector-eolica-800.webp', 'Energía y eólica', 'Energia eta eolikoa')
SEC_AGRICOLA = ('sector-agricola-800.webp', 'Maquinaria agrícola', 'Nekazaritza-makineria')
GAL_TXT['sector-automocion-800.webp'] = ('Utillaje, bastidores, soportes y protecciones de línea.', 'Tresneria, markoak, euskarriak eta lerro-babesak.')
GAL_TXT['sector-aeronautica-800.webp'] = ('Utillaje, carros y estructuras de montaje y de hangar.', 'Muntaketa- eta hangar-tresneria, gurdiak eta egiturak.')
GAL_TXT['sector-cnc-800.webp'] = ('Carenados, puertas, bancadas y armarios de máquina.', 'Makinen karenatuak, ateak, bankadak eta armairuak.')
GAL_TXT['sector-estructura-800.webp'] = ('Vigas, pórticos, celosías y entreplantas, hasta 6 m de largo.', 'Habeak, portikoak, saretak eta solairuarteak, 6 m-ko luzerara arte.')
GAL_TXT['sector-soldadura-800.webp'] = ('Conjuntos soldados, barandillas, cierres y tubo.', 'Multzo soldatuak, barandak, itxiturak eta hodiak.')
GAL_TXT['sector-taller-800.webp'] = ('Perfiles y bastidores de acero y aluminio para cerramientos.', 'Altzairuzko eta aluminiozko profilak eta markoak itxituretarako.')
GAL_TXT['sector-eolica-800.webp'] = ('Soportes, armarios y estructuras auxiliares que van al exterior.', 'Kanpoan egongo diren euskarriak, armairuak eta egitura osagarriak.')
GAL_TXT['sector-agricola-800.webp'] = ('Chasis, tolvas, aperos y protecciones a la intemperie.', 'Xasisak, tolbak, lanabesak eta babesak, kanpoan.')

SEC_FERROVIARIO = ('sector-ferroviario-800.webp', 'Movilidad y ferrocarril', 'Mugikortasuna eta trenbidea')
SEC_CERRAJERIA = ('sector-cerrajeria-800.webp', 'Cerrajería y herrajes', 'Sarrailagintza eta burdineria')
SEC_BODEGA = ('sector-bodega-800.webp', 'Bodegas', 'Upeltegiak')
GAL_TXT['sector-ferroviario-800.webp'] = ('Bastidores, soportes, cofres y piezas de material rodante.', 'Material mugikorraren markoak, euskarriak, kutxak eta piezak.')
GAL_TXT['sector-cerrajeria-800.webp'] = ('Herrajes, tiradores, placas y pequeña pieza en serie.', 'Burdineria, heldulekuak, plakak eta seriezko pieza txikiak.')
GAL_TXT['sector-bodega-800.webp'] = ('Estructuras, soportes, pasarelas y maquinaria de bodega.', 'Upeltegietako egiturak, euskarriak, pasabideak eta makineria.')


def gallery(lang, *photos):
    i = 1 if lang == 'es' else 2
    return [(f[0], f[i], GAL_TXT[f[0]][0 if lang == 'es' else 1]) for f in photos]


def km(rows):
    """[(lugar, km, minutos)] → [(lugar, '95 km · 1 h 10 min')]"""
    out = []
    for name, d, m in rows:
        m = int(round(m / 5.0) * 5)
        t = '%d min' % m if m < 60 else ('%d h' % (m // 60) + (' %d min' % (m % 60) if m % 60 else ''))
        out.append((name, '%d km · %s' % (d, t)))
    return out


GAL_CAP = {'es': 'Fotos de referencia de los sectores para los que pintamos (Unsplash y archivo de Joma); no muestran trabajos de JomaPaint.',
           'eu': 'Pintatzen dugun sektoreen erreferentziazko argazkiak (Unsplash eta Jomaren artxiboa); ez dira JomaPaint-en lanak.'}

HOW = {
    'es': [
        ('Envía el plano', 'Plano, foto o lista de piezas, con cantidades, color RAL y acabado.'),
        ('Presupuesto firme', 'Por escrito en menos de 24 h laborables.'),
        ('Trae las piezas', 'A nuestra planta de Legutio, con tu transporte o tu transportista. Los portes no están incluidos.'),
        ('Pintamos en una semana', 'Plazo estándar desde que las piezas entran en planta.'),
        ('Recoge el pedido', 'Embaladas si lo pides, listas para tu cliente.'),
    ],
    'eu': [
        ('Bidali planoa', 'Planoa, argazkia edo pieza-zerrenda, kopuruekin, RAL kolorearekin eta akaberarekin.'),
        ('Aurrekontu irmoa', 'Idatziz, 24 lanordu baino gutxiagoan.'),
        ('Ekarri piezak', 'Legutioko gure lantegira, zure garraioarekin edo garraiolariarekin. Garraio-kostuak ez daude barne.'),
        ('Astebetean pintatzen dugu', 'Ohiko epea, piezak lantegian sartzen direnetik.'),
        ('Jaso eskaera', 'Paketatuta, hala eskatzen baduzu, zure bezeroarentzat prest.'),
    ],
}

FACTS = {
    'es': lambda d, place: [('Desde Legutio', d, place), ('Plazo estándar', '1 semana', 'Desde que entran las piezas'), ('Presupuesto firme', 'Menos de 24 h', 'En días laborables')],
    'eu': lambda d, place: [('Legutiotik', d, place), ('Ohiko epea', 'Astebete', 'Piezak sartzen direnetik'), ('Aurrekontu irmoa', '24 h baino gutxiago', 'Lanegunetan')],
}

FAQ_COMMON = {
    'es': [
        ('¿Recogéis o entregáis las piezas?', 'No. Las piezas se entregan y se recogen en nuestra planta de Legutio (C/ San Bartolomé 11, Pol. Ind. Goiain), con tu transporte o con el transportista que elijas. Los portes no están incluidos; si necesitas transporte, lo estudiamos caso a caso. Horario: de lunes a viernes, de 7:00 a 15:00.'),
        ('¿Cuánto tardáis?', 'El plazo estándar es de una semana desde que las piezas entran en planta. El presupuesto firme te lo enviamos antes, en menos de 24 horas laborables.'),
        ('¿Qué tamaño de pieza admitís?', 'Hasta 6 m de largo, 2 m de alto y 0,65 m de ancho, y hasta 165 kg por pieza. Si la tuya no entra, consúltanos.'),
    ],
    'eu': [
        ('Piezak jaso edo entregatzen dituzue?', 'Ez. Piezak Legutioko gure lantegian entregatu eta jasotzen dira (San Bartolome kalea 11, Goiain industrialdea), zure garraioarekin edo zuk aukeratutako garraiolariarekin. Garraio-kostuak ez daude barne; garraioa behar baduzu, kasuz kasu aztertuko dugu. Ordutegia: astelehenetik ostiralera, 7:00etatik 15:00etara.'),
        ('Zenbat denbora behar duzue?', 'Ohiko epea astebetekoa da, piezak lantegian sartzen direnetik. Aurrekontu irmoa lehenago bidaltzen dizugu, 24 lanordu baino lehen.'),
        ('Zer pieza-tamaina onartzen duzue?', 'Gehienez 6 m luze, 2 m garai eta 0,65 m zabal diren piezak onartzen ditugu, bakoitza 165 kg-koa gehienez. Zure pieza handiagoa bada, galdetu iezaguzu.'),
    ],
}

ZONES = [
    # ================================================================== ÁLAVA
    {
        'key': 'alava', 'area': 'Araba/Álava',
        'img': 'svc-termolacado', 'img_w': 1200, 'img_h': 800,
        'es': {
            'slug': 'termolacado-vitoria-gasteiz-alava/',
            'title': 'Termolacado en Vitoria-Gasteiz y Álava | JomaPaint',
            'description': 'Pintura en polvo al horno en Legutio, a 20 minutos de Vitoria-Gasteiz. Para la industria de Álava: presupuesto en 24 h y plazo estándar de una semana.',
            'og_title': 'Termolacado en Vitoria-Gasteiz y Álava · JomaPaint',
            'name': 'Termolacado en Vitoria-Gasteiz y Álava', 'crumb': 'Álava', 'service_type': 'Termolacado (pintura en polvo)',
            'kicker': 'Pintura en polvo en Álava',
            'h1': 'Termolacado en Vitoria-Gasteiz y Álava',
            'lead': 'Pintamos en Legutio, a unos 20 minutos de Júndiz y Ali-Gobeo. Estructuras y piezas de acero, galvanizado y aluminio para la industria alavesa, con presupuesto firme en 24 h y plazo estándar de una semana.',
            'img_alt': 'Pintura en polvo de color naranja sobre fondo negro', 'img_cap': 'Pintura en polvo',
            'facts': FACTS['es']('19 km', 'Unos 20 min a Júndiz'),
            'sections': [
                {'h2': 'Para la industria de Álava', 'p': [
                    'Álava concentra automoción y sus proveedores, aeronáutica, maquinaria y bienes de equipo, y un tejido amplio de talleres de cerrajería, carpintería metálica y calderería en Júndiz, Ali-Gobeo, la Llanada y el valle de Ayala.',
                    'Para todos ellos pintamos lo mismo que sale de un taller o de una línea: piezas sueltas, series y conjuntos soldados, desde una pieza hasta varias cadenas llenas.',
                ],
                 'cards': [
                     ('Automoción y aeronáutica', 'Utillaje, carros y bastidores de montaje, soportes, protecciones y estructuras de línea. No pintamos piezas de vuelo ni piezas que exijan homologación del fabricante del avión o del vehículo.'),
                     ('Maquinaria y bienes de equipo', 'Bancadas, carenados, puertas y armarios de máquina, en el RAL de tu marca y con el brillo que pidas.'),
                     ('Cerrajería y construcción', 'Barandillas, escaleras, cierres, pérgolas y estructuras, en acero o galvanizado, con imprimación rica en zinc si van al exterior.'),
                 ]},
                {'h2': 'Comarcas e industria', 'p': ['Para quién pintamos en cada comarca:'], 'data': [('Vitoria-Gasteiz (Júndiz, Ali-Gobeo)', 'Automoción y neumáticos, proveedores y logística'), ('Miñano (Parque Tecnológico de Álava)', 'Aeronáutica e ingeniería'), ('Aiaraldea (Laudio, Amurrio)', 'Tubo de acero, fundición y calderería'), ('Llanada (Agurain, Legutio)', 'Metal, maquinaria y equipamiento')]},
                {'h2': 'Fotos tipo', 'gallery': gallery('es', SEC_AUTOMOCION, SEC_AERONAUTICA, SEC_CNC, SEC_ESTRUCTURA), 'gallery_cap': GAL_CAP['es']},
                {'h2': 'Cómo trabajamos con empresas alavesas', 'steps': HOW['es']},
                {'h2': 'A qué distancia estamos', 'p': ['Estamos en el polígono de Goiain, en Legutio, junto a la N-240 entre Vitoria-Gasteiz y Bilbao. Distancias por carretera desde la planta, aproximadas:'],
                 'data': km([('Vitoria-Gasteiz (Júndiz)', 19, 22), ('Arrasate (Gipuzkoa)', 24, 27), ('Agurain', 34, 28), ('Amurrio', 44, 40), ('Laudio/Llodio', 53, 44)])},
                {'h2': 'La pintura según dónde vaya la pieza', 'p': [
                    'En la Llanada y en Vitoria-Gasteiz, el exterior suele ser un ambiente C2 o C3 según la ISO 12944-2: urbano o industrial moderado. Para eso basta un poliéster de exterior bien curado sobre un buen pretratamiento.',
                    'Si la pieza va a una carretera con sal de deshielo, a una zona industrial agresiva o a la costa, subimos el sistema: imprimación rica en zinc y poliéster, nuestro sistema C4-H, con el sello en proceso de homologación.',
                ]},
            ],
            'faq': FAQ_COMMON['es'] + [
                ('¿Puedo llevar las piezas el mismo día que pido presupuesto?', 'Sí, pero te recomendamos esperar al presupuesto firme: así sabes precio y plazo antes de traerlas. Llámanos al 945 31 87 70 (ext. 3) y te decimos cuándo puedes venir.'),
            ],
        },
        'eu': {
            'slug': 'termolakatzea-gasteiz-araba/',
            'title': 'Termolakatzea Gasteizen eta Araban | JomaPaint',
            'description': 'Labean ondutako hauts-pintura Legution, Gasteiztik 20 bat minutura. Arabako industriarentzat: aurrekontua 24 orduan eta astebeteko ohiko epea.',
            'og_title': 'Termolakatzea Gasteizen eta Araban · JomaPaint',
            'name': 'Termolakatzea Gasteizen eta Araban', 'crumb': 'Araba', 'service_type': 'Termolakatzea (hauts-pintura)',
            'kicker': 'Hauts-pintura Araban',
            'h1': 'Termolakatzea Gasteizen eta Araban',
            'lead': 'Legution pintatzen dugu, Jundiztik eta Ali-Gobeotik 20 bat minutura. Altzairuzko, altzairu galbanizatuzko eta aluminiozko egiturak eta piezak Arabako industriarentzat, aurrekontu irmoa 24 orduan eta astebeteko ohiko epea.',
            'img_alt': 'Kolore laranjako hauts-pintura hondo beltzean', 'img_cap': 'Hauts-pintura',
            'facts': FACTS['eu']('19 km', '20 bat min Jundizera'),
            'sections': [
                {'h2': 'Arabako industriarentzat', 'p': [
                    'Araban automobilgintza eta haren hornitzaileak, aeronautika, makineria eta ekipamendu industriala daude, baita sarrailagintza-, arotzeria metaliko- eta galdaragintza-tailer ugari ere Jundizen, Ali-Gobeon, Lautadan eta Aiaraldean.',
                    'Guztientzat pintatzen dugu tailer edo lerro batetik ateratzen dena: pieza solteak, serieak eta soldatutako multzoak, pieza bakar batetik hainbat kate betera arte.',
                ],
                 'cards': [
                     ('Automobilgintza eta aeronautika', 'Muntaketa-tresneria, gurdiak eta markoak, euskarriak, babesak eta lerro-egiturak. Ez dugu hegaldiko piezarik pintatzen, ezta hegazkinaren edo ibilgailuaren fabrikatzailearen homologazioa behar duen piezarik ere.'),
                     ('Makineria eta ekipamendu industriala', 'Bankadak, karenatuak, makina-ateak eta -armairuak, zure markaren RAL kolorean eta eskatzen duzun distirarekin.'),
                     ('Sarrailagintza eta eraikuntza', 'Barandak, eskailerak, itxiturak, pergolak eta egiturak, altzairuzkoak nahiz galbanizatuak. Kanpoan jartzeko badira, zinkez aberastutako inprimazioa erabiltzen dugu.'),
                 ]},
                {'h2': 'Eskualdeak eta industria', 'p': ['Eskualde bakoitzean norentzat pintatzen dugun:'], 'data': [('Gasteiz (Jundiz, Ali-Gobeo)', 'Automobilgintza eta pneumatikoak, hornitzaileak eta logistika'), ('Miñao (Arabako Parke Teknologikoa)', 'Aeronautika eta ingeniaritza'), ('Aiaraldea (Laudio, Amurrio)', 'Altzairuzko hodiak, galdaketa eta galdaragintza'), ('Lautada (Agurain, Legutio)', 'Metala, makineria eta ekipamendua')]},
                {'h2': 'Argazki adierazgarriak', 'gallery': gallery('eu', SEC_AUTOMOCION, SEC_AERONAUTICA, SEC_CNC, SEC_ESTRUCTURA), 'gallery_cap': GAL_CAP['eu']},
                {'h2': 'Nola lan egiten dugun Arabako enpresekin', 'steps': HOW['eu']},
                {'h2': 'Zer distantziatara gaude?', 'p': ['Goiaingo industrialdean gaude, Legution, N-240 errepidearen ondoan, Vitoria-Gasteiz eta Bilbo artean. Lantegitik errepidez dauden gutxi gorabeherako distantziak:'],
                 'data': km([('Vitoria-Gasteiz (Jundiz)', 19, 22), ('Arrasate (Gipuzkoa)', 24, 27), ('Agurain', 34, 28), ('Amurrio', 44, 40), ('Laudio', 53, 44)])},
                {'h2': 'Pintura-sistema, piezaren kokapenaren arabera', 'p': [
                    'Lautadan eta Gasteizen, kanpoko korrosibitate-kategoria C2 edo C3 izan ohi da, ISO 12944-2 arauaren arabera: hiri- edo industria-ingurune moderatuetan. Horretarako, nahikoa izan ohi da aurretratamendu egoki baten gainean aplikatutako eta behar bezala ondutako kanporako poliesterrezko hauts-pintura.',
                    'Pieza izotz-gatza duen errepide batera, industria-gune oldarkor batera edo kostaldera badoa, sistema indartzen dugu: zinkez aberastutako inprimazioa eta poliesterra, gure C4-H sistema, zigilua homologatzeko bidean.',
                ]},
            ],
            'faq': FAQ_COMMON['eu'] + [
                ('Aurrekontua eskatzen dudan egunean bertan ekar ditzaket piezak?', 'Bai, baina aurrekontu irmoaren zain egotea gomendatzen dizugu: horrela, prezioa eta epea jakingo dituzu piezak ekarri aurretik. Deitu 945 31 87 70 zenbakira (3. luzapena) eta noiz etor zaitezkeen esango dizugu.'),
            ],
        },
    },
    # ================================================================== GIPUZKOA
    {
        'key': 'gipuzkoa', 'area': 'Gipuzkoa',
        'img': 'svc-galvanizado', 'img_w': 1200, 'img_h': 800,
        'es': {
            'slug': 'termolacado-gipuzkoa-donostia/',
            'title': 'Termolacado en Gipuzkoa y Donostia | JomaPaint',
            'description': 'Pintura en polvo al horno para empresas de Gipuzkoa: Arrasate a 25 minutos, Eibar a 40 y Donostia a algo más de una hora. Presupuesto en 24 h y plazo de una semana.',
            'og_title': 'Termolacado en Gipuzkoa y Donostia · JomaPaint',
            'name': 'Termolacado en Gipuzkoa y Donostia', 'crumb': 'Gipuzkoa', 'service_type': 'Termolacado (pintura en polvo)',
            'kicker': 'Pintura en polvo para Gipuzkoa',
            'h1': 'Termolacado para Gipuzkoa y Donostia',
            'lead': 'Desde Legutio estamos a 25 minutos de Arrasate, a 40 de Eibar y a algo más de una hora de Donostia-San Sebastián. Pintamos piezas y estructuras para la industria guipuzcoana, también para la costa, con presupuesto firme en 24 h.',
            'img_alt': 'Tubos de acero galvanizado apilados', 'img_cap': 'Tubo galvanizado',
            'facts': FACTS['es']('95 km', 'Unos 70 min a Donostia'),
            'sections': [
                {'h2': 'Para la industria de Gipuzkoa', 'p': [
                    'En Debagoiena y en el Bajo Deba hay máquina-herramienta, componentes, cerrajería y herrajes; en el Goierri, material ferroviario y calderería; en Tolosaldea, Donostialdea y Bidasoa, talleres, carpintería metálica y construcción.',
                    'Muchos están más cerca de Legutio que de la costa: desde Arrasate o Bergara se llega en media hora.',
                ],
                 'cards': [
                     ('Máquina-herramienta y bienes de equipo', 'Carenados, puertas, bancadas, cuadros y armarios en el RAL de tu marca, con un acabado uniforme de pieza a pieza y de lote a lote.'),
                     ('Cerrajería y herrajes', 'Herrajes, soportes, tapas y pequeña pieza en serie, colgados uno a uno en la cadena.'),
                     ('Carpintería metálica y construcción', 'Barandillas, cierres, escaleras y estructuras. Cerca del mar, con imprimación rica en zinc debajo.'),
                 ]},
                {'h2': 'Comarcas e industria', 'p': ['Para quién pintamos en cada comarca:'], 'data': [('Arrasate y Debagoiena', 'Cerrajería, herrajes y componentes'), ('Elgoibar, Eibar y Debabarrena', 'Máquina-herramienta y mecanizado'), ('Beasain y Goierri', 'Movilidad y material ferroviario'), ('Tolosaldea', 'Papel y su maquinaria'), ('Donostialdea y Bidasoa', 'Naval y portuaria, construcción y carpintería metálica')]},
                {'h2': 'Fotos tipo', 'gallery': gallery('es', SEC_CERRAJERIA, SEC_FERROVIARIO, SEC_CNC, SEC_SOLDADURA), 'gallery_cap': GAL_CAP['es']},
                {'h2': 'Cómo trabajamos con empresas guipuzcoanas', 'steps': HOW['es']},
                {'h2': 'A qué distancia estamos', 'p': ['Distancias por carretera desde la planta de Legutio, aproximadas:'],
                 'data': km([('Arrasate-Mondragón', 24, 27), ('Bergara', 36, 31), ('Eibar', 48, 38), ('Elgoibar', 50, 39), ('Beasain', 59, 48), ('Tolosa', 74, 58), ('Donostia-San Sebastián', 95, 70), ('Irun', 112, 81)])},
                {'h2': 'Costa y valles: no es el mismo ambiente', 'p': [
                    'Para la ISO 12944-2, la costa con salinidad moderada es un ambiente C4, y la primera línea de mar puede llegar a C5. En los valles del interior, el exterior suele quedarse en C3.',
                    'Para piezas que van a Donostia, Pasaia, Hondarribia o a cualquier punto cerca del mar, recomendamos imprimación rica en zinc y poliéster: nuestro sistema C4-H, con el sello en proceso de homologación. En el interior suele bastar una sola capa de poliéster de exterior.',
                ]},
            ],
            'faq': FAQ_COMMON['es'] + [
                ('Mis piezas van a primera línea de mar. ¿Qué me recomendáis?', 'Imprimación rica en zinc y acabado de poliéster de exterior, o partir de acero galvanizado. Cuéntanos dónde irá la pieza y te proponemos el sistema en el presupuesto.'),
            ],
        },
        'eu': {
            'slug': 'termolakatzea-gipuzkoa-donostia/',
            'title': 'Gipuzkoarako eta Donostiarako termolakatzea | JomaPaint',
            'description': 'Labean ondutako hauts-pintura Gipuzkoako enpresentzat: Arrasate 25 minutura, Eibar 40ra eta Donostia ordubete pasatxora. Aurrekontua 24 orduan eta astebeteko ohiko epea.',
            'og_title': 'Gipuzkoarako eta Donostiarako termolakatzea · JomaPaint',
            'name': 'Gipuzkoarako eta Donostiarako termolakatzea', 'crumb': 'Gipuzkoa', 'service_type': 'Termolakatzea (hauts-pintura)',
            'kicker': 'Gipuzkoako enpresentzako hauts-pintura',
            'h1': 'Gipuzkoako eta Donostiako enpresentzako termolakatzea',
            'lead': 'Legutiotik Arrasatera 25 minutu daude, Eibarrera 40 eta Donostiara ordubete pasatxo. Gipuzkoako industriarentzat piezak eta egiturak pintatzen ditugu, baita kostaldera doazenak ere, aurrekontu irmoa 24 orduan.',
            'img_alt': 'Altzairu galbanizatuzko hodiak pilatuta', 'img_cap': 'Hodi galbanizatua',
            'facts': FACTS['eu']('95 km', '70 bat min Donostiara'),
            'sections': [
                {'h2': 'Gipuzkoako industriarentzat', 'p': [
                    'Debagoienean eta Debabarrenean makina-erremintak, osagaiak, sarrailagintza eta burdineria daude; Goierrin, trenbide-materiala eta galdaragintza; Tolosaldean, Donostialdean eta Bidasoan, tailerrak, arotzeria metalikoa eta eraikuntza.',
                    'Horietako askorentzat Legutio kostaldea baino gertuago dago: Arrasatetik edo Bergaratik ordu erdian irits daiteke.',
                ],
                 'cards': [
                     ('Makina-erremintak eta ekipamendu industriala', 'Karenatuak, ateak, bankadak, koadroak eta armairuak zure markaren RAL kolorean, akabera berdinarekin piezatik piezara eta loteetik lotera.'),
                     ('Sarrailagintza eta burdineria', 'Burdineria, euskarriak, tapak eta seriezko pieza txikiak, katean banan-banan zintzilikatuta.'),
                     ('Arotzeria metalikoa eta eraikuntza', 'Barandak, itxiturak, eskailerak eta egiturak. Itsasotik gertu, azpian zinkez aberastutako inprimazioarekin.'),
                 ]},
                {'h2': 'Eskualdeak eta industria', 'p': ['Eskualde bakoitzean norentzat pintatzen dugun:'], 'data': [('Arrasate eta Debagoiena', 'Sarrailagintza, burdineria eta osagaiak'), ('Elgoibar, Eibar eta Debabarrena', 'Makina-erremintak eta mekanizazioa'), ('Beasain eta Goierri', 'Mugikortasuna eta trenbide-materiala'), ('Tolosaldea', 'Papera eta haren makineria'), ('Donostialdea eta Bidasoa', 'Ontzigintza eta portua, eraikuntza eta arotzeria metalikoa')]},
                {'h2': 'Argazki adierazgarriak', 'gallery': gallery('eu', SEC_CERRAJERIA, SEC_FERROVIARIO, SEC_CNC, SEC_SOLDADURA), 'gallery_cap': GAL_CAP['eu']},
                {'h2': 'Nola lan egiten dugun Gipuzkoako enpresekin', 'steps': HOW['eu']},
                {'h2': 'Zer distantziatara gaude?', 'p': ['Legutioko lantegitik errepidez dauden gutxi gorabeherako distantziak:'],
                 'data': km([('Arrasate', 24, 27), ('Bergara', 36, 31), ('Eibar', 48, 38), ('Elgoibar', 50, 39), ('Beasain', 59, 48), ('Tolosa', 74, 58), ('Donostia', 95, 70), ('Irun', 112, 81)])},
                {'h2': 'Kostaldea eta haranak: ez da giro bera', 'p': [
                    'ISO 12944-2 arauaren arabera, gazitasun moderatuko kostaldeari C4 korrosibitate-kategoria dagokio, eta itsasertzeko lehen lerroan C5era ere irits daiteke. Barnealdeko haranetan C3 izan ohi da.',
                    'Donostiara, Pasaiara, Hondarribira edo itsasotik gertuko edozein lekutara doazen piezetarako, zinkez aberastutako inprimazioa eta poliesterra gomendatzen ditugu: gure C4-H sistema, zigilua homologatzeko bidean. Barnealdean, kanporako poliester-geruza bakarra nahikoa izan ohi da.',
                ]},
            ],
            'faq': FAQ_COMMON['eu'] + [
                ('Nire piezak itsasertzean jarriko dira. Zer gomendatzen didazue?', 'Zinkez aberastutako inprimazioa eta kanporako poliester-akabera, edo altzairu galbanizatutik abiatzea. Esan iezaguzu non egongo den pieza eta aurrekontuan sistema proposatuko dizugu.'),
            ],
        },
    },
    # ================================================================== BIZKAIA
    {
        'key': 'bizkaia', 'area': 'Bizkaia',
        'img': 'svc-zinc', 'img_w': 1200, 'img_h': 800,
        'es': {
            'slug': 'termolacado-bizkaia-bilbao/',
            'title': 'Termolacado para Bizkaia y Bilbao | JomaPaint',
            'description': 'Pintura en polvo al horno para empresas de Bizkaia: Durango a 35 minutos y Bilbao a menos de una hora de Legutio. Presupuesto en 24 h y plazo estándar de una semana.',
            'og_title': 'Termolacado para Bizkaia y Bilbao · JomaPaint',
            'name': 'Termolacado para Bizkaia y Bilbao', 'crumb': 'Bizkaia', 'service_type': 'Termolacado (pintura en polvo)',
            'kicker': 'Pintura en polvo para Bizkaia',
            'h1': 'Termolacado para Bizkaia y Bilbao',
            'lead': 'Legutio está a 35 minutos de Durango y a menos de una hora de Bilbao. Pintamos estructuras, calderería y piezas para la industria vizcaína, con presupuesto firme en 24 h y plazo estándar de una semana.',
            'img_alt': 'Estructura de acero pintada con una cartela atornillada, vista desde abajo', 'img_cap': 'Estructura de acero',
            'facts': FACTS['es']('67 km', 'Unos 55 min a Bilbao'),
            'sections': [
                {'h2': 'Para la industria de Bizkaia', 'p': [
                    'Bizkaia tiene estructura metálica y calderería, bienes de equipo, energía y eólica, industria naval y portuaria, y en el Duranguesado, forja y componentes.',
                    'Son piezas grandes y conjuntos soldados que muchas veces van al exterior o cerca de la ría y del mar. Nuestra cabina admite piezas de hasta 6 m de largo y 165 kg.',
                ],
                 'cards': [
                     ('Estructura metálica y calderería', 'Vigas, pórticos, entreplantas, escaleras, bastidores y depósitos que entren en cabina, con el sistema adecuado para dónde van a estar.'),
                     ('Energía y bienes de equipo', 'Soportes, carenados, cuadros, armarios y estructuras auxiliares para eólica, eléctrica y maquinaria.'),
                     ('Carpintería metálica y construcción', 'Barandillas, cierres, celosías y escaleras en acero, galvanizado o aluminio.'),
                 ]},
                {'h2': 'Comarcas e industria', 'p': ['Para quién pintamos en cada comarca:'], 'data': [('Durangaldea y Ermua', 'Forja, estampación y automoción'), ('Zamudio y Derio (Parque Tecnológico)', 'Energía, eólica e ingeniería'), ('Margen izquierda (Barakaldo, Sestao)', 'Siderurgia y calderería'), ('Puerto de Bilbao', 'Estructuras y equipos portuarios')]},
                {'h2': 'Fotos tipo', 'gallery': gallery('es', SEC_ESTRUCTURA, SEC_EOLICA, SEC_SOLDADURA, SEC_TALLER), 'gallery_cap': GAL_CAP['es']},
                {'h2': 'Cómo trabajamos con empresas vizcaínas', 'steps': HOW['es']},
                {'h2': 'A qué distancia estamos', 'p': ['Distancias por carretera desde la planta de Legutio, aproximadas:'],
                 'data': km([('Durango', 33, 35), ('Ermua', 52, 41), ('Zamudio', 58, 55), ('Basauri', 64, 52), ('Bilbao', 67, 53), ('Barakaldo', 73, 59)])},
                {'h2': 'Ría, puerto y costa', 'p': [
                    'Las zonas industriales húmedas y la costa con salinidad moderada son un ambiente C4 según la ISO 12944-2; los entornos portuarios y la primera línea de mar pueden llegar a C5.',
                    'Para estructuras que van al exterior en el Gran Bilbao, en el puerto o en la costa, recomendamos imprimación rica en zinc y poliéster: nuestro sistema C4-H, con el sello en proceso de homologación. Si la pieza ya viene galvanizada, la pintamos sobre el galvanizado con su pretratamiento.',
                ]},
            ],
            'faq': FAQ_COMMON['es'] + [
                ('¿Pintáis estructuras ya galvanizadas?', 'Sí. Es el sistema dúplex: galvanizado más pintura en polvo. El galvanizado necesita un pretratamiento propio para que el polvo agarre y no salgan poros. Lo explicamos en la página de acero galvanizado.'),
            ],
        },
        'eu': {
            'slug': 'termolakatzea-bizkaia-bilbo/',
            'title': 'Bizkairako eta Bilborako termolakatzea | JomaPaint',
            'description': 'Labean ondutako hauts-pintura Bizkaiko enpresentzat: Durango 35 minutura eta Bilbo ordubete baino gutxiagora. Aurrekontua 24 orduan eta astebeteko ohiko epea.',
            'og_title': 'Bizkairako eta Bilborako termolakatzea · JomaPaint',
            'name': 'Bizkairako eta Bilborako termolakatzea', 'crumb': 'Bizkaia', 'service_type': 'Termolakatzea (hauts-pintura)',
            'kicker': 'Bizkaiko enpresentzako hauts-pintura',
            'h1': 'Bizkairako eta Bilborako termolakatzea',
            'lead': 'Legutio Durangotik 35 minutura dago, eta Bilbotik ordubete baino gutxiagora. Bizkaiko industriarentzat egiturak, galdaragintza eta piezak pintatzen ditugu, aurrekontu irmoa 24 orduan eta astebeteko ohiko epea.',
            'img_alt': 'Altzairuzko egitura pintatua, torlojuz lotutako plaka batekin, behetik ikusia', 'img_cap': 'Altzairuzko egitura',
            'facts': FACTS['eu']('67 km', '55 bat min Bilbora'),
            'sections': [
                {'h2': 'Bizkaiko industriarentzat', 'p': [
                    'Bizkaian egitura metalikoak eta galdaragintza, ekipamendu industriala, energia eta eolikoa, ontzigintza eta portu-industria daude, eta Durangaldean, forja eta osagaiak.',
                    'Pieza handiak eta soldatutako multzoak dira, askotan kanpora edo itsasadarretik eta itsasotik gertu doazenak. Gure kabinak 6 m-ko luzera eta 165 kg arteko piezak onartzen ditu.',
                ],
                 'cards': [
                     ('Egitura metalikoak eta galdaragintza', 'Habeak, portikoak, solairuarteak, eskailerak, bastidoreak eta kabinan sartzeko moduko tangak, kokatuko diren ingurunera egokitutako babes-sistemarekin.'),
                     ('Energia eta ekipamendu industriala', 'Euskarriak, karenatuak, koadroak, armairuak eta egitura osagarriak, eolikorako, elektrizitaterako eta makineriarako.'),
                     ('Arotzeria metalikoa eta eraikuntza', 'Barandak, itxiturak, sareta-hesiak eta eskailerak, altzairuzkoak, galbanizatuak edo aluminiozkoak.'),
                 ]},
                {'h2': 'Eskualdeak eta industria', 'p': ['Eskualde bakoitzean norentzat pintatzen dugun:'], 'data': [('Durangaldea eta Ermua', 'Forja, estanpazioa eta automobilgintza'), ('Zamudio eta Derio (Parke Teknologikoa)', 'Energia, eolikoa eta ingeniaritza'), ('Ezkerraldea (Barakaldo, Sestao)', 'Siderurgia eta galdaragintza'), ('Bilboko portua', 'Portuko egiturak eta ekipoak')]},
                {'h2': 'Argazki adierazgarriak', 'gallery': gallery('eu', SEC_ESTRUCTURA, SEC_EOLICA, SEC_SOLDADURA, SEC_TALLER), 'gallery_cap': GAL_CAP['eu']},
                {'h2': 'Nola lan egiten dugun Bizkaiko enpresekin', 'steps': HOW['eu']},
                {'h2': 'Zer distantziatara gaude?', 'p': ['Legutioko lantegitik errepidez dauden gutxi gorabeherako distantziak:'],
                 'data': km([('Durango', 33, 35), ('Ermua', 52, 41), ('Zamudio', 58, 55), ('Basauri', 64, 52), ('Bilbo', 67, 53), ('Barakaldo', 73, 59)])},
                {'h2': 'Itsasadarra, portua eta kostaldea', 'p': [
                    'ISO 12944-2 arauaren arabera, industria-ingurune hezeak eta gazitasun moderatuko kostaldeak C4 korrosibitate-kategorian sar daitezke; portu-inguruneak eta itsasertzeko lehen lerroa C5 kategoriara irits daitezke.',
                    'Bilbo Handian, portuan edo kostaldean kanpoan egongo diren egituretarako, zinkez aberastutako inprimazioa eta poliesterra gomendatzen ditugu: gure C4-H sistema, zigilua homologatzeko bidean. Pieza galbanizatuta badator, galbanizatuaren gainean pintatzen dugu, bere aurretratamenduarekin.',
                ]},
            ],
            'faq': FAQ_COMMON['eu'] + [
                ('Galbanizatutako egiturak pintatzen dituzue?', 'Bai. Sistema duplexa da: galbanizazioa eta hauts-pintura uztartzen ditu. Altzairu galbanizatuak aurretratamendu berezia behar du pintura ondo itsasteko eta pororik ez sortzeko. Altzairu galbanizatuari buruzko orrian azaltzen dugu.'),
            ],
        },
    },
    # ================================================================== BURGOS
    {
        'key': 'burgos', 'area': 'Burgos',
        'img': 'svc-zinc', 'img_w': 1200, 'img_h': 800,
        'es': {
            'slug': 'termolacado-burgos-miranda-de-ebro/',
            'title': 'Termolacado para Burgos y Miranda de Ebro | JomaPaint',
            'description': 'Pintura en polvo al horno para empresas de Burgos: Miranda de Ebro a 40 minutos de Legutio y Burgos capital a hora y media. Presupuesto en 24 h y plazo de 1 semana.',
            'og_title': 'Termolacado para Burgos y Miranda de Ebro · JomaPaint',
            'name': 'Termolacado para Burgos y Miranda de Ebro', 'crumb': 'Burgos', 'service_type': 'Termolacado (pintura en polvo)',
            'kicker': 'Pintura en polvo para la provincia de Burgos',
            'h1': 'Termolacado para Burgos y Miranda de Ebro',
            'lead': 'Miranda de Ebro está a 40 minutos de nuestra planta de Legutio, y Burgos capital, a hora y media. Pintamos piezas y estructuras para la industria burgalesa, con presupuesto firme en 24 h y plazo estándar de una semana.',
            'img_alt': 'Estructura de acero pintada con una cartela atornillada, vista desde abajo', 'img_cap': 'Estructura de acero',
            'facts': FACTS['es']('47 km', 'Unos 40 min a Miranda'),
            'sections': [
                {'h2': 'Para la industria de Burgos', 'p': [
                    'En Burgos capital, Miranda de Ebro, Briviesca y las Merindades hay automoción y componentes, química, agroalimentación, maquinaria agrícola y un buen número de talleres de cerrajería y estructura.',
                    'Para una empresa de Miranda, Legutio está más cerca que muchos polígonos de la propia provincia.',
                ],
                 'cards': [
                     ('Automoción y componentes', 'Soportes, bastidores, utillaje y protecciones de línea, en serie y con el mismo acabado lote a lote. No pintamos piezas que exijan la homologación del fabricante del vehículo.'),
                     ('Maquinaria agrícola y agroalimentaria', 'Chasis, tolvas, protecciones y carenados que van a la intemperie, con poliéster de exterior o con imprimación rica en zinc.'),
                     ('Cerrajería y construcción', 'Barandillas, cierres, naves y estructuras en acero o galvanizado.'),
                 ]},
                {'h2': 'Comarcas e industria', 'p': ['Para quién pintamos en cada comarca:'], 'data': [('Burgos (Villalonquéjar)', 'Automoción y componentes, alimentación'), ('Miranda de Ebro', 'Química, ferrocarril y logística'), ('Bureba (Briviesca)', 'Industria auxiliar y agroalimentaria'), ('Merindades (Medina de Pomar)', 'Agroalimentaria y maquinaria agrícola')]},
                {'h2': 'Fotos tipo', 'gallery': gallery('es', SEC_AUTOMOCION, SEC_AGRICOLA, SEC_SOLDADURA, SEC_ESTRUCTURA), 'gallery_cap': GAL_CAP['es']},
                {'h2': 'Cómo trabajamos con empresas burgalesas', 'steps': HOW['es']},
                {'h2': 'A qué distancia estamos', 'p': ['Distancias por carretera desde la planta de Legutio, aproximadas:'],
                 'data': km([('Miranda de Ebro', 47, 38), ('Briviesca', 87, 64), ('Medina de Pomar', 110, 103), ('Burgos', 129, 92)])},
                {'h2': 'Frío, hielo y sal en la carretera', 'p': [
                    'El interior de Burgos tiene inviernos fríos y carreteras con sal de deshielo. Para piezas a la intemperie que no estén cerca de esas carreteras, un poliéster de exterior suele bastar: es un ambiente C2 o C3 según la ISO 12944-2.',
                    'Para maquinaria que trabaja en el campo, equipos junto a carreteras salinizadas o estructuras en zonas industriales agresivas, recomendamos imprimación rica en zinc bajo el poliéster: nuestro sistema C4-H, con el sello en proceso de homologación.',
                ]},
            ],
            'faq': FAQ_COMMON['es'] + [
                ('¿Os compensa una pieza suelta desde Burgos?', 'Sí, pintamos desde una sola pieza. Lo que conviene es agrupar envíos para que el transporte te salga a cuenta: si nos dices cuántas piezas tienes en el mes, te ayudamos a planificar las entregas.'),
            ],
        },
    },
    # ================================================================== NAVARRA
    {
        'key': 'navarra', 'area': 'Navarra',
        'img': 'svc-termolacado', 'img_w': 1200, 'img_h': 800,
        'es': {
            'slug': 'termolacado-navarra-pamplona/',
            'title': 'Termolacado para Navarra y Pamplona | JomaPaint',
            'description': 'Pintura en polvo al horno para empresas de Navarra: Altsasu a 40 minutos de Legutio y Pamplona a una hora y cuarto. Presupuesto en 24 h y plazo de una semana.',
            'og_title': 'Termolacado para Navarra y Pamplona · JomaPaint',
            'name': 'Termolacado para Navarra y Pamplona', 'crumb': 'Navarra', 'service_type': 'Termolacado (pintura en polvo)',
            'kicker': 'Pintura en polvo para Navarra',
            'h1': 'Termolacado para Navarra y Pamplona',
            'lead': 'Altsasu/Alsasua está a 40 minutos de Legutio por la A-1 y Pamplona, a una hora y cuarto por la A-10. Pintamos piezas y estructuras para la industria navarra, con presupuesto firme en 24 h y plazo estándar de una semana.',
            'img_alt': 'Pintura en polvo de color naranja sobre fondo negro', 'img_cap': 'Pintura en polvo',
            'facts': FACTS['es']('54 km', 'Unos 40 min a Altsasu'),
            'sections': [
                {'h2': 'Para la industria de Navarra', 'p': [
                    'En la Sakana, en la comarca de Pamplona y en Tierra Estella hay automoción y componentes, energías renovables, maquinaria agrícola y agroalimentaria, y talleres de metal y carpintería metálica.',
                    'La Sakana es la parte de Navarra más cercana a nuestra planta: de Altsasu a Legutio hay unos 40 minutos.',
                ],
                 'cards': [
                     ('Automoción y componentes', 'Soportes, bastidores, utillaje y protecciones, en serie y con el mismo acabado lote a lote. No pintamos piezas que exijan la homologación del fabricante del vehículo.'),
                     ('Renovables y bienes de equipo', 'Soportes, armarios, carenados y estructuras auxiliares que van al exterior, con el sistema adecuado al ambiente.'),
                     ('Maquinaria agrícola y metal', 'Chasis, protecciones, piezas de máquina, barandillas y estructuras en acero o galvanizado.'),
                 ]},
                {'h2': 'Comarcas e industria', 'p': ['Para quién pintamos en cada comarca:'], 'data': [('Pamplona (Landaben)', 'Automoción y componentes'), ('Cuenca de Pamplona', 'Renovables, eólica e ingeniería'), ('Sakana (Altsasu)', 'Metal y fundición'), ('Ribera (Tudela)', 'Agroalimentaria y maquinaria agrícola')]},
                {'h2': 'Fotos tipo', 'gallery': gallery('es', SEC_AUTOMOCION, SEC_EOLICA, SEC_AGRICOLA, SEC_SOLDADURA), 'gallery_cap': GAL_CAP['es']},
                {'h2': 'Cómo trabajamos con empresas navarras', 'steps': HOW['es']},
                {'h2': 'A qué distancia estamos', 'p': ['Distancias por carretera desde la planta de Legutio, aproximadas:'],
                 'data': km([('Altsasu/Alsasua', 54, 40), ('Lizarra/Estella', 93, 78), ('Pamplona/Iruña', 103, 75), ('Tudela', 196, 133)])},
                {'h2': 'La pintura según dónde vaya la pieza', 'p': [
                    'El exterior en la Navarra interior suele ser un ambiente C2 o C3 según la ISO 12944-2, y ahí un poliéster de exterior sobre un buen pretratamiento es suficiente.',
                    'Para maquinaria que trabaja en el campo, equipos junto a carreteras con sal de deshielo o estructuras en entornos industriales agresivos, recomendamos imprimación rica en zinc bajo el poliéster: nuestro sistema C4-H, con el sello en proceso de homologación.',
                ]},
            ],
            'faq': FAQ_COMMON['es'] + [
                ('¿Podéis igualar el color de una pieza que ya tenemos?', 'Sí, si es un RAL o una referencia de fabricante de polvo. Si no tiene referencia, tráenos una muestra y buscamos el polvo más cercano; te enviamos una placa pintada para que lo apruebes antes de pintar el pedido.'),
            ],
        },
    },
    # ================================================================== LA RIOJA
    {
        'key': 'rioja', 'area': 'La Rioja',
        'img': 'svc-aluminio', 'img_w': 1200, 'img_h': 800,
        'es': {
            'slug': 'termolacado-la-rioja-logrono/',
            'title': 'Termolacado para La Rioja y Logroño | JomaPaint',
            'description': 'Pintura en polvo al horno para empresas de La Rioja: Haro a 45 minutos de Legutio y Logroño a una hora y cuarto. Presupuesto en 24 h y plazo estándar de una semana.',
            'og_title': 'Termolacado para La Rioja y Logroño · JomaPaint',
            'name': 'Termolacado para La Rioja y Logroño', 'crumb': 'La Rioja', 'service_type': 'Termolacado (pintura en polvo)',
            'kicker': 'Pintura en polvo para La Rioja',
            'h1': 'Termolacado para La Rioja y Logroño',
            'lead': 'Haro está a 45 minutos de nuestra planta de Legutio y Logroño, a una hora y cuarto. Pintamos piezas, estructuras y carpintería metálica para la industria riojana, con presupuesto firme en 24 h y plazo estándar de una semana.',
            'img_alt': 'Perfil de aluminio extruido en primer plano, sobre fondo oscuro', 'img_cap': 'Perfil de aluminio',
            'facts': FACTS['es']('57 km', 'Unos 45 min a Haro'),
            'sections': [
                {'h2': 'Para la industria de La Rioja', 'p': [
                    'En La Rioja Alta y en el entorno de Logroño hay maquinaria para bodega y agroalimentaria, metal y componentes, mueble y carpintería metálica, y construcción.',
                    'Haro y Santo Domingo de la Calzada están a menos de una hora de Legutio.',
                ],
                 'cards': [
                     ('Maquinaria de bodega y agroalimentaria', 'Bastidores, soportes, protecciones y estructuras de máquina en acero. En contacto con alimentos o en zonas de lavado, cuéntanoslo y valoramos el polvo adecuado.'),
                     ('Carpintería metálica y construcción', 'Perfiles y chapa de aluminio, barandillas, cierres y pérgolas en acero o galvanizado.'),
                     ('Mueble y mobiliario', 'Estructuras de mesas, sillas y estanterías, en el RAL y el acabado que pidas: mate, satinado o texturado.'),
                 ]},
                {'h2': 'Comarcas e industria', 'p': ['Para quién pintamos en cada comarca:'], 'data': [('Logroño', 'Metal, componentes y carpintería metálica'), ('Haro y Rioja Alta', 'Bodegas y su maquinaria'), ('Calahorra y Rioja Baja', 'Conservas, agroalimentaria y maquinaria agrícola')]},
                {'h2': 'Fotos tipo', 'gallery': gallery('es', SEC_BODEGA, SEC_AGRICOLA, SEC_TALLER, SEC_ESTRUCTURA), 'gallery_cap': GAL_CAP['es']},
                {'h2': 'Cómo trabajamos con empresas riojanas', 'steps': HOW['es']},
                {'h2': 'A qué distancia estamos', 'p': ['Distancias por carretera desde la planta de Legutio, aproximadas:'],
                 'data': km([('Haro', 57, 44), ('Santo Domingo de la Calzada', 77, 61), ('Logroño', 105, 75), ('Calahorra', 149, 101), ('Arnedo', 154, 108)])},
                {'h2': 'La pintura según dónde vaya la pieza', 'p': [
                    'El exterior en La Rioja suele ser un ambiente C2 o C3 según la ISO 12944-2. Para eso basta un poliéster de exterior bien curado; para mobiliario y carpintería, con la carta RAL y el brillo que elijas.',
                    'Si la pieza va a estar en una zona de lavado, en una bodega con humedad constante o en un entorno industrial agresivo, recomendamos imprimación rica en zinc bajo el poliéster: nuestro sistema C4-H, con el sello en proceso de homologación.',
                ]},
            ],
            'faq': FAQ_COMMON['es'] + [
                ('¿Pintáis aluminio además de acero?', 'Sí. El aluminio lleva su propio pretratamiento, distinto del acero, para que el polvo agarre. Pintamos perfiles, chapa y piezas de aluminio en toda la carta RAL.'),
            ],
        },
    },
]

# Texto del enlace a cada zona en la portada, por idioma
LINK_NAMES = {
    'es': {'alava': 'Vitoria-Gasteiz y Álava', 'gipuzkoa': 'Gipuzkoa y Donostia', 'bizkaia': 'Bizkaia y Bilbao', 'burgos': 'Burgos y Miranda', 'navarra': 'Navarra y Pamplona', 'rioja': 'La Rioja y Logroño'},
    'eu': {'alava': 'Vitoria-Gasteiz eta Araba', 'gipuzkoa': 'Gipuzkoa eta Donostia', 'bizkaia': 'Bizkaia eta Bilbo'},
}


# ---------- Francés (Álava, Gipuzkoa, Bizkaia), generado desde el castellano ----------
import copy as _copy  # noqa: E402
import re as _re  # noqa: E402
import zones_fr as _ZF  # noqa: E402

_KEEP = {'slug', 'img', 'img_w', 'img_h'}


def _to_fr(obj, missing, key=None):
    if isinstance(obj, str):
        if key in _KEEP or not any(c.isalpha() for c in obj) or _re.fullmatch(r'[\d\s·kmhin]+', obj) or obj.endswith('.webp'):
            return obj
        if obj not in _ZF.FR:
            missing.append(obj)
            return obj
        return _ZF.FR[obj]
    if isinstance(obj, dict):
        return {k: _to_fr(v, missing, k) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        out = [_to_fr(v, missing) for v in obj]
        return tuple(out) if isinstance(obj, tuple) else out
    return obj


_missing = []
for _z in ZONES:
    if _z['key'] in _ZF.SLUGS:
        _fr = _to_fr(_copy.deepcopy(_z['es']), _missing)
        _fr['slug'] = _ZF.SLUGS[_z['key']]
        _z['fr'] = _fr
LINK_NAMES['fr'] = {k: _ZF.FR[LINK_NAMES['es'][k]] for k in _ZF.SLUGS}
if _missing:
    raise SystemExit('zones_fr: faltan traducciones:\n  ' + '\n  '.join(sorted(set(_missing))))
