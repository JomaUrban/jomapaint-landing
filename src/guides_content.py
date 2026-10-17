# -*- coding: utf-8 -*-
"""Página «Certificaciones y normas de la pintura en polvo» (ES, EU, FR).

Borrador. Misma estructura que una entrada de services.py (ver la cabecera de
ese archivo para los tipos de bloque). Solo datos contrastados en la
investigación (research/normas.md, proveedores.md, competencia-marine.md).
Lo pendiente va con PH('[...]') y queda fuera de FAQPage: 'faq_n' cuenta las
preguntas iniciales con respuesta verificada.

Notas de fuente:
- Umbrales de brillo de las clases QUALICOAT y espesores mínimos: especificación
  técnica QUALICOAT 2023 (copia pública); la edición vigente es la 26.ª (2026).
- Horas QUALISTEELCOAT por categoría: especificación v4.2 (2021) citada por
  Kunce et al.; C5-H coincide con la v4.3 (2025).
- Horas ISO 12944-6 y rangos de durabilidad: fuentes secundarias concordantes.
"""
from content import PH

CERT = {
    'key': 'certificaciones',
    'img': None,
    # ================================================================== ES
    'es': {
        'slug': 'certificaciones-normas-pintura-polvo/',
        'title': 'Certificaciones y normas de la pintura en polvo | JomaPaint',
        'description': 'QUALICOAT, QUALISTEELCOAT, GSB, ISO 9001 e ISO 12944 en pintura en polvo: qué asegura cada sello y norma, cómo se verifica y qué pedir en un pliego.',
        'og_title': 'Certificaciones y normas de la pintura en polvo · JomaPaint',
        'name': 'Certificaciones y normas de la pintura en polvo', 'crumb': 'Certificaciones y normas', 'service_type': None,
        'kicker': 'Guía técnica · JomaPaint, Legutio (Álava)',
        'h1': 'Certificaciones y normas de la pintura en polvo',
        'lead': 'Qué es cada sello y cada norma, qué te asegura y cómo se comprueba: ensayos, horas y criterios. Para leer un pliego, especificar un sistema o comparar ofertas con datos.',
        'img_alt': '',
        'img_cap': '',
        'facts': [('Esquemas', 'QUALICOAT · QUALISTEELCOAT · GSB', 'Certifican al lacador'), ('Ambientes', 'C1 a CX', 'ISO 12944-2:2017'), ('Durabilidad', 'L · M · H · VH', 'No es una garantía')],
        'sections': [
            # ---------------------------------------------------------- 1
            {'h2': 'Certificado, homologación y norma: no es lo mismo', 'p': [
                'Un certificado lo concede un tercero que inspecciona al lacador y ensaya sus piezas. Es el caso de QUALICOAT, QUALISTEELCOAT y GSB. Va ligado a una planta o a un sistema, tiene número y se mantiene con inspecciones periódicas.',
                'Una homologación se refiere a un producto: un polvo, un pretratamiento o un sistema de capas que el esquema ha ensayado. Que el polvo esté homologado no convierte al lacador en certificado.',
                'Una norma ISO o EN define ensayos y requisitos. No es un sello: su cumplimiento se demuestra con informes de ensayo, con laboratorio y número.',
            ],
             'table': {
                 'cols': ['Esquema', 'Aluminio', 'Acero y galvanizado', 'Certifica el lacado'],
                 'rows': [
                     ('QUALICOAT', [('yes', 'Sí'), ('no', 'No'), ('yes', 'Sí, por planta')]),
                     ('QUALISTEELCOAT', [('no', 'No'), ('yes', 'Sí'), ('yes', 'Sí, por sistema')]),
                     ('GSB', [('yes', 'Sí'), ('yes', 'Sí'), ('yes', 'Sí: sello Standard, Master o Premium')]),
                     ('ISO 9001 · ISO 14001', [('mid', 'Según el alcance'), ('mid', 'Según el alcance'), ('no', 'No: certifican la gestión')]),
                     ('Normas ISO y EN', [('mid', 'Según la norma'), ('mid', 'Según la norma'), ('no', 'No: definen ensayos')]),
                 ],
                 'note': 'Un sello solo vale con su número de licencia y dentro de su vigencia.',
             }},
            # ---------------------------------------------------------- 2
            {'h2': 'QUALICOAT: lacado de aluminio para arquitectura', 'p': [
                'QUALICOAT es un sello de calidad para la pintura en polvo o líquida sobre aluminio para arquitectura: perfiles, fachadas, carpintería. Es una marca registrada. La especificación vigente es la 26.ª edición, válida desde el 1 de enero de 2026.',
                'Qué te asegura: que el pretratamiento, el polvo, el curado y el producto acabado cumplen requisitos definidos, y que lo verifica un tercero con laboratorios acreditados según ISO/IEC 17025.',
                'En España lo gestiona la Asociación Española del Aluminio y Tratamientos de Superficie (AEA).',
            ],
             'cards': [
                 ('Licencia del lacador', 'Se concede por planta. Antes se inspeccionan la línea, el laboratorio propio, el proceso y el producto acabado. Después siguen inspecciones periódicas, con ensayos de corrosión. El lacador controla en su laboratorio, entre otros, brillo (ISO 2813), espesor (ISO 2360), adherencia (ISO 2409, resultado 0), plegado (ISO 1519) e impacto (ISO 6272). Espesor mínimo: 60 µm en una capa (polvos de clase 1, 1.5 y 2) y 110 µm en dos; ninguna medida por debajo del 80 % del mínimo.'),
                 ('Homologación del polvo', 'Cada polvo homologado tiene un código P-No. y una clase. Para homologarlo se ensaya, entre otros, con xenón (ISO 16474-2, 1.000 h, clases 1 a 2), niebla salina acética (ISO 9227 AASS, 1.000 h; 2.000 h en clase 3), condensación (ISO 6270-2, 1.000 h; 2.000 h en clase 3) y SO₂ (ISO 22479, 24 ciclos).'),
                 ('SEASIDE', 'Aval adicional para ambiente marino. Exige un pretratamiento reforzado, con un ataque de al menos 2,0 g/m² frente a 1,0 g/m² del estándar, y un ensayo de corrosión filiforme (ISO 4623-2, 1.000 h): filamento más largo ≤ 4 mm y media ≤ 2 mm. QUALICOAT lo recomienda, o el pre-anodizado, a partir de C4, y sobre todo en C5 y CX.'),
             ],
             'note': 'Estado en JomaPaint: ' + PH('[a confirmar]')},
            # ---------------------------------------------------------- 3
            {'h2': 'Clases de polvo QUALICOAT: años en Florida y brillo', 'p': [
                'La clase de un polvo indica cuánto conserva el brillo y el color al sol. Se comprueba con probetas expuestas en Florida (ISO 2810), orientadas al sur: con 5° de inclinación en las clases 1 a 2 y con 45° en la clase 3.',
                'Al final de cada periodo se miden el brillo residual y la variación de color, que debe quedar dentro de los límites fijados para cada RAL.',
            ],
             'data': [
                 ('Clase 1', '1 año en Florida · brillo residual ≥ 50 %'),
                 ('Clase 1.5', '2 años · ≥ 65 % tras 1 año y ≥ 50 % tras 2'),
                 ('Clase 2', '3 años · ≥ 75 %, 60 % y 50 % tras 1, 2 y 3 años'),
                 ('Clase 3', '10 años · ≥ 80 % tras 3 años y ≥ 50 % tras 10'),
             ],
             'note': 'Umbrales de la especificación técnica de 2023. La edición vigente es la 26.ª, de 2026.'},
            # ---------------------------------------------------------- 4
            {'h2': 'QUALISTEELCOAT: lacado de acero y acero galvanizado', 'p': [
                'QUALISTEELCOAT es el sello equivalente para el acero. Certifica el lacado con pintura en polvo o líquida sobre acero desnudo o con zinc: galvanizado en caliente o en continuo, electrocincado, metalizado o sherardizado. En España lo gestiona la AEA.',
                'La licencia se concede por sistema: un pretratamiento, unas capas y una categoría de corrosividad concretos. El código indica el sustrato y el número de capas: ST (acero), HD (galvanizado en caliente), SZ (galvanizado en continuo), MS (metalizado) y STEC (acero con cataforesis). Por ejemplo, STEC3 es cataforesis, imprimación y acabado.',
                'Qué te asegura: que el sistema ha superado los ensayos de una categoría y una durabilidad concretas, y que la planta se inspecciona. Hace de puente entre ISO 12944, pensada para pintura líquida, y la pintura en polvo. La H significa durabilidad alta: de 15 a 25 años según ISO 12944-1.',
            ],
             'list': [
                 'El lacador elige la categoría de corrosividad y el sistema que quiere certificar.',
                 'Laboratorio propio, materiales homologados y autocontrol: espesor, brillo, adherencia, impacto, agua hirviendo, niebla salina, rayado y dureza.',
                 'Inspección de concesión y, después, dos inspecciones al año sin aviso.',
                 'Criterio en la incisión tras la niebla salina: ≤ 1 mm, más estricto que el 1,5 mm de ISO 12944-6. Sobre galvanizado se admite una delaminación de hasta 8 mm.',
                 'Además: xenón (ISO 16474-2, 1.000 h) y un año de exposición natural (ISO 2810).',
             ],
             'data': [
                 ('C2-H', 'Humedad ISO 6270-2: 120 h · Niebla salina ISO 9227: 240 h'),
                 ('C3-H', 'Humedad: 240 h · Niebla salina: 480 h'),
                 ('C4-H', 'Humedad: 480 h · Niebla salina: 720 h'),
                 ('C5-H', 'Humedad: 720 h · Niebla salina: 1.440 h, o 1.680 h de ensayo cíclico'),
             ],
             'note': 'Estado en JomaPaint: ' + PH('[a confirmar]')},
            # ---------------------------------------------------------- 5
            {'h2': 'GSB: el sello alemán para aluminio y acero', 'p': [
                'GSB International es una asociación alemana de calidad del lacado. Controla toda la cadena: productos de pretratamiento, pinturas y lacadores. Su normativa es GSB AL 631 para aluminio y GSB ST 663 para acero y galvanizado; la edición vigente es la de enero de 2026.',
                'Clasifica por separado las pinturas y los lacadores. Como en QUALICOAT, usar una pintura homologada por GSB no basta para que el lacado sea conforme.',
            ],
             'cards': [
                 ('Pinturas: Florida 1, 3, 5 y 10', 'Años de exposición en Florida que supera la pintura, con un brillo residual de al menos el 50 % y color estable. GSB las describe como resistencia UV estándar, alta, muy alta y extremadamente alta.'),
                 ('Lacadores: Standard, Master y Premium', 'Tres sellos. En acero se distinguen por la niebla salina que supera el sistema bicapa: 480 h (Standard), 720 h (Master) y 1.440 h (Premium); en monocapa, 480 h en los tres. Criterios: delaminación ≤ 3 mm en acero y ≤ 8 mm en galvanizado, sin ampollas. Premium exige además trazabilidad completa de cada pedido.'),
                 ('Sea Proof y Sea Proof Plus', 'Sellos adicionales para aluminio en costa: Sea Proof para C4 y Sea Proof Plus para C5, con pre-anodizado. Se ensayan con corrosión filiforme y niebla salina acética: una vez al año Sea Proof y dos veces Sea Proof Plus. Para ser Premium en aluminio hace falta uno de los dos.'),
                 ('Cómo se verifica', 'Una auditoría con aviso y otra sin aviso, con toma de muestras para ensayos de corrosión. Después, dos ensayos de prolongación al año, sin aviso. Si un ensayo falla: requisitos adicionales, repetición, rebaja de sello o retirada.'),
             ]},
            # ---------------------------------------------------------- 6
            {'h2': 'ISO 9001 e ISO 14001: sistemas de gestión', 'p': [
                'Certifican cómo se gestiona la empresa, no cómo se comporta un recubrimiento. ISO 9001 trata la gestión de la calidad; ISO 14001, la gestión ambiental. Cada certificado cubre un alcance concreto, que figura por escrito.',
                'No los emite ISO, sino entidades de certificación externas, preferiblemente acreditadas; en España, por ENAC. Se mantienen con auditorías de seguimiento.',
                'El certificado ISO 9001:2015 de Joma cubre el diseño, la fabricación y la comercialización de cajas de caudales, armarios de llaves, buzones, botiquines, paneles de anuncios y cajas metálicas. No incluye la pintura para terceros.',
            ],
             'cards': [
                 ('ISO 9001 · calidad', 'Procesos documentados, trazabilidad, tratamiento de no conformidades y reclamaciones, y mejora continua.'),
                 ('ISO 14001 · medio ambiente', 'Control de los aspectos ambientales: efluentes del pretratamiento, residuos de polvo y energía de los hornos.'),
             ],
             'data': [
                 ('Edición vigente de ISO 9001', 'ISO 9001:2026, publicada en septiembre de 2026'),
                 ('Edición vigente de ISO 14001', 'ISO 14001:2026, publicada en abril de 2026'),
                 ('Certificados ISO 9001:2015', 'Transición hasta el 30-09-2029'),
             ],
             'note': 'Estado en JomaPaint: ' + PH('[ISO 9001 e ISO 14001 para la pintura a terceros: a confirmar]')},
            # ---------------------------------------------------------- 7
            {'h2': 'ISO 12944, parte por parte', 'p': [
                'ISO 12944 es la norma de referencia para proteger estructuras de acero con sistemas de pintura. Define los ambientes, la durabilidad, la preparación, los sistemas, los ensayos y la ejecución.',
                'Su alcance son las estructuras de acero al carbono de 3 mm o más, con pinturas que secan o curan a temperatura ambiente. Deja fuera los recubrimientos en polvo y los esmaltes al horno; la parte 7 excluye expresamente la aplicación de polvo.',
                'Por eso un sistema en polvo no «cumple ISO 12944»: se ensaya según sus métodos (parte 6) y se describe con sus categorías (parte 2), o se acredita con un esquema pensado para polvo (QUALISTEELCOAT, GSB ST 663) o con la norma alemana DIN 55633.',
            ],
             'data': [
                 ('Parte 1 · 2017', 'Introducción, términos y durabilidad (L, M, H, VH).'),
                 ('Parte 2 · 2017', 'Clasificación de ambientes: C1 a CX e Im1 a Im4.'),
                 ('Parte 3 · 2017', 'Criterios de diseño. Pide grado P3 (ISO 8501-3) para durabilidad alta y muy alta en C4, C5, CX e Im.'),
                 ('Parte 4 · 2017', 'Tipos de superficie y su preparación.'),
                 ('Parte 5 · 2019', 'Sistemas de pintura: número de capas y espesor mínimo. No cubre CX ni Im4.'),
                 ('Parte 6 · 2018', 'Ensayos de laboratorio para C2 a C5 e Im1 a Im3. Sus resultados no dan la durabilidad de forma exacta.'),
                 ('Parte 7 · 2017', 'Ejecución y supervisión de los trabajos de pintura. Excluye la aplicación de polvo.'),
                 ('Parte 8 · 2017', 'Redacción de especificaciones para obra nueva y mantenimiento.'),
                 ('Parte 9 · 2018', 'Sistemas para offshore y estructuras similares: CX e Im4. Sustituye a ISO 20340.'),
             ],
             'note': 'Toda la serie está en revisión. Mientras tanto, siguen vigentes las ediciones indicadas.'},
            # ---------------------------------------------------------- 8
            {'h2': 'Categorías de corrosividad: de C1 a CX, e Im1 a Im4', 'p': [
                'ISO 12944-2 clasifica el ambiente por lo que corroe: la pérdida de espesor de una probeta de acero al carbono en su primer año de exposición. Los valores coinciden con los de ISO 9223.',
            ],
             'data': [
                 ('C1 · muy baja', 'Interior calefactado con aire limpio: oficinas, tiendas, colegios. Acero: ≤ 1,3 µm el primer año.'),
                 ('C2 · baja', 'Exterior rural poco contaminado; interior sin calefacción con condensación: almacenes, polideportivos. Más de 1,3 a 25 µm.'),
                 ('C3 · media', 'Urbano e industrial con SO₂ moderado; costa de baja salinidad; salas de producción húmedas. Más de 25 a 50 µm.'),
                 ('C4 · alta', 'Industrial y costa de salinidad moderada; plantas químicas, piscinas. Más de 50 a 80 µm.'),
                 ('C5 · muy alta', 'Industrial muy húmedo y agresivo; costa de alta salinidad. Más de 80 a 200 µm.'),
                 ('CX · extrema', 'Offshore, industrial extremo, clima tropical y subtropical. Más de 200 a 700 µm.'),
                 ('Im1', 'Agua dulce.'),
                 ('Im2', 'Agua de mar o salobre, sin protección catódica.'),
                 ('Im3', 'Suelo.'),
                 ('Im4', 'Agua de mar o salobre, con protección catódica. Nueva en 2017.'),
             ]},
            # ---------------------------------------------------------- 9
            {'h2': '¿C5-M o C5? Lo que cambió en 2017', 'p': [
                'En la edición de 1998, C5 tenía dos variantes con la misma pérdida de acero: C5-I, industrial, y C5-M, marina, que incluía la costa y el offshore de alta salinidad.',
                'En la edición de 2017, las dos se unificaron en C5, que cubre la industria húmeda y agresiva y la costa de alta salinidad. El offshore pasó a la nueva CX.',
                'Hoy la categoría se escribe junto a la durabilidad: C4-H, C5-M, C5-VH. Así, «C5-M» significa «C5 con durabilidad media», de 7 a 15 años: es la clasificación del sistema Marine. En un pliego, mejor escribir la categoría, la letra de durabilidad y la edición de la norma: por ejemplo, C5-M según ISO 12944-2:2017.',
                'La durabilidad (ISO 12944-1) se expresa en cuatro clases. No es un plazo de garantía, sino un dato para planificar. En 1998 las clases eran L (2 a 5 años), M (5 a 15) y H (más de 15).',
            ],
             'data': [
                 ('L · baja', 'Hasta 7 años'),
                 ('M · media', '7 a 15 años'),
                 ('H · alta', '15 a 25 años'),
                 ('VH · muy alta', 'Más de 25 años. Nueva en 2017.'),
             ],
             'note': 'La durabilidad no es una garantía.'},
            # ---------------------------------------------------------- 10
            {'h2': 'Ensayos de ISO 12944-6: horas por categoría', 'p': [
                'La parte 6 fija los ensayos de laboratorio para cada categoría y durabilidad. La letra tras la categoría es la durabilidad: C5-M es C5 con durabilidad media. Se ensayan dos juegos de probetas: uno en condensación (ISO 6270-1) y otro en niebla salina neutra (ISO 9227). Para las exigencias más altas hay un ensayo cíclico.',
                'El ciclo dura una semana: 72 h de UV y condensación (ISO 16474-3), 72 h de niebla salina y 24 h a −20 °C.',
                'Después se evalúan ampollas, óxido, agrietamiento y descamación (ISO 4628-2 a -5), el avance de la corrosión desde la incisión (ISO 4628-8) y la adherencia (ISO 2409 o ISO 4624).',
            ],
             'data': [
                 ('C3-H', 'Condensación 240 h · niebla salina 480 h'),
                 ('C4-H', 'Condensación 480 h · niebla salina 720 h'),
                 ('C5-M', 'Condensación 480 h · niebla salina 720 h'),
                 ('C5-H', 'Condensación 720 h · niebla salina 1.440 h, o 1.680 h de ensayo cíclico'),
                 ('C5-VH', '2.688 h de ensayo cíclico (16 ciclos)'),
                 ('CX (ISO 12944-9)', '4.200 h de ensayo cíclico (25 ciclos)'),
             ],
             'note': 'Hacen falta los dos ensayos: las horas de niebla salina, solas, no acreditan una durabilidad.'},
            # ---------------------------------------------------------- 11
            {'h2': 'Ensayos de corrosión y de envejecimiento', 'p': [
                'Son ensayos acelerados en cámara. Sirven para controlar un sistema concreto frente a una referencia y para comprobar que cumple lo pactado. Sus horas no se convierten en años de servicio.',
            ],
             'cards': [
                 ('Niebla salina · ISO 9227', 'Probetas, normalmente con una incisión hasta el metal, en una niebla continua de agua salada. Tres variantes: neutra (NSS: 35 °C, cloruro sódico al 5 %), acética (AASS: la que pide QUALICOAT para aluminio) y acética con cobre (CASS, a 50 °C). La norma advierte que no sirve para ordenar materiales ni para predecir la resistencia a largo plazo. Edición vigente: 2022.'),
                 ('Humedad · ISO 6270', 'Agua que condensa sobre la probeta. La parte 1 condensa por una cara de forma continua; la parte 2 expone la probeta en cámara, con clima constante (40 °C y 100 % de humedad) o alternante. Detecta ampollas y pérdidas de adherencia.'),
                 ('SO₂ (Kesternich) · ISO 22479', 'Humedad con dióxido de azufre, que simula atmósferas industriales. Ciclos de 24 h: 8 h a 40 °C con SO₂ y 16 h a temperatura ambiente con la cámara ventilada. Sustituye a ISO 3231 e ISO 6988, retiradas.'),
                 ('Xenón · ISO 16474-2', 'Luz de lámpara de xenón, parecida a la del sol, con ciclos de agua. QUALICOAT la usa 1.000 h para homologar polvos. Sustituyó a ISO 11341.'),
                 ('UV fluorescente · ISO 16474-3', 'Lámparas UV, por ejemplo UVA-340, con condensación. Forma parte del ensayo cíclico de ISO 12944-6 y -9. No reproduce todo el espectro solar.'),
                 ('Exposición natural · ISO 2810', 'Probetas al aire libre, directamente o tras vidrio. Es la base del «ensayo de Florida» de QUALICOAT y GSB: la verificación real del brillo y el color con los años.'),
             ],
             'note': 'Un informe de ensayo serio indica norma y edición, laboratorio, número, probetas, horas, criterios y resultado.'},
            # ---------------------------------------------------------- 12
            {'h2': 'Ensayos de la película: adherencia, espesor, brillo y color', 'p': [
                'Son los controles que se hacen sobre la propia capa, en planta o en laboratorio.',
            ],
             'data': [
                 ('Corte por enrejado · ISO 2409', 'Se corta una cuadrícula hasta el metal, se aplica cinta y se mira cuánto se suelta. Clases de 0 (sin desprendimiento) a 5. QUALICOAT exige 0. No sirve por encima de 250 µm ni en texturados.'),
                 ('Tracción (pull-off) · ISO 4624', 'Se pega una sufridera y se arranca: da la adherencia en MPa. ISO 12944-9 pide al menos 5 MPa antes del envejecimiento.'),
                 ('Espesor · ISO 2808 e ISO 2360', 'ISO 2808 recoge los métodos de medida de la película, también del polvo sin curar; ISO 2360, la medida por corrientes inducidas sobre metal no magnético, como el aluminio. Sobre superficies chorreadas, el muestreo y la aceptación siguen ISO 19840.'),
                 ('Brillo · ISO 2813', 'Se mide a 20°, 60° u 85°, en unidades de brillo (GU). QUALICOAT agrupa los polvos en tres categorías a 60°: mate (0–30 GU), satinado (31–70) y brillo (71–100).'),
                 ('Plegado · ISO 1519', 'Se dobla la probeta pintada sobre un mandril cilíndrico y se revisa si la película se agrieta o se despega.'),
                 ('Embutición · ISO 1520', 'Se deforma la chapa pintada con un punzón hasta formar una cúpula y se revisa la película.'),
                 ('Impacto · ISO 6272', 'Una masa cae sobre la probeta y se revisa si la película se agrieta o se despega.'),
                 ('Dureza Buchholz · ISO 2815', 'Un indentador de peso fijo deja una huella; su longitud da la dureza.'),
                 ('Degradación · ISO 4628', 'Cómo se califica el daño tras un ensayo: ampollas (-2), óxido (-3), agrietamiento (-4), descamación (-5), corrosión desde la incisión (-8) y filiforme (-10).'),
                 ('Color · ISO 11664-4', 'Diferencia de color ΔE entre la pieza y la referencia, en el espacio CIELAB. La antigua ISO 7724 está retirada desde 2013.'),
             ],
             'note': 'Controles que hacemos en planta: ' + PH('[a confirmar]')},
            # ---------------------------------------------------------- 13
            {'h2': 'Preparación de superficie: ISO 8501 e ISO 8503', 'p': [
                'Buena parte de la vida de un sistema depende de la limpieza y la rugosidad del acero antes de pintar. Estas normas permiten pactar grados que se pueden comprobar.',
            ],
             'data': [
                 ('ISO 8501-1', 'Grados de óxido del acero de partida y grados de preparación: Sa 1 a Sa 3 por chorreado y St por limpieza manual o mecánica. Sa 2½ es metal casi blanco; Sa 3, metal blanco. Se describen con fotografías.'),
                 ('ISO 8501-3', 'Grados P1, P2 y P3 para soldaduras, cantos y otras imperfecciones. Edición de 2025. ISO 12944-3 pide P3 para durabilidad alta y muy alta en C4, C5 y CX, y EN 1090-2 también los usa.'),
                 ('ISO 8503-1', 'Comparadores para clasificar el perfil de rugosidad tras el chorreado con granalla o corindón.'),
             ],
             'note': 'Preparación en JomaPaint: ' + PH('[chorreado y grado Sa: a confirmar]')},
            # ---------------------------------------------------------- 14
            {'h2': 'Normas EN de producto y de ejecución', 'p': [
                'Normas europeas que aparecen en los pliegos de construcción. Son normas, no sellos: se cumplen y se demuestran con ensayos y documentos.',
            ],
             'data': [
                 ('EN 13438', 'Requisitos de comportamiento de la pintura en polvo sobre acero galvanizado en caliente o sherardizado, para construcción. No regula el proceso de lacado.'),
                 ('EN 15773', 'Aplicación industrial de polvo sobre acero galvanizado en caliente o sherardizado: los sistemas dúplex. Fija qué deben acordar cliente, galvanizador, proveedor químico y lacador, y la calidad exigida al galvanizado. Edición de 2018.'),
                 ('EN ISO 1461', 'Galvanizado en caliente de piezas fabricadas: propiedades y ensayos. No cubre lo que se aplica encima. Edición de 2022.'),
                 ('EN 12206-1', 'Lacado en polvo sobre aluminio para arquitectura: pretratamiento, polvo, proceso y producto acabado. Edición de 2021.'),
                 ('EN 1090-2', 'Ejecución de estructuras de acero, incluido el tratamiento de superficie. Relaciona el grado de preparación P1 a P3 con la vida prevista de la protección y la categoría de corrosividad, que indica el proyectista.'),
                 ('DIN 55633', 'Norma alemana para proteger el acero con sistemas en polvo; sus categorías remiten a ISO 12944-2. La parte 2 trata los sistemas de cataforesis epoxi y polvo.'),
             ]},
            # ---------------------------------------------------------- 15
            {'h2': 'Ensayos del sistema Marine', 'p': [
                'Marine es el sistema anticorrosión de Joma: pretratamiento por inmersión, cataforesis, imprimación y acabado en pintura en polvo. Su clasificación es C5-M: ambiente C5, como la primera línea de costa, con durabilidad media (7 a 15 años).',
                'No es un sistema certificado: ISO 12944 se escribió para pinturas líquidas y no certifica sistemas en polvo. Por eso cada dato va con su norma, su laboratorio y su número de informe.',
                'Para C5-M, ISO 12944-6 pide 720 h de niebla salina neutra y 480 h de condensación, evaluadas con ISO 4628 y adherencia. Las horas no equivalen a años.',
            ],
             'layers': [
                 ('Pintura en polvo', 'Acabado en el RAL elegido. Tipo de polvo: ' + PH('[poliéster: a confirmar]') + ' · ' + PH('[XX] µm')),
                 ('Imprimación', PH('[Tipo: a confirmar]') + ' · ' + PH('[XX] µm')),
                 ('Cataforesis', 'Imprimación por electrodeposición en toda la superficie · ' + PH('[XX] µm')),
                 ('Sustrato', PH('[Acero, galvanizado o ambos: a confirmar]') + ', pretratado por inmersión'),
             ],
             'data': [
                 ('Niebla salina neutra · UNE-EN ISO 9227', '1.000 h (C5-M pide 720 h) · ' + PH('[informe a confirmar]')),
                 ('Resultado', PH('[ampollas, óxido y avance desde la incisión según ISO 4628]')),
                 ('Condensación · ISO 6270-1', PH('[C5-M pide 480 h: informe a confirmar]')),
                 ('Adherencia · ISO 2409', PH('[clase a confirmar]')),
                 ('Espesor total · ISO 2808', PH('[XX] µm')),
                 ('Laboratorio y n.º de informe', PH('[a confirmar]')),
             ],
             'note': 'Certificación QUALISTEELCOAT del sistema: ' + PH('[a confirmar]')},
            # ---------------------------------------------------------- 16
            {'h2': 'Cómo elegir el sistema según dónde va la pieza', 'p': [
                'Orientación general, a partir de los ambientes de ISO 12944-2. El sistema exacto depende del sustrato, de la durabilidad que pidas y del polvo, y lo fijamos contigo.',
            ],
             'cards': [
                 ('Interior seco · C1', 'Oficinas, tiendas o colegios con calefacción. Basta una capa de polvo; el epoxi-poliéster sirve si la pieza no ve el sol.'),
                 ('Interior con condensación o exterior rural · C2', 'Naves sin calefacción, almacenes, polideportivos; exterior poco contaminado. En exterior, una capa de poliéster.'),
                 ('Urbano o costa de baja salinidad · C3', 'Ciudad, industria con SO₂ moderado, salas de producción húmedas. Poliéster sobre un pretratamiento cuidado; sobre galvanizado, sistema dúplex.'),
                 ('Industrial o costa de salinidad moderada · C4', 'Plantas químicas, piscinas. En acero, imprimación y acabado; en galvanizado, una o dos capas según la durabilidad.'),
                 ('Industria agresiva o costa de alta salinidad · C5', 'En 1998, C5-I y C5-M. Sistemas de varias capas: galvanizado con imprimación y acabado, o cataforesis, imprimación y acabado, como el sistema Marine C5-M. Pide los ensayos del sistema completo.'),
                 ('Offshore, inmersión o enterrado · CX e Im', 'Sistemas específicos, ensayados según ISO 12944-9 (CX, Im4) o ISO 12944-6 (Im1 a Im3). Se estudian caso a caso.'),
             ],
             'note': 'En aluminio para arquitectura, QUALICOAT recomienda pretratamiento SEASIDE o pre-anodizado a partir de C4.'},
            # ---------------------------------------------------------- 17
            {'h2': 'Qué pedir en un pliego o especificación', 'p': [
                'Lo que conviene pedir por escrito a cualquier lacador, también a nosotros:',
            ],
             'list': [
                 'Ambiente y durabilidad: categoría de corrosividad (C1 a CX, Im) y clase de durabilidad (L, M, H o VH), con la edición de la norma. Por ejemplo, C5-H según ISO 12944-2:2017.',
                 'Sustrato: acero; acero galvanizado en caliente, en continuo o electrocincado; o aluminio.',
                 'Preparación: pretratamiento químico o grado de chorreado (ISO 8501-1), y grado de soldaduras y cantos (ISO 8501-3).',
                 'Sistema: número de capas, tipo de cada una y espesor mínimo por capa y total, y cómo se mide (ISO 2808, ISO 2360 o ISO 19840).',
                 'Polvo: fabricante, referencia y homologación: código P-No. y clase QUALICOAT, o clase Florida de GSB.',
                 'Lacador: número de licencia QUALICOAT, QUALISTEELCOAT o GSB, sistema que cubre y vigencia. QUALICOAT publica la lista de lacadores con licencia.',
                 'Ensayos: informe con laboratorio, número y fecha; norma y edición; horas; probetas con o sin incisión; y resultado según ISO 4628 y adherencia.',
                 'Brillo: categoría o valor en GU a 60° (ISO 2813).',
                 'Color: referencia RAL y tolerancia ΔE (ISO 11664-4), con una placa de muestra aprobada.',
                 'Garantía: plazo en años y condiciones, por escrito. La durabilidad de ISO 12944 no es una garantía.',
             ]},
        ],
        'faq': [
            ('¿Qué diferencia hay entre una certificación y una norma?', 'Una certificación la concede un tercero que inspecciona al lacador y ensaya sus piezas, como QUALICOAT o QUALISTEELCOAT; tiene número y vigencia. Una norma, como ISO 12944 o ISO 9227, define ensayos y requisitos; su cumplimiento se demuestra con informes de ensayo.'),
            ('¿Se aplica la norma ISO 12944 a la pintura en polvo?', 'No directamente. ISO 12944 está pensada para pinturas que secan a temperatura ambiente y deja fuera los recubrimientos en polvo. Un sistema en polvo puede ensayarse según sus métodos, certificarse con QUALISTEELCOAT o GSB, o seguir la norma alemana DIN 55633, escrita para sistemas en polvo sobre acero.'),
            ('¿Sigue existiendo la clase C5-M?', 'Sí, con otro significado. En 1998 era la clase marina; en ISO 12944-2:2017, C5-I y C5-M se unificaron en C5, y la letra pasó a indicar la durabilidad. Hoy C5-M es C5 con durabilidad media (7 a 15 años): la clasificación del sistema Marine.'),
            ('¿A cuántos años equivalen 1.000 horas de niebla salina?', 'A ninguna cifra concreta. La propia ISO 9227 advierte que el ensayo no sirve para predecir la resistencia a largo plazo. Sirve para controlar un sistema concreto frente a una referencia.'),
            ('¿La durabilidad de ISO 12944 es una garantía?', 'No. Las clases L, M, H y VH son un dato para planificar, no un plazo de garantía. La garantía se pacta aparte, por escrito.'),
            ('Si el polvo está homologado QUALICOAT, ¿el lacado también lo está?', 'No. La homologación es del polvo; el sello es del lacador. Solo una planta con licencia QUALICOAT puede vender su lacado con el sello. Con GSB ocurre lo mismo.'),
            ('¿Qué diferencia hay entre QUALICOAT y QUALISTEELCOAT?', 'QUALICOAT certifica el lacado de aluminio para arquitectura. QUALISTEELCOAT certifica el lacado de acero y acero galvanizado, por sistema y por categoría de corrosividad, por ejemplo C5-H.'),
            ('¿Tiene JomaPaint licencia QUALICOAT o QUALISTEELCOAT?', PH('[Estado en JomaPaint: a confirmar]')),
            ('¿La ISO 9001 de Joma cubre la pintura para terceros?', 'El certificado actual cubre el diseño, la fabricación y la comercialización de cajas de caudales, armarios de llaves, buzones y otras cajas metálicas; no la pintura para terceros. ' + PH('[Ampliación del alcance: a confirmar]')),
            ('¿Puedo ver el informe de ensayo del sistema Marine?', PH('[Laboratorio, n.º de informe y condiciones de entrega: a confirmar]')),
        ],
        'faq_n': 7,
    },
    # ================================================================== EU
    'eu': {
        'slug': 'hauts-pinturaren-ziurtagiriak-arauak/',
        'title': 'Hauts-pinturaren ziurtagiriak eta arauak | JomaPaint',
        'description': 'QUALICOAT, QUALISTEELCOAT, GSB, ISO 9001 eta ISO 12944 azalduta: zer bermatzen duen zigilu eta arau bakoitzak, nola egiaztatzen den eta zer eskatu agirian.',
        'og_title': 'Hauts-pinturaren ziurtagiriak eta arauak · JomaPaint',
        'name': 'Hauts-pinturaren ziurtagiriak eta arauak', 'crumb': 'Ziurtagiriak eta arauak', 'service_type': None,
        'kicker': 'Gida teknikoa · JomaPaint, Legutio (Araba)',
        'h1': 'Hauts-pinturaren ziurtagiriak eta arauak',
        'lead': 'Zigilu eta arau bakoitza zer den, zer bermatzen dizun eta nola egiaztatzen den: saiakuntzak, orduak eta irizpideak. Baldintza-agiri bat irakurtzeko, sistema bat zehazteko edo eskaintzak datuekin alderatzeko.',
        'img_alt': '',
        'img_cap': '',
        'facts': [('Eskemak', 'QUALICOAT · QUALISTEELCOAT · GSB', 'Lakatzailea ziurtatzen dute'), ('Giroak', 'C1etik CXera', 'ISO 12944-2:2017'), ('Iraunkortasuna', 'L · M · H · VH', 'Ez da bermea')],
        'sections': [
            # ---------------------------------------------------------- 1
            {'h2': 'Ziurtagiria, homologazioa eta araua: ez dira gauza bera', 'p': [
                'Ziurtagiria hirugarren batek ematen du, lakatzailea ikuskatu eta haren piezei saiakuntzak egin ondoren. Hala dira QUALICOAT, QUALISTEELCOAT eta GSB. Lantegi edo sistema jakin bati lotuta dago, zenbakia du eta aldizkako ikuskapenekin mantentzen da.',
                'Homologazioa produktu bati dagokio: eskemak probatu duen hauts, aurretratamendu edo geruza-sistema bati. Hautsa homologatuta egoteak ez du lakatzailea ziurtatu bihurtzen.',
                'ISO edo EN arau batek saiakuntzak eta baldintzak zehazten ditu. Ez da zigilua: betetzen dela saiakuntza-txostenekin frogatzen da, laborategia eta zenbakia adierazita.',
            ],
             'table': {
                 'cols': ['Eskema', 'Aluminioa', 'Altzairua eta galbanizatua', 'Lakatzea ziurtatzen du'],
                 'rows': [
                     ('QUALICOAT', [('yes', 'Bai'), ('no', 'Ez'), ('yes', 'Bai, lantegi bakoitzeko')]),
                     ('QUALISTEELCOAT', [('no', 'Ez'), ('yes', 'Bai'), ('yes', 'Bai, sistema bakoitzeko')]),
                     ('GSB', [('yes', 'Bai'), ('yes', 'Bai'), ('yes', 'Bai: Standard, Master edo Premium zigilua')]),
                     ('ISO 9001 · ISO 14001', [('mid', 'Irismenaren arabera'), ('mid', 'Irismenaren arabera'), ('no', 'Ez: kudeaketa ziurtatzen dute')]),
                     ('ISO eta EN arauak', [('mid', 'Arauaren arabera'), ('mid', 'Arauaren arabera'), ('no', 'Ez: saiakuntzak zehazten dituzte')]),
                 ],
                 'note': 'Zigilu batek lizentzia-zenbakiarekin eta indarraldiaren barruan bakarrik balio du.',
             }},
            # ---------------------------------------------------------- 2
            {'h2': 'QUALICOAT: arkitekturako aluminioaren lakatzea', 'p': [
                'QUALICOAT kalitate-zigilu bat da, arkitekturako aluminioari hauts-pintura edo pintura likidoa aplikatzeko: profilak, fatxadak, arotzeria. Marka erregistratua da. Indarreko zehaztapena 26. edizioa da, 2026ko urtarrilaren 1etik baliozkoa.',
                'Zer bermatzen dizun: aurretratamenduak, hautsak, ontzeak eta amaitutako produktuak baldintza zehatzak betetzen dituztela, eta hirugarren batek egiaztatzen duela, ISO/IEC 17025 arauaren arabera akreditatutako laborategiekin.',
                'Espainian Espainiako Aluminioaren eta Gainazal Tratamenduen Elkarteak (AEA) kudeatzen du.',
            ],
             'cards': [
                 ('Lakatzailearen lizentzia', 'Lantegi bakoitzari ematen zaio. Aurretik linea, barneko laborategia, prozesua eta amaitutako produktua ikuskatzen dira. Gero aldizkako ikuskapenak etortzen dira, korrosio-saiakuntzekin. Lakatzaileak bere laborategian kontrolatzen ditu, besteak beste, distira (ISO 2813), lodiera (ISO 2360), atxikimendua (ISO 2409, 0 emaitza), tolestea (ISO 1519) eta talka (ISO 6272). Gutxieneko lodiera: 60 µm geruza bakarrean (1., 1.5 eta 2. klaseetako hautsak) eta 110 µm bi geruzatan; neurketa bakar bat ere ez gutxienekoaren % 80tik behera.'),
                 ('Hautsaren homologazioa', 'Homologatutako hauts bakoitzak P-No. kode bat eta klase bat ditu. Homologatzeko, besteak beste, saiakuntza hauek egiten dira: xenoia (ISO 16474-2, 1.000 h, 1. klasetik 2.era), gatz-laino azetikoa (ISO 9227 AASS, 1.000 h; 2.000 h 3. klasean), kondentsazioa (ISO 6270-2, 1.000 h; 2.000 h 3. klasean) eta SO₂ (ISO 22479, 24 ziklo).'),
                 ('SEASIDE', 'Itsas girorako abal gehigarria. Aurretratamendu indartua eskatzen du, gutxienez 2,0 g/m²-ko eraso kimikoarekin (estandarrean, 1,0 g/m²), eta korrosio filiformeko saiakuntza bat (ISO 4623-2, 1.000 h): harizpirik luzeena ≤ 4 mm eta batez bestekoa ≤ 2 mm. QUALICOATek C4tik aurrera gomendatzen du, edo aurre-anodizatua, eta batez ere C5ean eta CXen.'),
             ],
             'note': 'JomaPaint-en egoera: ' + PH('[berresteko]')},
            # ---------------------------------------------------------- 3
            {'h2': 'QUALICOAT hauts-klaseak: Floridako urteak eta distira', 'p': [
                'Hauts baten klaseak adierazten du zenbat mantentzen dituen distira eta kolorea eguzkitan. Floridan (ISO 2810) hegoaldera begira jarritako probetekin egiaztatzen da: 5°-ko inklinazioarekin 1. klasetik 2.era, eta 45°-koarekin 3. klasean.',
                'Aldi bakoitzaren amaieran hondar-distira eta kolore-aldaketa neurtzen dira; aldaketak RAL bakoitzerako finkatutako mugen barruan egon behar du.',
            ],
             'data': [
                 ('1. klasea', 'Urtebete Floridan · hondar-distira ≥ % 50'),
                 ('1.5 klasea', '2 urte · ≥ % 65 urtebetera eta ≥ % 50 bi urtera'),
                 ('2. klasea', '3 urte · ≥ % 75, % 60 eta % 50, 1, 2 eta 3 urtera'),
                 ('3. klasea', '10 urte · ≥ % 80 hiru urtera eta ≥ % 50 hamar urtera'),
             ],
             'note': '2023ko zehaztapen teknikoko atalaseak. Indarreko edizioa 26.a da, 2026koa.'},
            # ---------------------------------------------------------- 4
            {'h2': 'QUALISTEELCOAT: altzairuaren eta altzairu galbanizatuaren lakatzea', 'p': [
                'QUALISTEELCOAT altzairurako zigilu baliokidea da. Altzairu biluzian edo zinkdunean hauts-pinturaz edo pintura likidoz egindako lakatzea ziurtatzen du: beroan edo etengabe galbanizatua, elektrozinkatua, metalizatua edo sherardizatua. Espainian AEAk kudeatzen du.',
                'Lizentzia sistema bakoitzeko ematen da: aurretratamendu, geruza eta korrosibitate-kategoria jakin batzuetarako. Kodeak substratua eta geruza kopurua adierazten ditu: ST (altzairua), HD (beroan galbanizatua), SZ (etengabe galbanizatua), MS (metalizatua) eta STEC (kataforesidun altzairua). Adibidez, STEC3 kataforesia, inprimazioa eta akabera da.',
                'Zer bermatzen dizun: sistemak kategoria eta iraunkortasun jakin baten saiakuntzak gainditu dituela, eta lantegia ikuskatu egiten dela. ISO 12944ren, pintura likidorako pentsatua, eta hauts-pinturaren arteko zubia da. H letrak iraunkortasun handia esan nahi du: 15 eta 25 urte artean, ISO 12944-1en arabera.',
            ],
             'list': [
                 'Lakatzaileak aukeratzen ditu ziurtatu nahi dituen korrosibitate-kategoria eta sistema.',
                 'Laborategi propioa, material homologatuak eta autokontrola: lodiera, distira, atxikimendua, talka, ur irakina, gatz-lainoa, marradura eta gogortasuna.',
                 'Emakida-ikuskapena eta, ondoren, urtean bi ikuskapen, abisatu gabe.',
                 'Gatz-lainoaren ondoren, ebakiko irizpidea ≤ 1 mm da, ISO 12944-6ko 1,5 mm baino zorrotzagoa. Galbanizatuan 8 mm arteko delaminazioa onartzen da.',
                 'Gainera: xenoia (ISO 16474-2, 1.000 h) eta urtebeteko esposizio naturala (ISO 2810).',
             ],
             'data': [
                 ('C2-H', 'Hezetasuna ISO 6270-2: 120 h · Gatz-lainoa ISO 9227: 240 h'),
                 ('C3-H', 'Hezetasuna: 240 h · Gatz-lainoa: 480 h'),
                 ('C4-H', 'Hezetasuna: 480 h · Gatz-lainoa: 720 h'),
                 ('C5-H', 'Hezetasuna: 720 h · Gatz-lainoa: 1.440 h, edo 1.680 h saiakuntza ziklikoan'),
             ],
             'note': 'JomaPaint-en egoera: ' + PH('[berresteko]')},
            # ---------------------------------------------------------- 5
            {'h2': 'GSB: aluminiorako eta altzairurako zigilu alemana', 'p': [
                'GSB International lakatzearen kalitaterako elkarte alemana da. Kate osoa kontrolatzen du: aurretratamendu-produktuak, pinturak eta lakatzaileak. Bere araudia GSB AL 631 da aluminiorako eta GSB ST 663 altzairurako eta galbanizaturako; indarreko edizioa 2026ko urtarrilekoa da.',
                'Pinturak eta lakatzaileak bereiz sailkatzen ditu. QUALICOATen bezala, GSBk homologatutako pintura erabiltzea ez da nahikoa lakatzea araudiarekin bat etor dadin.',
            ],
             'cards': [
                 ('Pinturak: Florida 1, 3, 5 eta 10', 'Pinturak Floridan gainditzen dituen esposizio-urteak, gutxienez % 50eko hondar-distirarekin eta kolore egonkorrarekin. GSBk UV erresistentzia estandarra, handia, oso handia eta muturrekoa deitzen die.'),
                 ('Lakatzaileak: Standard, Master eta Premium', 'Hiru zigilu. Altzairuan, bi geruzako sistemak gainditzen duen gatz-lainoak bereizten ditu: 480 h (Standard), 720 h (Master) eta 1.440 h (Premium); geruza bakarrean, 480 h hirurek. Irizpideak: altzairuan ≤ 3 mm-ko delaminazioa eta galbanizatuan ≤ 8 mm, burbuilarik gabe. Premiumek, gainera, eskaera bakoitzaren trazabilitate osoa eskatzen du.'),
                 ('Sea Proof eta Sea Proof Plus', 'Kostaldeko aluminiorako zigilu gehigarriak: Sea Proof C4rako eta Sea Proof Plus C5erako, aurre-anodizatuarekin. Korrosio filiformeko eta gatz-laino azetikoko saiakuntzak egiten zaizkie: Sea Proof-i urtean behin eta Sea Proof Plus-i urtean bitan. Aluminioan Premium izateko, bietako bat behar da.'),
                 ('Nola egiaztatzen den', 'Abisatutako auditoria bat eta abisatu gabeko beste bat, korrosio-saiakuntzetarako laginak hartuta. Ondoren, urtean bi luzapen-saiakuntza, abisatu gabe. Saiakuntza batek huts egiten badu: baldintza gehigarriak, errepikapena, zigilua jaistea edo kentzea.'),
             ]},
            # ---------------------------------------------------------- 6
            {'h2': 'ISO 9001 eta ISO 14001: kudeaketa-sistemak', 'p': [
                'Enpresa nola kudeatzen den ziurtatzen dute, ez estaldura batek nola jokatzen duen. ISO 9001 kalitatearen kudeaketari buruzkoa da; ISO 14001, ingurumen-kudeaketari buruzkoa. Ziurtagiri bakoitzak irismen zehatz bat du, idatziz jasota.',
                'Ez ditu ISOk ematen, kanpoko ziurtapen-erakundeek baizik, ahal dela akreditatuek; Espainian, ENACek akreditatuek. Jarraipen-auditoriekin mantentzen dira.',
                'Jomaren ISO 9001:2015 ziurtagiriak kutxa gotorren, giltza-armairuen, postontzien, botikinen, iragarki-panelen eta kutxa metalikoen diseinua, fabrikazioa eta merkaturatzea hartzen ditu. Ez du hirugarrenentzako pintura hartzen.',
            ],
             'cards': [
                 ('ISO 9001 · kalitatea', 'Prozesu dokumentatuak, trazabilitatea, ez-adostasunen eta erreklamazioen kudeaketa, eta etengabeko hobekuntza.'),
                 ('ISO 14001 · ingurumena', 'Ingurumen-alderdien kontrola: aurretratamenduko isurketak, hauts-hondakinak eta labeen energia.'),
             ],
             'data': [
                 ('ISO 9001en indarreko edizioa', 'ISO 9001:2026, 2026ko irailean argitaratua'),
                 ('ISO 14001en indarreko edizioa', 'ISO 14001:2026, 2026ko apirilean argitaratua'),
                 ('ISO 9001:2015 ziurtagiriak', 'Trantsizioa 2029-09-30 arte'),
             ],
             'note': 'JomaPaint-en egoera: ' + PH('[ISO 9001 eta ISO 14001 hirugarrenentzako pinturarako: berresteko]')},
            # ---------------------------------------------------------- 7
            {'h2': 'ISO 12944, zatiz zati', 'p': [
                'ISO 12944 altzairuzko egiturak pintura-sistemen bidez babesteko erreferentziazko araua da. Giroak, iraunkortasuna, prestaketa, sistemak, saiakuntzak eta exekuzioa zehazten ditu.',
                'Bere eremua 3 mm edo lodiagoko karbono-altzairuzko egiturak dira, giro-tenperaturan lehortzen edo ontzen diren pinturekin. Kanpoan uzten ditu hauts-estaldurak eta labeko esmalteak; 7. zatiak berariaz baztertzen du hautsaren aplikazioa.',
                'Horregatik, hauts-sistema batek ez du «ISO 12944 betetzen»: haren metodoen arabera probatzen da (6. zatia) eta haren kategoriekin deskribatzen da (2. zatia), edo hautserako pentsatutako eskema batekin egiaztatzen da (QUALISTEELCOAT, GSB ST 663) edo DIN 55633 arau alemanarekin.',
            ],
             'data': [
                 ('1. zatia · 2017', 'Sarrera, terminoak eta iraunkortasuna (L, M, H, VH).'),
                 ('2. zatia · 2017', 'Giroen sailkapena: C1etik CXera eta Im1etik Im4ra.'),
                 ('3. zatia · 2017', 'Diseinu-irizpideak. P3 maila (ISO 8501-3) eskatzen du iraunkortasun handi eta oso handirako C4, C5, CX eta Im giroetan.'),
                 ('4. zatia · 2017', 'Gainazal motak eta haien prestaketa.'),
                 ('5. zatia · 2019', 'Pintura-sistemak: geruza kopurua eta gutxieneko lodiera. Ez ditu CX eta Im4 hartzen.'),
                 ('6. zatia · 2018', 'Laborategiko saiakuntzak C2tik C5era eta Im1etik Im3ra. Emaitzek ez dute iraunkortasuna zehatz ematen.'),
                 ('7. zatia · 2017', 'Pintura-lanen exekuzioa eta gainbegiratzea. Hautsaren aplikazioa baztertzen du.'),
                 ('8. zatia · 2017', 'Obra berrirako eta mantentze-lanetarako zehaztapenak idaztea.'),
                 ('9. zatia · 2018', 'Offshore eta antzeko egituretarako sistemak: CX eta Im4. ISO 20340 ordezten du.'),
             ],
             'note': 'Serie osoa berrikusten ari dira. Bitartean, adierazitako edizioak daude indarrean.'},
            # ---------------------------------------------------------- 8
            {'h2': 'Korrosibitate-kategoriak: C1etik CXera, eta Im1etik Im4ra', 'p': [
                'ISO 12944-2 arauak giroa sailkatzen du zenbat korrosio eragiten duen kontuan hartuta: karbono-altzairuzko probeta batek esposizioaren lehen urtean galtzen duen lodiera. Balioak ISO 9223 arauarenak dira.',
            ],
             'data': [
                 ('C1 · oso txikia', 'Aire garbiko barrualde berotua: bulegoak, dendak, ikastetxeak. Altzairua: ≤ 1,3 µm lehen urtean.'),
                 ('C2 · txikia', 'Kutsadura gutxiko landa-giroa; kondentsazioa duen barrualde berotu gabea: biltegiak, kiroldegiak. 1,3 µm baino gehiago, 25 µm arte.'),
                 ('C3 · ertaina', 'Hiri- eta industria-giroa, SO₂ moderatuarekin; gazitasun txikiko kostaldea; ekoizpen-areto hezeak. 25 µm baino gehiago, 50 µm arte.'),
                 ('C4 · handia', 'Industria eta gazitasun moderatuko kostaldea; lantegi kimikoak, igerilekuak. 50 µm baino gehiago, 80 µm arte.'),
                 ('C5 · oso handia', 'Industria oso heze eta oldarkorra; gazitasun handiko kostaldea. 80 µm baino gehiago, 200 µm arte.'),
                 ('CX · muturrekoa', 'Offshore, muturreko industria, klima tropikala eta subtropikala. 200 µm baino gehiago, 700 µm arte.'),
                 ('Im1', 'Ur geza.'),
                 ('Im2', 'Itsasoko ura edo ur gazikara, babes katodikorik gabe.'),
                 ('Im3', 'Lurzorua.'),
                 ('Im4', 'Itsasoko ura edo ur gazikara, babes katodikoarekin. 2017an berria.'),
             ]},
            # ---------------------------------------------------------- 9
            {'h2': 'C5-M ala C5? 2017an aldatu zena', 'p': [
                '1998ko edizioan, C5ek bi aldaera zituen, altzairu-galera berarekin: C5-I, industriala, eta C5-M, itsasokoa, gazitasun handiko kostaldea eta offshore-a barne.',
                '2017ko edizioan biak C5 bakarrean bateratu ziren, eta horrek industria heze eta oldarkorra eta gazitasun handiko kostaldea hartzen ditu. Offshore-a CX kategoria berrira pasatu zen.',
                'Gaur egun kategoria iraunkortasunarekin batera idazten da: C4-H, C5-M, C5-VH. Horrela, «C5-M» «C5, iraunkortasun ertaina» da, 7tik 15 urtera: Marine sistemaren sailkapena. Baldintza-agirian, hobe da kategoria, iraunkortasun-letra eta arauaren edizioa idaztea: adibidez, C5-M, ISO 12944-2:2017 arauaren arabera.',
                'Iraunkortasuna (ISO 12944-1) lau mailatan adierazten da. Ez da berme-epea, planifikatzeko datua baizik. 1998an mailak hauek ziren: L (2 eta 5 urte artean), M (5 eta 15 artean) eta H (15 baino gehiago).',
            ],
             'data': [
                 ('L · txikia', '7 urte arte'),
                 ('M · ertaina', '7 eta 15 urte artean'),
                 ('H · handia', '15 eta 25 urte artean'),
                 ('VH · oso handia', '25 urte baino gehiago. 2017an berria.'),
             ],
             'note': 'Iraunkortasuna ez da bermea.'},
            # ---------------------------------------------------------- 10
            {'h2': 'ISO 12944-6ko saiakuntzak: orduak kategoriaka', 'p': [
                '6. zatiak kategoria eta iraunkortasun bakoitzerako laborategiko saiakuntzak finkatzen ditu. Kategoriaren ondoko letra iraunkortasuna da: C5-M C5 da, iraunkortasun ertainarekin. Bi probeta-sorta erabiltzen dira: bata kondentsazioan (ISO 6270-1) eta bestea gatz-laino neutroan (ISO 9227). Eskakizun handienetarako saiakuntza ziklikoa dago.',
                'Zikloak aste bat irauten du: 72 h UV eta kondentsazio (ISO 16474-3), 72 h gatz-laino eta 24 h −20 °C-tan.',
                'Ondoren, burbuilak, herdoila, pitzadurak eta ezkatatzea (ISO 4628-2tik -5era), ebakitik abiatutako korrosioaren aurrerapena (ISO 4628-8) eta atxikimendua (ISO 2409 edo ISO 4624) ebaluatzen dira.',
            ],
             'data': [
                 ('C3-H', 'Kondentsazioa 240 h · gatz-lainoa 480 h'),
                 ('C4-H', 'Kondentsazioa 480 h · gatz-lainoa 720 h'),
                 ('C5-M', 'Kondentsazioa 480 h · gatz-lainoa 720 h'),
                 ('C5-H', 'Kondentsazioa 720 h · gatz-lainoa 1.440 h, edo 1.680 h saiakuntza ziklikoan'),
                 ('C5-VH', '2.688 h saiakuntza ziklikoan (16 ziklo)'),
                 ('CX (ISO 12944-9)', '4.200 h saiakuntza ziklikoan (25 ziklo)'),
             ],
             'note': 'Bi saiakuntzak behar dira: gatz-laino orduek, bakarrik, ez dute iraunkortasunik egiaztatzen.'},
            # ---------------------------------------------------------- 11
            {'h2': 'Korrosio- eta zahartze-saiakuntzak', 'p': [
                'Ganberan egiten diren saiakuntza azkartuak dira. Sistema jakin bat erreferentzia baten aldean kontrolatzeko eta hitzartutakoa betetzen duela egiaztatzeko balio dute. Haien orduak ez dira zerbitzu-urte bihurtzen.',
            ],
             'cards': [
                 ('Gatz-lainoa · ISO 9227', 'Probetak, normalean metaleraino iristen den ebaki batekin, ur gaziko laino etengabe batean. Hiru aldaera: neutroa (NSS: 35 °C, % 5eko sodio kloruroa), azetikoa (AASS: QUALICOATek aluminiorako eskatzen duena) eta kobrezko azetikoa (CASS, 50 °C-tan). Arauak berak ohartarazten du ez dela materialak sailkatzeko ezta epe luzeko erresistentzia aurreikusteko. Indarreko edizioa: 2022.'),
                 ('Hezetasuna · ISO 6270', 'Ura kondentsatzen da probetaren gainean. 1. zatian, alde batetik eta etengabe; 2. zatian, ganberan, giro konstantean (40 °C eta % 100eko hezetasuna) edo txandakakoan. Burbuilak eta atxikimendu-galerak atzematen ditu.'),
                 ('SO₂ (Kesternich) · ISO 22479', 'Hezetasuna sufre dioxidoarekin, giro industrialak simulatzeko. 24 orduko zikloak: 8 h 40 °C-tan SO₂-arekin eta 16 h giro-tenperaturan, ganbera aireztatuta. ISO 3231 eta ISO 6988 ordezten ditu, biak baliogabetuak.'),
                 ('Xenoia · ISO 16474-2', 'Xenon-lanpararen argia, eguzkiaren antzekoa, ur-zikloekin. QUALICOATek 1.000 h erabiltzen ditu hautsak homologatzeko. ISO 11341 ordeztu zuen.'),
                 ('UV fluoreszentea · ISO 16474-3', 'UV lanparak, adibidez UVA-340, kondentsazioarekin. ISO 12944-6 eta -9 arauen saiakuntza ziklikoaren parte da. Ez du eguzki-espektro osoa erreproduzitzen.'),
                 ('Esposizio naturala · ISO 2810', 'Probetak kanpoan, zuzenean edo beiraren atzean. QUALICOAT eta GSBren «Floridako saiakuntzaren» oinarria da: distiraren eta kolorearen benetako egiaztapena urteetan zehar.'),
             ],
             'note': 'Saiakuntza-txosten serio batek araua eta edizioa, laborategia, zenbakia, probetak, orduak, irizpideak eta emaitza adierazten ditu.'},
            # ---------------------------------------------------------- 12
            {'h2': 'Filmaren saiakuntzak: atxikimendua, lodiera, distira eta kolorea', 'p': [
                'Geruzaren beraren gainean egiten diren kontrolak dira, lantegian edo laborategian.',
            ],
             'data': [
                 ('Koadrikula-ebakia · ISO 2409', 'Metaleraino koadrikula bat ebaki, zinta itsatsi eta zenbat askatzen den begiratzen da. 0 (askatzerik gabe) eta 5 arteko klaseak. QUALICOATek 0 eskatzen du. Ez da baliozkoa 250 µm-tik gora ezta testuradunetan ere.'),
                 ('Trakzioa (pull-off) · ISO 4624', 'Euskarri metaliko bat itsatsi eta tiraka erauzten da: atxikimendua MPa-tan ematen du. ISO 12944-9k gutxienez 5 MPa eskatzen ditu zahartu aurretik.'),
                 ('Lodiera · ISO 2808 eta ISO 2360', 'ISO 2808k filma neurtzeko metodoak biltzen ditu, ontu gabeko hautsarena ere bai; ISO 2360k, metal ez-magnetikoaren gaineko neurketa korronte induzituen bidez, aluminioan adibidez. Gainazal granailatuetan, laginketa eta onarpena ISO 19840 arauaren araberakoak dira.'),
                 ('Distira · ISO 2813', '20°, 60° edo 85°-tan neurtzen da, distira-unitateetan (GU). QUALICOATek hiru kategoriatan biltzen ditu hautsak 60°-tan: matea (0–30 GU), satinatua (31–70) eta distiratsua (71–100).'),
                 ('Tolestea · ISO 1519', 'Probeta pintatua mandril zilindriko baten gainean tolestu eta filma pitzatzen edo askatzen den begiratzen da.'),
                 ('Enbutizioa · ISO 1520', 'Xafla pintatua zulatzaile batekin deformatzen da kupula bat osatu arte, eta filma berrikusten da.'),
                 ('Talka · ISO 6272', 'Pisu bat erortzen da probetaren gainera, eta filma pitzatzen edo askatzen den begiratzen da.'),
                 ('Buchholz gogortasuna · ISO 2815', 'Pisu finkoko identadore batek arrasto bat uzten du; haren luzerak ematen du gogortasuna.'),
                 ('Degradazioa · ISO 4628', 'Saiakuntza baten ondoren kaltea nola kalifikatzen den: burbuilak (-2), herdoila (-3), pitzadurak (-4), ezkatatzea (-5), ebakitik abiatutako korrosioa (-8) eta filiformea (-10).'),
                 ('Kolorea · ISO 11664-4', 'Piezaren eta erreferentziaren arteko ΔE kolore-aldea, CIELAB espazioan. ISO 7724 zaharra 2013tik dago baliogabetuta.'),
             ],
             'note': 'Lantegian egiten ditugun kontrolak: ' + PH('[berresteko]')},
            # ---------------------------------------------------------- 13
            {'h2': 'Gainazalaren prestaketa: ISO 8501 eta ISO 8503', 'p': [
                'Sistema baten bizitzaren zati handi bat pintatu aurreko altzairuaren garbitasunaren eta zimurtasunaren araberakoa da. Arau hauei esker, egiazta daitezkeen mailak adostu daitezke.',
            ],
             'data': [
                 ('ISO 8501-1', 'Hasierako altzairuaren herdoil-mailak eta prestaketa-mailak: Sa 1etik Sa 3ra granailatuz, eta St eskuzko edo makina bidezko garbiketarako. Sa 2½ ia metal zuria da; Sa 3, metal zuria. Argazkiekin deskribatzen dira.'),
                 ('ISO 8501-3', 'P1, P2 eta P3 mailak soldaduretarako, ertzetarako eta beste akats batzuetarako. 2025eko edizioa. ISO 12944-3k P3 eskatzen du iraunkortasun handi eta oso handirako C4, C5 eta CX giroetan; EN 1090-2k ere erabiltzen ditu.'),
                 ('ISO 8503-1', 'Granailarekin edo korindoiarekin granailatu ondorengo zimurtasun-profila sailkatzeko konparagailuak.'),
             ],
             'note': 'JomaPaint-en prestaketa: ' + PH('[granailatzea eta Sa maila: berresteko]')},
            # ---------------------------------------------------------- 14
            {'h2': 'Produktuko eta exekuzioko EN arauak', 'p': [
                'Eraikuntzako baldintza-agirietan agertzen diren Europako arauak. Arauak dira, ez zigiluak: saiakuntzekin eta dokumentuekin betetzen eta frogatzen dira.',
            ],
             'data': [
                 ('EN 13438', 'Beroan galbanizatutako edo sherardizatutako altzairuaren gaineko hauts-pinturaren portaera-baldintzak, eraikuntzarako. Ez du lakatze-prozesua arautzen.'),
                 ('EN 15773', 'Beroan galbanizatutako edo sherardizatutako altzairuaren gaineko hautsaren aplikazio industriala: sistema duplexak. Bezeroak, galbanizatzaileak, produktu kimikoen hornitzaileak eta lakatzaileak zer adostu behar duten zehazten du, baita galbanizatuari eskatzen zaion kalitatea ere. 2018ko edizioa.'),
                 ('EN ISO 1461', 'Pieza fabrikatuen beroko galbanizatua: propietateak eta saiakuntzak. Ez du gainean aplikatzen dena hartzen. 2022ko edizioa.'),
                 ('EN 12206-1', 'Arkitekturako aluminioaren gaineko hauts-lakatzea: aurretratamendua, hautsa, prozesua eta amaitutako produktua. 2021eko edizioa.'),
                 ('EN 1090-2', 'Altzairuzko egituren exekuzioa, gainazal-tratamendua barne. P1etik P3ra bitarteko prestaketa-maila babesaren aurreikusitako bizitzarekin eta korrosibitate-kategoriarekin lotzen du; biak proiektugileak adierazten ditu.'),
                 ('DIN 55633', 'Altzairua hauts-sistemekin babesteko arau alemana; haren kategoriak ISO 12944-2ri lotuta daude. 2. zatia kataforesi epoxi eta hauts sistemei buruzkoa da.'),
             ]},
            # ---------------------------------------------------------- 15
            {'h2': 'Marine sistemaren saiakuntzak', 'p': [
                'Marine Jomaren korrosioaren aurkako sistema da: murgiltze bidezko aurretratamendua, kataforesia, inprimazioa eta hauts-pinturazko akabera. Haren sailkapena C5-M da: C5 giroa, itsasertzeko lehen lerroa adibidez, iraunkortasun ertainarekin (7-15 urte).',
                'Ez da sistema ziurtatua: ISO 12944 pintura likidoetarako idatzi zen eta ez ditu hauts-sistemak ziurtatzen. Horregatik, datu bakoitza bere arauarekin, laborategiarekin eta txosten-zenbakiarekin doa.',
                'C5-M lortzeko, ISO 12944-6k 720 h gatz-laino neutro eta 480 h kondentsazio eskatzen ditu, ISO 4628 arauarekin eta atxikimenduarekin ebaluatuta. Orduak ez dira urteen baliokideak.',
            ],
             'layers': [
                 ('Hauts-pintura', 'Akabera, aukeratutako RALean. Hauts mota: ' + PH('[poliesterra: berresteko]') + ' · ' + PH('[XX] µm')),
                 ('Inprimazioa', PH('[Mota: berresteko]') + ' · ' + PH('[XX] µm')),
                 ('Kataforesia', 'Elektrodeposizio bidezko inprimazioa gainazal osoan · ' + PH('[XX] µm')),
                 ('Substratua', PH('[Altzairua, galbanizatua edo biak: berresteko]') + ', murgiltze bidez aurretratatua'),
             ],
             'data': [
                 ('Gatz-laino neutroa · UNE-EN ISO 9227', '1.000 h (C5-Mk 720 h eskatzen ditu) · ' + PH('[txostena berresteko]')),
                 ('Emaitza', PH('[burbuilak, herdoila eta ebakitiko aurrerapena, ISO 4628 arauaren arabera]')),
                 ('Kondentsazioa · ISO 6270-1', PH('[C5-Mk 480 h eskatzen ditu: txostena berresteko]')),
                 ('Atxikimendua · ISO 2409', PH('[klasea berresteko]')),
                 ('Lodiera osoa · ISO 2808', PH('[XX] µm')),
                 ('Laborategia eta txosten-zenbakia', PH('[berresteko]')),
             ],
             'note': 'Sistemaren QUALISTEELCOAT ziurtapena: ' + PH('[berresteko]')},
            # ---------------------------------------------------------- 16
            {'h2': 'Nola aukeratu sistema, pieza non egongo den kontuan hartuta', 'p': [
                'Orientazio orokorra, ISO 12944-2ko giroetan oinarrituta. Sistema zehatza substratuaren, eskatzen duzun iraunkortasunaren eta hautsaren araberakoa da, eta zurekin finkatzen dugu.',
            ],
             'cards': [
                 ('Barrualde lehorra · C1', 'Bulego, denda edo ikastetxe berotuak. Hauts-geruza bat nahikoa da; epoxi-poliesterrak balio du pieza eguzkitan egongo ez bada.'),
                 ('Kondentsazioa duen barrualdea edo landa-giroa · C2', 'Nabe berotu gabeak, biltegiak, kiroldegiak; kutsadura gutxiko kanpoaldea. Kanpoan, poliester-geruza bat.'),
                 ('Hiria edo gazitasun txikiko kostaldea · C3', 'Hiria, SO₂ moderatuko industria, ekoizpen-areto hezeak. Poliesterra, aurretratamendu zaindu baten gainean; galbanizatuan, sistema duplexa.'),
                 ('Industria edo gazitasun moderatuko kostaldea · C4', 'Lantegi kimikoak, igerilekuak. Altzairuan, inprimazioa eta akabera; galbanizatuan, geruza bat edo bi, iraunkortasunaren arabera.'),
                 ('Industria oldarkorra edo gazitasun handiko kostaldea · C5', '1998an, C5-I eta C5-M. Geruza anitzeko sistemak: galbanizatua inprimazioarekin eta akaberarekin, edo kataforesia, inprimazioa eta akabera, Marine C5-M sistema bezala. Eskatu sistema osoaren saiakuntzak.'),
                 ('Offshore, urpean edo lurperatuta · CX eta Im', 'Berariazko sistemak, ISO 12944-9 (CX, Im4) edo ISO 12944-6 (Im1etik Im3ra) arauen arabera probatuak. Kasuz kasu aztertzen dira.'),
             ],
             'note': 'Arkitekturako aluminioan, QUALICOATek SEASIDE aurretratamendua edo aurre-anodizatua gomendatzen du C4tik aurrera.'},
            # ---------------------------------------------------------- 17
            {'h2': 'Zer eskatu baldintza-agiri edo zehaztapen batean', 'p': [
                'Edozein lakatzaileri idatziz eskatzea komeni dena, guri ere bai:',
            ],
             'list': [
                 'Giroa eta iraunkortasuna: korrosibitate-kategoria (C1etik CXera, Im) eta iraunkortasun-maila (L, M, H edo VH), arauaren edizioarekin. Adibidez, C5-H, ISO 12944-2:2017 arauaren arabera.',
                 'Substratua: altzairua; beroan edo etengabe galbanizatutako altzairua edo altzairu elektrozinkatua; edo aluminioa.',
                 'Prestaketa: aurretratamendu kimikoa edo granailatze-maila (ISO 8501-1), eta soldadura eta ertzen maila (ISO 8501-3).',
                 'Sistema: geruza kopurua, bakoitzaren mota eta gutxieneko lodiera, geruzaka eta guztira, eta nola neurtzen den (ISO 2808, ISO 2360 edo ISO 19840).',
                 'Hautsa: fabrikatzailea, erreferentzia eta homologazioa: QUALICOAT P-No. kodea eta klasea, edo GSBren Florida klasea.',
                 'Lakatzailea: QUALICOAT, QUALISTEELCOAT edo GSB lizentziaren zenbakia, hartzen duen sistema eta indarraldia. QUALICOATek lizentziadun lakatzaileen zerrenda argitaratzen du.',
                 'Saiakuntzak: txostena, laborategia, zenbakia eta data; araua eta edizioa; orduak; probetak ebakiarekin edo gabe; eta emaitza, ISO 4628 arauaren eta atxikimenduaren arabera.',
                 'Distira: kategoria edo balioa GUtan, 60°-tan (ISO 2813).',
                 'Kolorea: RAL erreferentzia eta ΔE tolerantzia (ISO 11664-4), onartutako lagin-plaka batekin.',
                 'Bermea: epea urtetan eta baldintzak, idatziz. ISO 12944ko iraunkortasuna ez da bermea.',
             ]},
        ],
        'faq': [
            ('Zer alde dago ziurtapen baten eta arau baten artean?', 'Ziurtapena hirugarren batek ematen du, lakatzailea ikuskatu eta haren piezei saiakuntzak egin ondoren, QUALICOATek edo QUALISTEELCOATek bezala; zenbakia eta indarraldia ditu. Arau batek, ISO 12944k edo ISO 9227k bezala, saiakuntzak eta baldintzak zehazten ditu; betetzen dela saiakuntza-txostenekin frogatzen da.'),
            ('ISO 12944 araua hauts-pinturari aplikatzen zaio?', 'Ez zuzenean. ISO 12944 giro-tenperaturan lehortzen diren pinturetarako pentsatuta dago, eta kanpoan uzten ditu hauts-estaldurak. Hauts-sistema bat haren metodoen arabera proba daiteke, QUALISTEELCOAT edo GSB bidez ziurta daiteke, edo DIN 55633 arau alemanari jarrai diezaioke, altzairuaren gaineko hauts-sistemetarako idatzia.'),
            ('Oraindik badago C5-M klasea?', 'Bai, beste esanahi batekin. 1998an itsas klasea zen; ISO 12944-2:2017 arauan, C5-I eta C5-M C5 bakarrean bateratu ziren, eta letrak iraunkortasuna adierazten du orain. Gaur C5-M C5 da, iraunkortasun ertainarekin (7-15 urte): Marine sistemaren sailkapena.'),
            ('Zenbat urteren baliokideak dira gatz-lainoko 1.000 orduak?', 'Ez dago kopuru zehatzik. ISO 9227 arauak berak ohartarazten du saiakuntza ez dela epe luzeko erresistentzia aurreikusteko. Sistema jakin bat erreferentzia baten aldean kontrolatzeko balio du.'),
            ('ISO 12944ko iraunkortasuna bermea al da?', 'Ez. L, M, H eta VH mailak planifikatzeko datua dira, ez berme-epea. Bermea aparte hitzartzen da, idatziz.'),
            ('Hautsa QUALICOAT homologatua bada, lakatzea ere bai?', 'Ez. Homologazioa hautsarena da; zigilua, lakatzailearena. QUALICOAT lizentzia duen lantegi batek bakarrik saldu dezake bere lakatzea zigiluarekin. GSBrekin gauza bera gertatzen da.'),
            ('Zer alde dago QUALICOAT eta QUALISTEELCOAT artean?', 'QUALICOATek arkitekturako aluminioaren lakatzea ziurtatzen du. QUALISTEELCOATek altzairuaren eta altzairu galbanizatuaren lakatzea ziurtatzen du, sistemaka eta korrosibitate-kategoriaka, adibidez C5-H.'),
            ('JomaPaint-ek QUALICOAT edo QUALISTEELCOAT lizentzia du?', PH('[JomaPaint-en egoera: berresteko]')),
            ('Jomaren ISO 9001 ziurtagiriak hirugarrenentzako pintura hartzen du?', 'Gaur egungo ziurtagiriak kutxa gotorren, giltza-armairuen, postontzien eta beste kutxa metaliko batzuen diseinua, fabrikazioa eta merkaturatzea hartzen ditu; ez hirugarrenentzako pintura. ' + PH('[Irismenaren zabalkuntza: berresteko]')),
            ('Marine sistemaren saiakuntza-txostena ikus dezaket?', PH('[Laborategia, txosten-zenbakia eta emateko baldintzak: berresteko]')),
        ],
        'faq_n': 7,
    },
    # ================================================================== FR
    'fr': {
        'slug': 'certifications-normes-peinture-poudre/',
        'title': 'Certifications et normes de la peinture poudre | JomaPaint',
        'description': 'QUALICOAT, QUALISTEELCOAT, GSB, ISO 9001 et ISO 12944 expliqués : ce que garantit chaque label ou norme, comment on le vérifie, quoi exiger au cahier des charges.',
        'og_title': 'Certifications et normes de la peinture poudre · JomaPaint',
        'name': 'Certifications et normes de la peinture poudre', 'crumb': 'Certifications et normes', 'service_type': None,
        'kicker': 'Guide technique · JomaPaint, Legutio (Álava, Espagne)',
        'h1': 'Certifications et normes de la peinture poudre',
        'lead': 'Ce qu’est chaque label et chaque norme, ce qu’il vous garantit et comment on le vérifie : essais, durées et critères. Pour lire un cahier des charges, spécifier un système ou comparer des offres sur pièces.',
        'img_alt': '',
        'img_cap': '',
        'facts': [('Labels', 'QUALICOAT · QUALISTEELCOAT · GSB', 'Ils certifient l’applicateur'), ('Environnements', 'C1 à CX', 'ISO 12944-2:2017'), ('Durabilité', 'L · M · H · VH', 'Ce n’est pas une garantie')],
        'sections': [
            # ---------------------------------------------------------- 1
            {'h2': 'Certificat, homologation et norme : trois choses différentes', 'p': [
                'Un certificat est délivré par un tiers qui inspecte l’applicateur et fait essayer ses pièces. C’est le cas de QUALICOAT, QUALISTEELCOAT et GSB. Il est lié à une usine ou à un système, porte un numéro et se maintient par des inspections périodiques.',
                'Une homologation porte sur un produit : une poudre, un prétraitement ou un système de couches que le label a fait essayer. Une poudre homologuée ne fait pas de l’applicateur un applicateur certifié.',
                'Une norme ISO ou EN définit des essais et des exigences. Ce n’est pas un label : la conformité se démontre par des rapports d’essai, avec laboratoire et numéro.',
            ],
             'table': {
                 'cols': ['Label', 'Aluminium', 'Acier et galvanisé', 'Certifie le laquage'],
                 'rows': [
                     ('QUALICOAT', [('yes', 'Oui'), ('no', 'Non'), ('yes', 'Oui, par usine')]),
                     ('QUALISTEELCOAT', [('no', 'Non'), ('yes', 'Oui'), ('yes', 'Oui, par système')]),
                     ('GSB', [('yes', 'Oui'), ('yes', 'Oui'), ('yes', 'Oui : label Standard, Master ou Premium')]),
                     ('ISO 9001 · ISO 14001', [('mid', 'Selon le périmètre'), ('mid', 'Selon le périmètre'), ('no', 'Non : elles certifient la gestion')]),
                     ('Normes ISO et EN', [('mid', 'Selon la norme'), ('mid', 'Selon la norme'), ('no', 'Non : elles définissent des essais')]),
                 ],
                 'note': 'Un label ne vaut qu’avec son numéro de licence et pendant sa durée de validité.',
             }},
            # ---------------------------------------------------------- 2
            {'h2': 'QUALICOAT : le laquage de l’aluminium pour l’architecture', 'p': [
                'QUALICOAT est un label de qualité pour les revêtements en poudre ou liquides sur aluminium pour l’architecture : profilés, façades, menuiserie. C’est une marque déposée. La spécification en vigueur est la 26e édition, applicable depuis le 1er janvier 2026.',
                'Ce qu’il vous garantit : le prétraitement, la poudre, la cuisson et le produit fini répondent à des exigences définies, vérifiées par un tiers avec des laboratoires accrédités selon l’ISO/CEI 17025.',
                'En Espagne, il est géré par l’Association espagnole de l’aluminium et des traitements de surface (AEA).',
            ],
             'cards': [
                 ('Licence de l’applicateur', 'Elle est accordée par usine. Avant, on inspecte la ligne, le laboratoire interne, le procédé et le produit fini. Ensuite viennent des inspections périodiques, avec essais de corrosion. L’applicateur contrôle dans son laboratoire, entre autres, la brillance (ISO 2813), l’épaisseur (ISO 2360), l’adhérence (ISO 2409, résultat 0), le pliage (ISO 1519) et le choc (ISO 6272). Épaisseur minimale : 60 µm en une couche (poudres de classe 1, 1.5 et 2) et 110 µm en deux ; aucune mesure sous 80 % du minimum.'),
                 ('Homologation de la poudre', 'Chaque poudre homologuée a un code P-No. et une classe. Pour l’homologuer, on réalise entre autres des essais au xénon (ISO 16474-2, 1 000 h, classes 1 à 2), au brouillard salin acétique (ISO 9227 AASS, 1 000 h ; 2 000 h en classe 3), à la condensation (ISO 6270-2, 1 000 h ; 2 000 h en classe 3) et au SO₂ (ISO 22479, 24 cycles).'),
                 ('SEASIDE', 'Option complémentaire pour le milieu marin. Elle exige un prétraitement renforcé, avec une attaque d’au moins 2,0 g/m² contre 1,0 g/m² en standard, et un essai de corrosion filiforme (ISO 4623-2, 1 000 h) : filament le plus long ≤ 4 mm et moyenne ≤ 2 mm. QUALICOAT la recommande, ou la pré-anodisation, à partir de C4, et surtout en C5 et CX.'),
             ],
             'note': 'Statut chez JomaPaint : ' + PH('[à confirmer]')},
            # ---------------------------------------------------------- 3
            {'h2': 'Classes de poudre QUALICOAT : années en Floride et brillance', 'p': [
                'La classe d’une poudre indique dans quelle mesure elle conserve sa brillance et sa couleur au soleil. On la vérifie avec des éprouvettes exposées en Floride (ISO 2810), orientées au sud : inclinées à 5° pour les classes 1 à 2 et à 45° pour la classe 3.',
                'À la fin de chaque période, on mesure la brillance résiduelle et l’écart de couleur, qui doit rester dans les limites fixées pour chaque RAL.',
            ],
             'data': [
                 ('Classe 1', '1 an en Floride · brillance résiduelle ≥ 50 %'),
                 ('Classe 1.5', '2 ans · ≥ 65 % après 1 an et ≥ 50 % après 2 ans'),
                 ('Classe 2', '3 ans · ≥ 75 %, 60 % et 50 % après 1, 2 et 3 ans'),
                 ('Classe 3', '10 ans · ≥ 80 % après 3 ans et ≥ 50 % après 10 ans'),
             ],
             'note': 'Seuils de la spécification technique de 2023. L’édition en vigueur est la 26e, de 2026.'},
            # ---------------------------------------------------------- 4
            {'h2': 'QUALISTEELCOAT : le laquage de l’acier et de l’acier galvanisé', 'p': [
                'QUALISTEELCOAT est l’équivalent pour l’acier. Il certifie le laquage en poudre ou liquide sur acier nu ou revêtu de zinc : galvanisé à chaud ou en continu, électrozingué, métallisé ou shérardisé. En Espagne, il est géré par l’AEA.',
                'La licence est accordée par système : un prétraitement, des couches et une catégorie de corrosivité donnés. Le code indique le support et le nombre de couches : ST (acier), HD (galvanisé à chaud), SZ (galvanisé en continu), MS (métallisé) et STEC (acier cataphorésé). Par exemple, STEC3 désigne cataphorèse, primaire et finition.',
                'Ce qu’il vous garantit : le système a passé les essais d’une catégorie et d’une durabilité données, et l’usine est inspectée. Il fait le pont entre l’ISO 12944, pensée pour la peinture liquide, et la peinture poudre. Le H signifie durabilité haute : 15 à 25 ans selon l’ISO 12944-1.',
            ],
             'list': [
                 'L’applicateur choisit la catégorie de corrosivité et le système à certifier.',
                 'Laboratoire interne, matériaux homologués et autocontrôle : épaisseur, brillance, adhérence, choc, eau bouillante, brouillard salin, rayure et dureté.',
                 'Inspection d’admission, puis deux inspections par an sans préavis.',
                 'Critère à la rayure après brouillard salin : ≤ 1 mm, plus strict que les 1,5 mm de l’ISO 12944-6. Sur galvanisé, un décollement jusqu’à 8 mm est admis.',
                 'En plus : xénon (ISO 16474-2, 1 000 h) et un an d’exposition naturelle (ISO 2810).',
             ],
             'data': [
                 ('C2-H', 'Humidité ISO 6270-2 : 120 h · Brouillard salin ISO 9227 : 240 h'),
                 ('C3-H', 'Humidité : 240 h · Brouillard salin : 480 h'),
                 ('C4-H', 'Humidité : 480 h · Brouillard salin : 720 h'),
                 ('C5-H', 'Humidité : 720 h · Brouillard salin : 1 440 h, ou 1 680 h en essai cyclique'),
             ],
             'note': 'Statut chez JomaPaint : ' + PH('[à confirmer]')},
            # ---------------------------------------------------------- 5
            {'h2': 'GSB : le label allemand pour l’aluminium et l’acier', 'p': [
                'GSB International est une association allemande pour la qualité du laquage. Elle contrôle toute la chaîne : produits de prétraitement, peintures et applicateurs. Son règlement est GSB AL 631 pour l’aluminium et GSB ST 663 pour l’acier et le galvanisé ; l’édition en vigueur date de janvier 2026.',
                'Elle classe séparément les peintures et les applicateurs. Comme pour QUALICOAT, utiliser une peinture homologuée GSB ne suffit pas à rendre le laquage conforme.',
            ],
             'cards': [
                 ('Peintures : Florida 1, 3, 5 et 10', 'Années d’exposition en Floride que tient la peinture, avec une brillance résiduelle d’au moins 50 % et une couleur stable. GSB parle de résistance aux UV standard, haute, très haute et extrêmement haute.'),
                 ('Applicateurs : Standard, Master et Premium', 'Trois labels. Sur acier, ils se distinguent par le brouillard salin que tient le système bicouche : 480 h (Standard), 720 h (Master) et 1 440 h (Premium) ; en monocouche, 480 h pour les trois. Critères : décollement ≤ 3 mm sur acier et ≤ 8 mm sur galvanisé, sans cloquage. Premium exige en plus la traçabilité complète de chaque commande.'),
                 ('Sea Proof et Sea Proof Plus', 'Labels complémentaires pour l’aluminium en bord de mer : Sea Proof pour C4 et Sea Proof Plus pour C5, avec pré-anodisation. Essais de corrosion filiforme et de brouillard salin acétique : une fois par an pour Sea Proof, deux fois pour Sea Proof Plus. Pour être Premium sur aluminium, il faut l’un des deux.'),
                 ('Comment on le vérifie', 'Un audit annoncé et un autre inopiné, avec prélèvement d’échantillons pour essais de corrosion. Ensuite, deux essais de prolongation par an, sans préavis. En cas d’échec : exigences supplémentaires, nouvel essai, déclassement ou retrait du label.'),
             ]},
            # ---------------------------------------------------------- 6
            {'h2': 'ISO 9001 et ISO 14001 : systèmes de management', 'p': [
                'Elles certifient la façon dont l’entreprise est gérée, pas le comportement d’un revêtement. L’ISO 9001 porte sur le management de la qualité ; l’ISO 14001, sur le management environnemental. Chaque certificat couvre un périmètre précis, inscrit sur le certificat.',
                'Ce n’est pas l’ISO qui les délivre, mais des organismes de certification externes, de préférence accrédités ; en Espagne, par l’ENAC. Elles se maintiennent par des audits de suivi.',
                'Le certificat ISO 9001:2015 de Joma couvre la conception, la fabrication et la commercialisation de coffres-forts, armoires à clés, boîtes aux lettres, armoires à pharmacie, panneaux d’affichage et boîtes métalliques. Il ne couvre pas la peinture pour des tiers.',
            ],
             'cards': [
                 ('ISO 9001 · qualité', 'Procédés documentés, traçabilité, traitement des non-conformités et des réclamations, amélioration continue.'),
                 ('ISO 14001 · environnement', 'Maîtrise des aspects environnementaux : effluents du prétraitement, déchets de poudre et énergie des fours.'),
             ],
             'data': [
                 ('Édition en vigueur de l’ISO 9001', 'ISO 9001:2026, publiée en septembre 2026'),
                 ('Édition en vigueur de l’ISO 14001', 'ISO 14001:2026, publiée en avril 2026'),
                 ('Certificats ISO 9001:2015', 'Transition jusqu’au 30/09/2029'),
             ],
             'note': 'Statut chez JomaPaint : ' + PH('[ISO 9001 et ISO 14001 pour la peinture à façon : à confirmer]')},
            # ---------------------------------------------------------- 7
            {'h2': 'L’ISO 12944, partie par partie', 'p': [
                'L’ISO 12944 est la norme de référence pour protéger les structures en acier par des systèmes de peinture. Elle définit les environnements, la durabilité, la préparation, les systèmes, les essais et l’exécution.',
                'Elle vise les structures en acier au carbone de 3 mm ou plus, avec des peintures qui sèchent ou durcissent à température ambiante. Elle exclut les revêtements en poudre et les émaux cuits au four ; la partie 7 exclut expressément l’application de poudre.',
                'Un système poudre n’est donc pas « conforme à l’ISO 12944 » : on l’essaie selon ses méthodes (partie 6) et on le décrit avec ses catégories (partie 2), ou on le qualifie avec un label conçu pour la poudre (QUALISTEELCOAT, GSB ST 663) ou avec la norme allemande DIN 55633.',
            ],
             'data': [
                 ('Partie 1 · 2017', 'Introduction, termes et durabilité (L, M, H, VH).'),
                 ('Partie 2 · 2017', 'Classification des environnements : C1 à CX et Im1 à Im4.'),
                 ('Partie 3 · 2017', 'Conception. Exige le degré P3 (ISO 8501-3) pour une durabilité haute et très haute en C4, C5, CX et Im.'),
                 ('Partie 4 · 2017', 'Types de surface et préparation.'),
                 ('Partie 5 · 2019', 'Systèmes de peinture : nombre de couches et épaisseur minimale. Ne couvre ni CX ni Im4.'),
                 ('Partie 6 · 2018', 'Essais de laboratoire pour C2 à C5 et Im1 à Im3. Les résultats ne donnent pas la durabilité de façon exacte.'),
                 ('Partie 7 · 2017', 'Exécution et surveillance des travaux de peinture. Exclut l’application de poudre.'),
                 ('Partie 8 · 2017', 'Rédaction des spécifications pour le neuf et la maintenance.'),
                 ('Partie 9 · 2018', 'Systèmes pour l’offshore et les structures associées : CX et Im4. Remplace l’ISO 20340.'),
             ],
             'note': 'Toute la série est en cours de révision. En attendant, les éditions indiquées restent en vigueur.'},
            # ---------------------------------------------------------- 8
            {'h2': 'Catégories de corrosivité : de C1 à CX, et de Im1 à Im4', 'p': [
                'L’ISO 12944-2 classe l’environnement selon sa corrosivité : la perte d’épaisseur d’une éprouvette en acier au carbone pendant sa première année d’exposition. Les valeurs sont celles de l’ISO 9223.',
            ],
             'data': [
                 ('C1 · très faible', 'Intérieur chauffé à l’air propre : bureaux, magasins, écoles. Acier : ≤ 1,3 µm la première année.'),
                 ('C2 · faible', 'Extérieur rural peu pollué ; intérieur non chauffé avec condensation : entrepôts, salles de sport. Plus de 1,3 à 25 µm.'),
                 ('C3 · moyenne', 'Urbain et industriel avec SO₂ modéré ; littoral à faible salinité ; ateliers de production humides. Plus de 25 à 50 µm.'),
                 ('C4 · élevée', 'Industriel et littoral à salinité modérée ; usines chimiques, piscines. Plus de 50 à 80 µm.'),
                 ('C5 · très élevée', 'Industriel très humide et agressif ; littoral à forte salinité. Plus de 80 à 200 µm.'),
                 ('CX · extrême', 'Offshore, industriel extrême, climats tropical et subtropical. Plus de 200 à 700 µm.'),
                 ('Im1', 'Eau douce.'),
                 ('Im2', 'Eau de mer ou saumâtre, sans protection cathodique.'),
                 ('Im3', 'Sol.'),
                 ('Im4', 'Eau de mer ou saumâtre, avec protection cathodique. Nouvelle en 2017.'),
             ]},
            # ---------------------------------------------------------- 9
            {'h2': 'C5-M ou C5 ? Ce qui a changé en 2017', 'p': [
                'Dans l’édition de 1998, C5 avait deux variantes pour la même perte d’acier : C5-I, industrielle, et C5-M, marine, qui couvrait le littoral et l’offshore à forte salinité.',
                'Dans l’édition de 2017, les deux ont été regroupées en C5, qui couvre l’industrie humide et agressive et le littoral à forte salinité. L’offshore est passé dans la nouvelle catégorie CX.',
                'Aujourd’hui, la catégorie s’écrit avec la durabilité : C4-H, C5-M, C5-VH. Ainsi, « C5-M » signifie « C5, durabilité moyenne », de 7 à 15 ans : c’est le classement du système Marine. Dans un cahier des charges, mieux vaut écrire la catégorie, la lettre de durabilité et l’édition de la norme : par exemple, C5-M selon l’ISO 12944-2:2017.',
                'La durabilité (ISO 12944-1) s’exprime en quatre niveaux. Ce n’est pas une durée de garantie, mais une donnée de planification. En 1998, les niveaux étaient L (2 à 5 ans), M (5 à 15) et H (plus de 15).',
            ],
             'data': [
                 ('L · faible', 'Jusqu’à 7 ans'),
                 ('M · moyenne', '7 à 15 ans'),
                 ('H · haute', '15 à 25 ans'),
                 ('VH · très haute', 'Plus de 25 ans. Nouvelle en 2017.'),
             ],
             'note': 'La durabilité n’est pas une garantie.'},
            # ---------------------------------------------------------- 10
            {'h2': 'Essais de l’ISO 12944-6 : durées par catégorie', 'p': [
                'La partie 6 fixe les essais de laboratoire pour chaque catégorie et durabilité. La lettre après la catégorie est la durabilité : C5-M signifie C5, durabilité moyenne. On essaie deux séries d’éprouvettes : l’une en condensation (ISO 6270-1), l’autre en brouillard salin neutre (ISO 9227). Pour les exigences les plus élevées, il existe un essai cyclique.',
                'Le cycle dure une semaine : 72 h d’UV et de condensation (ISO 16474-3), 72 h de brouillard salin et 24 h à −20 °C.',
                'Ensuite, on évalue le cloquage, l’enrouillement, le craquelage et l’écaillage (ISO 4628-2 à -5), la progression de la corrosion depuis la rayure (ISO 4628-8) et l’adhérence (ISO 2409 ou ISO 4624).',
            ],
             'data': [
                 ('C3-H', 'Condensation 240 h · brouillard salin 480 h'),
                 ('C4-H', 'Condensation 480 h · brouillard salin 720 h'),
                 ('C5-M', 'Condensation 480 h · brouillard salin 720 h'),
                 ('C5-H', 'Condensation 720 h · brouillard salin 1 440 h, ou 1 680 h en essai cyclique'),
                 ('C5-VH', '2 688 h en essai cyclique (16 cycles)'),
                 ('CX (ISO 12944-9)', '4 200 h en essai cyclique (25 cycles)'),
             ],
             'note': 'Les deux essais sont nécessaires : des heures de brouillard salin seules ne prouvent aucune durabilité.'},
            # ---------------------------------------------------------- 11
            {'h2': 'Essais de corrosion et de vieillissement', 'p': [
                'Ce sont des essais accélérés en enceinte. Ils servent à contrôler un système donné par rapport à une référence et à vérifier qu’il respecte ce qui a été convenu. Leurs heures ne se convertissent pas en années de service.',
            ],
             'cards': [
                 ('Brouillard salin · ISO 9227', 'Éprouvettes, en général rayées jusqu’au métal, dans un brouillard continu d’eau salée. Trois variantes : neutre (NSS : 35 °C, chlorure de sodium à 5 %), acétique (AASS : celle qu’exige QUALICOAT pour l’aluminium) et cupro-acétique (CASS, à 50 °C). La norme précise qu’elle ne sert ni à classer des matériaux ni à prédire la tenue à long terme. Édition en vigueur : 2022.'),
                 ('Humidité · ISO 6270', 'De l’eau se condense sur l’éprouvette. Partie 1 : condensation continue sur une face ; partie 2 : en enceinte, en climat constant (40 °C et 100 % d’humidité) ou alterné. Révèle cloques et pertes d’adhérence.'),
                 ('SO₂ (Kesternich) · ISO 22479', 'Humidité chargée de dioxyde de soufre, qui simule les atmosphères industrielles. Cycles de 24 h : 8 h à 40 °C avec SO₂ et 16 h à température ambiante, enceinte ventilée. Remplace l’ISO 3231 et l’ISO 6988, annulées.'),
                 ('Xénon · ISO 16474-2', 'Lumière de lampe au xénon, proche du soleil, avec cycles d’arrosage. QUALICOAT l’utilise 1 000 h pour homologuer les poudres. A remplacé l’ISO 11341.'),
                 ('UV fluorescent · ISO 16474-3', 'Lampes UV, par exemple UVA-340, avec condensation. Fait partie de l’essai cyclique des ISO 12944-6 et -9. Ne reproduit pas tout le spectre solaire.'),
                 ('Exposition naturelle · ISO 2810', 'Éprouvettes en extérieur, directement ou sous verre. C’est la base de « l’essai en Floride » de QUALICOAT et GSB : la vérification réelle de la brillance et de la couleur au fil des ans.'),
             ],
             'note': 'Un rapport d’essai sérieux indique la norme et son édition, le laboratoire, le numéro, les éprouvettes, la durée, les critères et le résultat.'},
            # ---------------------------------------------------------- 12
            {'h2': 'Essais du film : adhérence, épaisseur, brillance et couleur', 'p': [
                'Ce sont les contrôles réalisés sur le film lui-même, en atelier ou en laboratoire.',
            ],
             'data': [
                 ('Quadrillage · ISO 2409', 'On incise un quadrillage jusqu’au métal, on applique un ruban adhésif et on observe ce qui se détache. Classes de 0 (aucun détachement) à 5. QUALICOAT exige 0. Ne s’applique pas au-delà de 250 µm ni aux finitions texturées.'),
                 ('Traction (arrachement) · ISO 4624', 'On colle un plot puis on l’arrache : on obtient l’adhérence en MPa. L’ISO 12944-9 demande au moins 5 MPa avant vieillissement.'),
                 ('Épaisseur · ISO 2808 et ISO 2360', 'L’ISO 2808 regroupe les méthodes de mesure du film, y compris de la poudre non cuite ; l’ISO 2360, la mesure par courants de Foucault sur métal non magnétique, comme l’aluminium. Sur surface grenaillée, l’échantillonnage et l’acceptation suivent l’ISO 19840.'),
                 ('Brillance · ISO 2813', 'Mesurée à 20°, 60° ou 85°, en unités de brillance (GU). QUALICOAT regroupe les poudres en trois catégories à 60° : mat (0–30 GU), satiné (31–70) et brillant (71–100).'),
                 ('Pliage · ISO 1519', 'On plie l’éprouvette peinte sur un mandrin cylindrique et on vérifie si le film se fissure ou se décolle.'),
                 ('Emboutissage · ISO 1520', 'On déforme la tôle peinte avec un poinçon jusqu’à former un dôme, puis on examine le film.'),
                 ('Choc · ISO 6272', 'Une masse tombe sur l’éprouvette ; on vérifie si le film se fissure ou se décolle.'),
                 ('Dureté Buchholz · ISO 2815', 'Un pénétrateur de poids fixe laisse une empreinte ; sa longueur donne la dureté.'),
                 ('Dégradation · ISO 4628', 'Comment on cote les dégâts après un essai : cloquage (-2), enrouillement (-3), craquelage (-4), écaillage (-5), corrosion depuis la rayure (-8) et filiforme (-10).'),
                 ('Couleur · ISO 11664-4', 'Écart de couleur ΔE entre la pièce et la référence, dans l’espace CIELAB. L’ancienne ISO 7724 est annulée depuis 2013.'),
             ],
             'note': 'Contrôles réalisés dans notre atelier : ' + PH('[à confirmer]')},
            # ---------------------------------------------------------- 13
            {'h2': 'Préparation de surface : ISO 8501 et ISO 8503', 'p': [
                'Une bonne part de la vie d’un système dépend de la propreté et de la rugosité de l’acier avant peinture. Ces normes permettent de convenir de degrés vérifiables.',
            ],
             'data': [
                 ('ISO 8501-1', 'Degrés de rouille de l’acier de départ et degrés de préparation : Sa 1 à Sa 3 par projection d’abrasif, St par nettoyage manuel ou mécanique. Sa 2½ correspond à un métal presque blanc ; Sa 3, à un métal blanc. Ils sont décrits par des photos.'),
                 ('ISO 8501-3', 'Degrés P1, P2 et P3 pour les soudures, les arêtes et autres imperfections. Édition 2025. L’ISO 12944-3 exige P3 pour une durabilité haute et très haute en C4, C5 et CX ; l’EN 1090-2 les utilise aussi.'),
                 ('ISO 8503-1', 'Comparateurs pour classer le profil de rugosité après projection de grenaille ou de corindon.'),
             ],
             'note': 'Préparation chez JomaPaint : ' + PH('[grenaillage et degré Sa : à confirmer]')},
            # ---------------------------------------------------------- 14
            {'h2': 'Normes EN de produit et d’exécution', 'p': [
                'Des normes européennes que l’on retrouve dans les cahiers des charges du bâtiment. Ce sont des normes, pas des labels : on les respecte et on le prouve par des essais et des documents.',
            ],
             'data': [
                 ('EN 13438', 'Exigences de performance des revêtements en poudre sur acier galvanisé à chaud ou shérardisé, pour la construction. Ne régit pas le procédé de laquage.'),
                 ('EN 15773', 'Application industrielle de poudre sur acier galvanisé à chaud ou shérardisé : les systèmes duplex. Fixe ce que doivent convenir le client, le galvanisateur, le fournisseur de produits chimiques et l’applicateur, ainsi que la qualité exigée de la galvanisation. Édition 2018.'),
                 ('EN ISO 1461', 'Galvanisation à chaud des pièces fabriquées : propriétés et essais. Ne couvre pas ce qui est appliqué par-dessus. Édition 2022.'),
                 ('EN 12206-1', 'Laquage en poudre de l’aluminium pour l’architecture : prétraitement, poudre, procédé et produit fini. Édition 2021.'),
                 ('EN 1090-2', 'Exécution des structures en acier, traitement de surface compris. Relie le degré de préparation P1 à P3 à la durée de vie prévue de la protection et à la catégorie de corrosivité, que le concepteur indique.'),
                 ('DIN 55633', 'Norme allemande pour la protection de l’acier par systèmes poudre ; ses catégories renvoient à l’ISO 12944-2. La partie 2 traite des systèmes cataphorèse époxy et poudre.'),
             ]},
            # ---------------------------------------------------------- 15
            {'h2': 'Essais du système Marine', 'p': [
                'Marine est le système anticorrosion de Joma : prétraitement par immersion, cataphorèse, primaire et finition en peinture poudre. Son classement est C5-M : environnement C5, comme le front de mer, durabilité moyenne (7 à 15 ans).',
                'Ce n’est pas un système certifié : l’ISO 12944 a été écrite pour les peintures liquides et ne certifie pas les systèmes poudre. Chaque donnée est donc indiquée avec sa norme, son laboratoire et son numéro de rapport.',
                'Pour C5-M, l’ISO 12944-6 exige 720 h de brouillard salin neutre et 480 h de condensation, évaluées selon l’ISO 4628 et par l’adhérence. Les heures ne se convertissent pas en années.',
            ],
             'layers': [
                 ('Peinture poudre', 'Finition dans le RAL choisi. Type de poudre : ' + PH('[polyester : à confirmer]') + ' · ' + PH('[XX] µm')),
                 ('Primaire', PH('[Type : à confirmer]') + ' · ' + PH('[XX] µm')),
                 ('Cataphorèse', 'Primaire par électrodéposition sur toute la surface · ' + PH('[XX] µm')),
                 ('Support', PH('[Acier, galvanisé ou les deux : à confirmer]') + ', prétraité par immersion'),
             ],
             'data': [
                 ('Brouillard salin neutre · UNE-EN ISO 9227', '1 000 h (C5-M exige 720 h) · ' + PH('[rapport à confirmer]')),
                 ('Résultat', PH('[cloquage, enrouillement et progression depuis la rayure selon ISO 4628]')),
                 ('Condensation · ISO 6270-1', PH('[C5-M exige 480 h : rapport à confirmer]')),
                 ('Adhérence · ISO 2409', PH('[classe à confirmer]')),
                 ('Épaisseur totale · ISO 2808', PH('[XX] µm')),
                 ('Laboratoire et n° de rapport', PH('[à confirmer]')),
             ],
             'note': 'Certification QUALISTEELCOAT du système : ' + PH('[à confirmer]')},
            # ---------------------------------------------------------- 16
            {'h2': 'Choisir le système selon l’endroit où va la pièce', 'p': [
                'Repères généraux, d’après les environnements de l’ISO 12944-2. Le système exact dépend du support, de la durabilité demandée et de la poudre ; nous le fixons avec vous.',
            ],
             'cards': [
                 ('Intérieur sec · C1', 'Bureaux, magasins ou écoles chauffés. Une couche de poudre suffit ; l’époxy-polyester convient si la pièce ne voit pas le soleil.'),
                 ('Intérieur avec condensation ou extérieur rural · C2', 'Bâtiments non chauffés, entrepôts, salles de sport ; extérieur peu pollué. En extérieur, une couche de polyester.'),
                 ('Urbain ou littoral à faible salinité · C3', 'Ville, industrie à SO₂ modéré, ateliers humides. Polyester sur un prétraitement soigné ; sur galvanisé, système duplex.'),
                 ('Industriel ou littoral à salinité modérée · C4', 'Usines chimiques, piscines. Sur acier, primaire et finition ; sur galvanisé, une ou deux couches selon la durabilité.'),
                 ('Industrie agressive ou littoral à forte salinité · C5', 'En 1998, C5-I et C5-M. Systèmes multicouches : galvanisé avec primaire et finition, ou cataphorèse, primaire et finition, comme le système Marine C5-M. Demandez les essais du système complet.'),
                 ('Offshore, immersion ou enfoui · CX et Im', 'Systèmes spécifiques, essayés selon l’ISO 12944-9 (CX, Im4) ou l’ISO 12944-6 (Im1 à Im3). À étudier au cas par cas.'),
             ],
             'note': 'Sur aluminium pour l’architecture, QUALICOAT recommande le prétraitement SEASIDE ou la pré-anodisation à partir de C4.'},
            # ---------------------------------------------------------- 17
            {'h2': 'Quoi exiger dans un cahier des charges', 'p': [
                'Ce qu’il vaut mieux demander par écrit à tout applicateur, y compris à nous :',
            ],
             'list': [
                 'Environnement et durabilité : catégorie de corrosivité (C1 à CX, Im) et niveau de durabilité (L, M, H ou VH), avec l’édition de la norme. Par exemple, C5-H selon l’ISO 12944-2:2017.',
                 'Support : acier ; acier galvanisé à chaud, en continu ou électrozingué ; ou aluminium.',
                 'Préparation : prétraitement chimique ou degré de grenaillage (ISO 8501-1), et degré des soudures et arêtes (ISO 8501-3).',
                 'Système : nombre de couches, nature de chacune et épaisseur minimale par couche et totale, et méthode de mesure (ISO 2808, ISO 2360 ou ISO 19840).',
                 'Poudre : fabricant, référence et homologation : code P-No. et classe QUALICOAT, ou classe Florida GSB.',
                 'Applicateur : numéro de licence QUALICOAT, QUALISTEELCOAT ou GSB, système couvert et validité. QUALICOAT publie la liste des applicateurs sous licence.',
                 'Essais : rapport avec laboratoire, numéro et date ; norme et édition ; durée ; éprouvettes rayées ou non ; résultat selon l’ISO 4628 et adhérence.',
                 'Brillance : catégorie ou valeur en GU à 60° (ISO 2813).',
                 'Couleur : référence RAL et tolérance ΔE (ISO 11664-4), avec une plaque échantillon validée.',
                 'Garantie : durée en années et conditions, par écrit. La durabilité de l’ISO 12944 n’est pas une garantie.',
             ]},
        ],
        'faq': [
            ('Quelle différence entre une certification et une norme ?', 'Une certification est délivrée par un tiers qui inspecte l’applicateur et fait essayer ses pièces, comme QUALICOAT ou QUALISTEELCOAT ; elle a un numéro et une durée de validité. Une norme, comme l’ISO 12944 ou l’ISO 9227, définit des essais et des exigences ; la conformité se démontre par des rapports d’essai.'),
            ('L’ISO 12944 s’applique-t-elle à la peinture poudre ?', 'Pas directement. L’ISO 12944 vise les peintures qui sèchent à température ambiante et exclut les revêtements en poudre. Un système poudre peut être essayé selon ses méthodes, certifié par QUALISTEELCOAT ou GSB, ou suivre la norme allemande DIN 55633, écrite pour les systèmes poudre sur acier.'),
            ('La classe C5-M existe-t-elle encore ?', 'Oui, avec un autre sens. En 1998, c’était la classe marine ; dans l’ISO 12944-2:2017, C5-I et C5-M ont été regroupées en C5, et la lettre indique désormais la durabilité. Aujourd’hui, C5-M signifie C5 avec une durabilité moyenne (7 à 15 ans) : c’est le classement du système Marine.'),
            ('À combien d’années correspondent 1 000 heures de brouillard salin ?', 'À aucun chiffre précis. L’ISO 9227 elle-même précise que l’essai ne sert pas à prédire la tenue à long terme. Il sert à contrôler un système donné par rapport à une référence.'),
            ('La durabilité de l’ISO 12944 est-elle une garantie ?', 'Non. Les niveaux L, M, H et VH sont une donnée de planification, pas une durée de garantie. La garantie se convient à part, par écrit.'),
            ('Si la poudre est homologuée QUALICOAT, le laquage l’est-il aussi ?', 'Non. L’homologation porte sur la poudre ; le label, sur l’applicateur. Seule une usine sous licence QUALICOAT peut vendre son laquage avec le label. Il en va de même avec GSB.'),
            ('Quelle différence entre QUALICOAT et QUALISTEELCOAT ?', 'QUALICOAT certifie le laquage de l’aluminium pour l’architecture. QUALISTEELCOAT certifie le laquage de l’acier et de l’acier galvanisé, par système et par catégorie de corrosivité, par exemple C5-H.'),
            ('JomaPaint a-t-il une licence QUALICOAT ou QUALISTEELCOAT ?', PH('[Statut chez JomaPaint : à confirmer]')),
            ('L’ISO 9001 de Joma couvre-t-elle la peinture pour des tiers ?', 'Le certificat actuel couvre la conception, la fabrication et la commercialisation de coffres-forts, armoires à clés, boîtes aux lettres et autres boîtes métalliques, pas la peinture pour des tiers. ' + PH('[Extension du périmètre : à confirmer]')),
            ('Puis-je consulter le rapport d’essai du système Marine ?', PH('[Laboratoire, n° de rapport et conditions de communication : à confirmer]')),
        ],
        'faq_n': 7,
    },
}

