# -*- coding: utf-8 -*-
"""Páginas legales: aviso legal, privacidad y cookies (ES / EU / FR).

Datos de la sociedad comprobados con el certificado de situación censal de la
Diputación Foral de Álava (21/10/2026). Los datos registrales (Registro
Mercantil) se añaden en REGISTRO cuando se tengan; mientras es None no se
muestran.
"""

UPDATED = {'es': '21 de octubre de 2026', 'eu': '2026ko urriaren 21a', 'fr': '21 octobre 2026'}

OWNER = 'José María Gallastegui y Compañía, S.A.'
CIF = 'A20029674'
ADDRESS = {
    'es': 'C/ San Bartolomé 11, Pol. Ind. Goiain, 01170 Legutio (Araba/Álava), España',
    'eu': 'San Bartolomé kalea 11, Goiain industrialdea, 01170 Legutio (Araba), Espainia',
    'fr': 'C/ San Bartolomé 11, Pol. Ind. Goiain, 01170 Legutio (Álava), Espagne',
}
PHONE = '+34 945 31 87 70'
MAIL = 'joma@joma.es'
# Datos registrales según Axesor (copia del BORME, sección Álava), 21-10-2026. Confirmar con la escritura.
REGISTRO = {
    'es': 'Registro Mercantil de Álava, tomo 1571, folio 23, sección 8.ª, hoja 17261',
    'eu': 'Arabako Merkataritza Erregistroa, 1571. liburukia, 23. folioa, 8. atala, 17261. orria',
    'fr': 'Registre du commerce (Registro Mercantil) d’Álava, volume 1571, folio 23, section 8, feuille 17261',
}


def _ident(lang):
    lab = {
        'es': ('Razón social', 'CIF', 'Domicilio', 'Teléfono', 'Email', 'Datos registrales'),
        'eu': ('Sozietatearen izena', 'IFZ', 'Helbidea', 'Telefonoa', 'Posta elektronikoa', 'Erregistroko datuak'),
        'fr': ('Raison sociale', 'NIF (CIF)', 'Siège', 'Téléphone', 'E-mail', 'Immatriculation'),
    }[lang]
    rows = [(lab[0], OWNER), (lab[1], CIF), (lab[2], ADDRESS[lang]), (lab[3], PHONE), (lab[4], MAIL)]
    if REGISTRO:
        rows.append((lab[5], REGISTRO[lang]))
    return rows