# Fuentes primarias para la lista «Fuentes» de la página.
_SRC = [
    ('qualicoat-spec', 'https://www.qualicoat.net/main/specifications.html'),
    ('qualicoat-coaters', 'https://www.qualicoat.net/main/about-us/assured-quality/licensed-coaters.html'),
    ('qualicoat-pn', 'https://www.qualicoat.net/main/about-us/assured-quality/approved-and-cancelled-coating-systems-p-n.html'),
    ('qsc-spec', 'https://www.asoc-aluminio.es/sites/default/files/documentos/QUALISTEELCOAT%20Especificaciones%20T%C3%A9cnicas%20V4.3_01.01.2025%20con%20anexos.pdf'),
    ('gsb', 'https://gsb-international.de/en/quality-regulations/'),
    ('iso-cert', 'https://www.iso.org/certification.html'),
    ('iso9001', 'https://www.iso.org/standard/88464.html'),
    ('iso14001', 'https://www.iso.org/standard/14001'),
    ('iso12944-1', 'https://www.iso.org/standard/64833.html'),
    ('iso12944-2', 'https://www.iso.org/standard/64834.html'),
    ('iso12944-6', 'https://www.iso.org/standard/51378.html'),
    ('iso12944-9', 'https://www.iso.org/standard/64832.html'),
    ('iso9227', 'https://www.iso.org/standard/81744.html'),
    ('iso22479', 'https://www.iso.org/standard/73301.html'),
    ('iso8501-1', 'https://www.iso.org/standard/43426.html'),
    ('en15773', 'https://www.evs.ee/en/evs-en-15773-2018'),
    ('en13438', 'https://evs.ee/en/evs-en-13438-2013'),
    ('din55633-2', 'https://www.dinmedia.de/en/standard/din-55633-2/359688287'),
]