def pages():
    return [
        {'key': 'aviso',
         'es': {
             'slug': 'aviso-legal/', 'crumb': 'Aviso legal',
             'title': 'Aviso legal | JomaPaint',
             'description': 'Titular de paint.joma.es: José María Gallastegui y Compañía, S.A. (CIF A20029674), Legutio (Álava). Condiciones de uso del sitio.',
             'h1': 'Aviso legal',
             'sections': [
                 {'h2': 'Titular del sitio', 'p': [
                     'En cumplimiento del artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE), te informamos de que paint.joma.es es un sitio web de José María Gallastegui y Compañía, S.A., que ofrece con la marca JomaPaint su servicio de termolacado para otras empresas.'],
                  'data': _ident('es')},
                 {'h2': 'Para qué sirve este sitio', 'p': [
                     'Aquí explicamos el servicio de termolacado y puedes pedirnos presupuesto. Las condiciones de cada encargo (precio, plazo y alcance) son las del presupuesto que te enviamos por escrito.']},
                 {'h2': 'Propiedad intelectual', 'p': [
                     'Los textos, fotografías, logotipos y el diseño del sitio son de José María Gallastegui y Compañía, S.A. o se usan con permiso de sus titulares. Algunas fotografías de sectores proceden de Unsplash y se usan con su licencia. Las marcas de fabricantes de pintura citadas pertenecen a sus titulares.',
                     'No puedes reproducir ni distribuir el contenido con fines comerciales sin nuestra autorización por escrito.']},
                 {'h2': 'Enlaces a otros sitios', 'p': [
                     'Enlazamos a sitios de terceros, como fabricantes de pintura o empresas del grupo, solo a título informativo. No somos responsables de su contenido.']},
                 {'h2': 'Legislación aplicable', 'p': ['Este aviso legal se rige por la legislación española.']},
             ]},
         'eu': {
             'slug': 'lege-oharra/', 'crumb': 'Lege-oharra',
             'title': 'Lege-oharra | JomaPaint',
             'description': 'paint.joma.es webgunearen titularra: José María Gallastegui y Compañía, S.A. (IFZ A20029674), Legutio (Araba). Webgunearen erabilera-baldintzak.',
             'h1': 'Lege-oharra',
             'sections': [
                 {'h2': 'Webgunearen titularra', 'p': [
                     'Informazioaren gizarteko zerbitzuei eta merkataritza elektronikoari buruzko 34/2002 Legearen (LSSI-CE) 10. artikulua betez, jakinarazten dizugu paint.joma.es José María Gallastegui y Compañía, S.A.-ren webgunea dela. Sozietate horrek JomaPaint markarekin eskaintzen du beste enpresentzako termolakatze-zerbitzua.'],
                  'data': _ident('eu')},
                 {'h2': 'Zertarako den webgune hau', 'p': [
                     'Hemen termolakatze-zerbitzua azaltzen dugu, eta aurrekontua eska diezagukezu. Enkargu bakoitzaren baldintzak (prezioa, epea eta irismena) idatziz bidaltzen dizugun aurrekontukoak dira.']},
                 {'h2': 'Jabetza intelektuala', 'p': [
                     'Webguneko testuak, argazkiak, logotipoak eta diseinua José María Gallastegui y Compañía, S.A.-renak dira, edo haien titularren baimenarekin erabiltzen dira. Sektoreetako argazki batzuk Unsplash-ekoak dira, eta haren lizentziarekin erabiltzen dira. Aipatutako pintura-fabrikatzaileen markak haien titularrenak dira.',
                     'Ezin duzu edukia helburu komertzialekin erreproduzitu edo banatu, guk idatziz baimendu gabe.']},
                 {'h2': 'Beste webgune batzuetarako estekak', 'p': [
                     'Hirugarrenen webguneetarako estekak (pintura-fabrikatzaileak edo taldeko enpresak, adibidez) informazio gisa baino ez ditugu jartzen. Ez gara haien edukiaren erantzule.']},
                 {'h2': 'Legeria aplikagarria', 'p': ['Lege-ohar hau Espainiako legeriaren arabera arautzen da.']},
             ]},
         'fr': {
             'slug': 'mentions-legales/', 'crumb': 'Mentions légales',
             'title': 'Mentions légales | JomaPaint',
             'description': 'Éditeur de paint.joma.es : José María Gallastegui y Compañía, S.A. (NIF A20029674), Legutio (Álava, Espagne). Conditions d’utilisation du site.',
             'h1': 'Mentions légales',
             'sections': [
                 {'h2': 'Éditeur du site', 'p': [
                     'Conformément à l’article 10 de la loi espagnole 34/2002 sur les services de la société de l’information et le commerce électronique (LSSI-CE), paint.joma.es est un site de José María Gallastegui y Compañía, S.A., qui propose sous la marque JomaPaint son service de thermolaquage à façon.'],
                  'data': _ident('fr')},
                 {'h2': 'Objet du site', 'p': [
                     'Ce site présente notre service de thermolaquage et vous permet de demander un devis. Les conditions de chaque commande (prix, délai et périmètre) sont celles du devis que nous vous envoyons par écrit.']},
                 {'h2': 'Propriété intellectuelle', 'p': [
                     'Les textes, photographies, logos et la conception du site appartiennent à José María Gallastegui y Compañía, S.A. ou sont utilisés avec l’autorisation de leurs titulaires. Certaines photographies de secteurs proviennent d’Unsplash et sont utilisées selon sa licence. Les marques des fabricants de peinture citées appartiennent à leurs titulaires.',
                     'Toute reproduction ou diffusion du contenu à des fins commerciales sans notre autorisation écrite est interdite.']},
                 {'h2': 'Liens vers d’autres sites', 'p': [
                     'Les liens vers des sites tiers, comme ceux des fabricants de peinture ou des entreprises du groupe, sont fournis à titre d’information. Nous ne sommes pas responsables de leur contenu.']},
                 {'h2': 'Droit applicable', 'p': ['Les présentes mentions légales sont régies par le droit espagnol.']},
             ]}},

        {'key': 'privacidad',
         'es': {
             'slug': 'privacidad/', 'crumb': 'Privacidad',
             'title': 'Política de privacidad | JomaPaint',
             'description': 'Cómo tratamos los datos y planos que nos envías al pedir presupuesto de termolacado en paint.joma.es, y cómo ejercer tus derechos.',
             'h1': 'Política de privacidad',
             'sections': [
                 {'h2': 'Responsable del tratamiento', 'data': _ident('es')},
                 {'h2': 'Qué datos tratamos', 'p': [
                     'Los que nos das al pedir presupuesto: empresa, CIF (opcional), nombre y apellidos, email, teléfono, la descripción de las piezas y los planos o archivos que adjuntes. También los que nos envías por email o nos das por teléfono.']},
                 {'h2': 'Para qué los usamos', 'p': [
                     'Para preparar y enviarte el presupuesto, resolver tus dudas y, si lo aceptas, gestionar el pedido: recepción de las piezas, pintura, recogida y facturación. No tomamos decisiones automatizadas con tus datos.']},
                 {'h2': 'Base legal', 'p': [
                     'Tratamos tus datos para aplicar, a petición tuya, medidas previas a un contrato y, si haces el pedido, para cumplirlo (artículo 6.1.b del Reglamento General de Protección de Datos). Los datos de facturación los conservamos por obligación legal (artículo 6.1.c).']},
                 {'h2': 'Quién accede a ellos', 'p': [
                     'El equipo de JomaPaint y el de administración de Joma. También los proveedores que nos dan el alojamiento web y el sistema de gestión, que actúan como encargados del tratamiento por contrato. No cedemos tus datos a terceros salvo obligación legal.']},
                 {'h2': 'Cuánto tiempo los guardamos', 'p': [
                     'El tiempo necesario para atender tu solicitud y, en su caso, tu pedido. Después, durante los plazos de conservación que exige la ley, como los fiscales y mercantiles.']},
                 {'h2': 'Tus derechos', 'p': [
                     'Puedes pedirnos acceso a tus datos, su rectificación o supresión, la limitación del tratamiento, oponerte a él o pedir la portabilidad. Escríbenos a joma@joma.es o a la dirección de arriba, con el asunto «Protección de datos».',
                     'Si crees que no hemos atendido bien tu solicitud, puedes reclamar ante la Agencia Española de Protección de Datos (www.aepd.es).']},
             ]},
         'eu': {
             'slug': 'pribatutasuna/', 'crumb': 'Pribatutasuna',
             'title': 'Pribatutasun-politika | JomaPaint',
             'description': 'Nola tratatzen ditugun paint.joma.es-en termolakatze-aurrekontua eskatzean bidaltzen dizkiguzun datuak eta planoak, eta nola erabili zure eskubideak.',
             'h1': 'Pribatutasun-politika',
             'sections': [
                 {'h2': 'Tratamenduaren arduraduna', 'data': _ident('eu')},
                 {'h2': 'Zer datu tratatzen ditugun', 'p': [
                     'Aurrekontua eskatzean ematen dizkiguzunak: enpresa, IFZ (aukerakoa), izen-abizenak, posta elektronikoa, telefonoa, piezen deskribapena eta eransten dituzun planoak edo fitxategiak. Baita posta elektronikoz bidaltzen dizkiguzunak edo telefonoz ematen dizkiguzunak ere.']},
                 {'h2': 'Zertarako erabiltzen ditugun', 'p': [
                     'Aurrekontua prestatu eta bidaltzeko, zure zalantzak argitzeko eta, aurrekontua onartzen baduzu, eskaera kudeatzeko: piezak jaso eta margotu, zuk jasotzeko prest utzi eta fakturatu. Ez dugu erabaki automatizaturik hartzen zure datuekin.']},
                 {'h2': 'Lege-oinarria', 'p': [
                     'Zure datuak tratatzen ditugu, zuk eskatuta, kontratu aurreko neurriak aplikatzeko eta, eskaera egiten baduzu, hura betetzeko (Datuak Babesteko Erregelamendu Orokorraren 6.1.b artikulua). Fakturazio-datuak legezko betebeharragatik gordetzen ditugu (6.1.c artikulua).']},
                 {'h2': 'Nork ikusten dituen', 'p': [
                     'JomaPainteko taldeak eta Jomako administrazio-taldeak. Baita web-ostatua eta kudeaketa-sistema ematen dizkiguten hornitzaileek ere, kontratu bidez tratamendu-eragile gisa. Ez diegu zure daturik lagatzen hirugarrenei, legeak hala eskatzen duenean izan ezik.']},
                 {'h2': 'Zenbat denboran gordetzen ditugun', 'p': [
                     'Zure eskaera eta, hala badagokio, zure enkargua kudeatzeko behar den denboran. Gero, legeak eskatzen dituen kontserbazio-epeetan, hala nola zerga- eta merkataritza-epeetan.']},
                 {'h2': 'Zure eskubideak', 'p': [
                     'Zure datuak eskuratzea, zuzentzea edo ezabatzea, tratamendua mugatzea, horren aurka egitea edo datuen eramangarritasuna eska diezagukezu. Idatzi joma@joma.es helbidera edo goiko helbidera, «Datuen babesa» gaiarekin.',
                     'Zure eskaera behar bezala bete ez dugula uste baduzu, erreklamazioa aurkez dezakezu Datuak Babesteko Espainiako Agentzian (www.aepd.es).']},
             ]},
         'fr': {
             'slug': 'confidentialite/', 'crumb': 'Confidentialité',
             'title': 'Politique de confidentialité | JomaPaint',
             'description': 'Comment nous traitons les données et les plans que vous nous envoyez pour un devis de thermolaquage sur paint.joma.es, et comment exercer vos droits.',
             'h1': 'Politique de confidentialité',
             'sections': [
                 {'h2': 'Responsable du traitement', 'data': _ident('fr')},
                 {'h2': 'Données traitées', 'p': [
                     'Celles que vous nous communiquez pour demander un devis : entreprise, numéro d’identification fiscale (facultatif), nom et prénom, e-mail, téléphone, description des pièces et plans ou fichiers joints. Ainsi que celles que vous nous envoyez par e-mail ou nous donnez par téléphone.']},
                 {'h2': 'Finalités', 'p': [
                     'Préparer et vous envoyer le devis, répondre à vos questions et, si vous l’acceptez, gérer la commande : réception des pièces, thermolaquage, retrait et facturation. Nous ne prenons aucune décision automatisée à partir de vos données.']},
                 {'h2': 'Base juridique', 'p': [
                     'Nous traitons vos données pour exécuter, à votre demande, des mesures précontractuelles et, si vous passez commande, pour exécuter le contrat (article 6.1.b du Règlement général sur la protection des données). Les données de facturation sont conservées en vertu d’une obligation légale (article 6.1.c).']},
                 {'h2': 'Destinataires', 'p': [
                     'L’équipe de JomaPaint et le service administratif de Joma, ainsi que nos prestataires d’hébergement web et de système de gestion, qui agissent en tant que sous-traitants sous contrat. Nous ne cédons pas vos données à des tiers, sauf obligation légale.']},
                 {'h2': 'Durée de conservation', 'p': [
                     'Le temps nécessaire pour traiter votre demande et, le cas échéant, votre commande. Ensuite, pendant les durées de conservation imposées par la loi, notamment en matière fiscale et commerciale.']},
                 {'h2': 'Vos droits', 'p': [
                     'Vous pouvez demander l’accès à vos données, leur rectification ou leur effacement, la limitation du traitement, vous y opposer ou demander leur portabilité. Écrivez-nous à joma@joma.es ou à l’adresse ci-dessus, avec l’objet « Protection des données ».',
                     'Si vous estimez que votre demande n’a pas été correctement traitée, vous pouvez introduire une réclamation auprès de l’autorité espagnole de protection des données, l’AEPD (www.aepd.es).']},
             ]}},

        {'key': 'cookies',
         'es': {
             'slug': 'cookies/', 'crumb': 'Cookies',
             'title': 'Política de cookies | JomaPaint',
             'description': 'paint.joma.es no usa cookies ni herramientas de analítica o seguimiento. Te explicamos qué significa y qué haríamos si eso cambia.',
             'h1': 'Política de cookies',
             'sections': [
                 {'h2': 'No usamos cookies', 'p': [
                     'paint.joma.es no instala cookies ni usa otras tecnologías de seguimiento o analítica. Tampoco carga contenido de terceros que las instale, como fuentes externas, mapas, vídeos o botones de redes sociales. Por eso no te mostramos ningún aviso de cookies.',
                     'Lo que escribes en el formulario de presupuesto se queda en tu navegador hasta que lo envías; no se guarda en él después.']},
                 {'h2': 'Si esto cambia', 'p': [
                     'Si algún día añadimos cookies, actualizaremos esta página y te pediremos consentimiento antes de instalar las que no sean técnicas, como exige la ley.']},
             ]},
         'eu': {
             'slug': 'cookieak/', 'crumb': 'Cookieak',
             'title': 'Cookie-politika | JomaPaint',
             'description': 'paint.joma.es-ek ez du cookierik erabiltzen, ezta analitika- edo jarraipen-tresnarik ere. Zer esan nahi duen eta aldatuz gero zer egingo genukeen.',
             'h1': 'Cookie-politika',
             'sections': [
                 {'h2': 'Ez dugu cookierik erabiltzen', 'p': [
                     'paint.joma.es-ek ez du cookierik instalatzen, ezta jarraipeneko edo analitikako beste teknologiarik erabiltzen ere. Ez du kargatzen cookieak instalatzen dituen hirugarrenen edukirik ere, hala nola kanpoko letra-tipoak, mapak, bideoak edo sare sozialetako botoiak. Horregatik ez dizugu cookie-oharrik erakusten.',
                     'Aurrekontu-formularioan idazten duzuna zure nabigatzailean geratzen da bidali arte; ez da bertan gordetzen gero.']},
                 {'h2': 'Hau aldatzen bada', 'p': [
                     'Noizbait cookieak gehitzen baditugu, orri hau eguneratuko dugu, eta teknikoak ez direnak instalatu aurretik baimena eskatuko dizugu, legeak eskatzen duen bezala.']},
             ]},
         'fr': {
             'slug': 'cookies/', 'crumb': 'Cookies',
             'title': 'Politique de cookies | JomaPaint',
             'description': 'paint.joma.es n’utilise ni cookies ni outils d’analyse ou de suivi. Nous expliquons ce que cela signifie et ce que nous ferions si cela changeait.',
             'h1': 'Politique de cookies',
             'sections': [
                 {'h2': 'Nous n’utilisons pas de cookies', 'p': [
                     'paint.joma.es ne dépose aucun cookie et n’utilise aucune autre technologie de suivi ou d’analyse. Il ne charge pas non plus de contenu tiers qui en déposerait, comme des polices externes, des cartes, des vidéos ou des boutons de réseaux sociaux. C’est pourquoi aucun bandeau cookies ne s’affiche.',
                     'Ce que vous saisissez dans le formulaire de devis reste dans votre navigateur jusqu’à l’envoi ; rien n’y est conservé ensuite.']},
                 {'h2': 'Si cela change', 'p': [
                     'Si nous ajoutons un jour des cookies, nous mettrons cette page à jour et vous demanderons votre consentement avant de déposer ceux qui ne sont pas techniques, comme l’exige la loi.']},
             ]}},
    ]


LEGAL = pages()