_LABELS = {
    'es': {
        'qualicoat-spec': 'QUALICOAT · Especificaciones (26.ª edición)',
        'qualicoat-coaters': 'QUALICOAT · Lista de lacadores con licencia',
        'qualicoat-pn': 'QUALICOAT · Polvos homologados (P-No.)',
        'qsc-spec': 'QUALISTEELCOAT · Especificaciones técnicas v4.3 (AEA)',
        'gsb': 'GSB International · Quality Regulations AL 631 / ST 663',
        'iso-cert': 'ISO · Certificación',
        'iso9001': 'ISO 9001:2026',
        'iso14001': 'ISO 14001:2026',
        'iso12944-1': 'ISO 12944-1:2017 · Introducción y durabilidad',
        'iso12944-2': 'ISO 12944-2:2017 · Clasificación de ambientes',
        'iso12944-6': 'ISO 12944-6:2018 · Ensayos de laboratorio',
        'iso12944-9': 'ISO 12944-9:2018 · Offshore (CX, Im4)',
        'iso9227': 'ISO 9227:2022 · Niebla salina',
        'iso22479': 'ISO 22479:2019 · SO₂ (Kesternich)',
        'iso8501-1': 'ISO 8501-1:2007 · Grados de preparación',
        'en15773': 'EN 15773:2018 · Sistemas dúplex',
        'en13438': 'EN 13438:2013 · Polvo sobre galvanizado',
        'din55633-2': 'DIN 55633-2:2023 · Cataforesis y polvo',
    },
    'eu': {
        'qualicoat-spec': 'QUALICOAT · Zehaztapenak (26. edizioa)',
        'qualicoat-coaters': 'QUALICOAT · Lizentziadun lakatzaileen zerrenda',
        'qualicoat-pn': 'QUALICOAT · Hauts homologatuak (P-No.)',
        'qsc-spec': 'QUALISTEELCOAT · Zehaztapen teknikoak v4.3 (AEA)',
        'gsb': 'GSB International · Quality Regulations AL 631 / ST 663',
        'iso-cert': 'ISO · Ziurtapena',
        'iso9001': 'ISO 9001:2026',
        'iso14001': 'ISO 14001:2026',
        'iso12944-1': 'ISO 12944-1:2017 · Sarrera eta iraunkortasuna',
        'iso12944-2': 'ISO 12944-2:2017 · Giroen sailkapena',
        'iso12944-6': 'ISO 12944-6:2018 · Laborategiko saiakuntzak',
        'iso12944-9': 'ISO 12944-9:2018 · Offshore (CX, Im4)',
        'iso9227': 'ISO 9227:2022 · Gatz-lainoa',
        'iso22479': 'ISO 22479:2019 · SO₂ (Kesternich)',
        'iso8501-1': 'ISO 8501-1:2007 · Prestaketa-mailak',
        'en15773': 'EN 15773:2018 · Sistema duplexak',
        'en13438': 'EN 13438:2013 · Hautsa galbanizatuaren gainean',
        'din55633-2': 'DIN 55633-2:2023 · Kataforesia eta hautsa',
    },
    'fr': {
        'qualicoat-spec': 'QUALICOAT · Spécifications (26e édition)',
        'qualicoat-coaters': 'QUALICOAT · Liste des applicateurs sous licence',
        'qualicoat-pn': 'QUALICOAT · Poudres homologuées (P-No.)',
        'qsc-spec': 'QUALISTEELCOAT · Spécifications techniques v4.3 (AEA)',
        'gsb': 'GSB International · Quality Regulations AL 631 / ST 663',
        'iso-cert': 'ISO · Certification',
        'iso9001': 'ISO 9001:2026',
        'iso14001': 'ISO 14001:2026',
        'iso12944-1': 'ISO 12944-1:2017 · Introduction et durabilité',
        'iso12944-2': 'ISO 12944-2:2017 · Classification des environnements',
        'iso12944-6': 'ISO 12944-6:2018 · Essais de laboratoire',
        'iso12944-9': 'ISO 12944-9:2018 · Offshore (CX, Im4)',
        'iso9227': 'ISO 9227:2022 · Brouillard salin',
        'iso22479': 'ISO 22479:2019 · SO₂ (Kesternich)',
        'iso8501-1': 'ISO 8501-1:2007 · Degrés de préparation',
        'en15773': 'EN 15773:2018 · Systèmes duplex',
        'en13438': 'EN 13438:2013 · Poudre sur galvanisé',
        'din55633-2': 'DIN 55633-2:2023 · Cataphorèse et poudre',
    },
}

SOURCES = {lang: [(_LABELS[lang][k], url) for k, url in _SRC] for lang in ('es', 'eu', 'fr')}
