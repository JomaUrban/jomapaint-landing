# JomaPaint · web

Propuesta de web para **JomaPaint**, la división de termolacado y pintura en polvo para terceros de Joma (Legutio, Álava).

- **Vista previa:** https://jomaurban.github.io/jomapaint-landing/ (ES) · `/eu/` (euskera) · `/fr/` (francés)
- **Estado:** lista para producción (19-10-2026). Sin datos pendientes visibles: lo que falta por confirmar se ha quitado de la web hasta tenerlo.
- **Indexable** desde el 17-10-2026 en GitHub Pages. Cuando se configure el dominio propio en Pages, GitHub redirige solo (301) desde `github.io`.

## Páginas

24 páginas: la portada, cinco páginas de servicio y dos guías técnicas, en tres idiomas.

| Página | ES | EU | FR |
|---|---|---|---|
| Portada | `/` | `/eu/` | `/fr/` |
| Termolacado de piezas y estructuras | `/termolacado-piezas-estructuras/` | `/eu/piezen-eta-egituren-termolakatzea/` | `/fr/thermolaquage-pieces-structures/` |
| Imprimación rica en zinc (C4-H) | `/imprimacion-rica-en-zinc/` | `/eu/zinkez-aberatsa-den-inprimazioa/` | `/fr/primaire-riche-en-zinc/` |
| Lacado de perfiles de aluminio | `/lacado-perfiles-aluminio/` | `/eu/aluminiozko-profilen-lakatzea/` | `/fr/thermolaquage-profiles-aluminium/` |
| Termolacado de acero galvanizado | `/pintura-acero-galvanizado/` | `/eu/altzairu-galbanizatuaren-termolakatzea/` | `/fr/thermolaquage-acier-galvanise/` |
| Grabado láser e impresión UV | `/grabado-laser-impresion-uv/` | `/eu/laser-grabatua-uv-inprimaketa/` | `/fr/gravure-laser-impression-uv/` |
| Guía: Certificaciones | `/certificaciones-pintura-polvo/` | `/eu/hauts-pinturaren-ziurtagiriak/` | `/fr/certifications-peinture-poudre/` |
| Guía: Normas y ensayos | `/normas-ensayos-pintura-polvo/` | `/eu/hauts-pinturaren-arauak-saiakuntzak/` | `/fr/normes-essais-peinture-poudre/` |

Las URL antiguas de cataforesis (`/cataforesis/`, `/eu/kataforesia/`, `/fr/cataphorese/`) redirigen a la imprimación rica en zinc (`noindex` + canonical; se generan en `build.py`, lista `RETIRED`).

`seguimiento.html` es la página de ejemplo del seguimiento de pedido (solo ES, `noindex`). Ahora no se enlaza desde ninguna parte.

### Portada

- **Hero** con subida de plano y presupuesto en 24 h, y partículas de polvo animadas.
- **Servicios**, con enlace a cada página de servicio.
- **Proceso** en cinco estaciones, interactivo.
- **Explorador RAL Classic** con los 216 colores, textura y brillo. La placa es 3D (three.js, `src/ral3d.js`) y se carga al acercarse a la sección:
  - **Mate:** sin reflejos. **Satinado:** reflejo difuso. **Brillo:** barniz con reflejos nítidos de una fila de regletas LED, como un túnel de inspección de pintura, y un haz de luz cálido que cruza la placa. **Texturado:** relieve real con mapa de normales.
  - Los reflejos usan una nave real (HDRI) casi en gris, para no teñir el color RAL. El mate está calibrado contra el valor RAL.
- **Cotizador guiado** en tres pasos. Arranca con una referencia vacía y envía la solicitud por email con FormSubmit (adjuntos hasta 10 MB). El destino está en `FORM_ENDPOINT` (`src/content.py`): marimar@joma.es. Avisa si una pieza supera la cabina (6 × 2 × 0,65 m) o los 165 kg. La entrega es siempre en Legutio, portes no incluidos. El plazo se calcula en horario de oficina (L–V, 7:00–17:00, hora de Madrid).
- **Dónde trabajamos**: zonas de servicio con los núcleos industriales, sin listas de topónimos (Google lo considera *keyword stuffing*). Las mismas zonas van en `areaServed`.
- **Seguimiento de pedido:** oculto. `TRACKING = True` en `src/content.py` lo vuelve a mostrar (sección, menú, enlace del hero y botón final del cotizador).
- **Calidad**: sistema anticorrosivo C4-H para terceros (imprimación rica en zinc en polvo + poliéster en polvo), sellos (ISO 9001, QUALICOAT* y QUALISTEELCOAT C4-H*, con asterisco «en proceso de homologación»), enlaces a las guías y fabricantes de polvo. El sistema Marine C5-M es de los productos de Joma, no del servicio a terceros.
- **Grupo Joma**: historia, fábrica de Legutio y marcas del grupo.

### Páginas de servicio

Cada una explica el servicio con datos contrastados, sin relleno. Todas siguen la misma estructura:

1. Cabecera con foto.
2. Datos clave.
3. Secciones técnicas.
4. Datos de la línea.
5. Preguntas frecuentes.
6. Enlaces al resto de servicios.
7. Contacto.

No llevan JavaScript.

### Guías técnicas

- **Certificaciones:** QUALICOAT (clases 1, 1.5, 2 y 3, SEASIDE), QUALISTEELCOAT, GSB, ISO 9001/14001 y qué pedir en un pliego.
- **Normas y ensayos:** ISO 12944 parte por parte, categorías C1–CX e Im, C5-M frente a C5, horas de ISO 12944-6, niebla salina, humedad, Kesternich, envejecimiento, ensayos de película, ISO 8501/8503, EN 13438, EN 15773, EN 12206-1, EN 1090-2 y ensayos del sistema C4-H.
- Contenido en `src/guides_content.py`; el reparto en dos páginas, en `src/guides.py`. Cada guía lista sus fuentes primarias.
- **Criterio:** ISO 12944 excluye la pintura en polvo; por eso la web habla de «ambientes C5» y nunca de «cumple ISO 12944» ni «certificado».

## Editar y regenerar

- Textos de la portada: `src/content.py`.
- Textos de las páginas de servicio: `src/services.py`.
- Plantillas: `src/page.html.j2` (portada) y `src/service.html.j2` (servicios). Cabecera, barra superior y pie son comunes y están en `src/_head.html.j2`, `src/_topbar.html.j2` y `src/_end.html.j2`.

Después de editar:

```bash
pip install jinja2
python3 src/build.py
```

Para publicar en el dominio definitivo (canonical, hreflang, Open Graph y sitemap con la URL buena):

```bash
python3 src/build.py --base https://DOMINIO-DEFINITIVO/
```

Para una copia de pruebas que Google no indexe: `--noindex`.

La placa 3D se compila aparte (three.js 0.185.1 con esbuild):

```bash
npm install
npm run build:3d   # src/ral3d.js → assets/ral3d.js
```

El build avisa si algún `title` pasa de 62 caracteres o alguna `description` se sale de 110–165.

## SEO incluido

**Arquitectura**
- Una URL por idioma y por servicio, con `hreflang` recíproco entre las tres versiones y `x-default`.
- `sitemap.xml` con las 24 URL y sus alternativas de idioma.
- Enlazado interno: los servicios de la portada y el pie de todas las páginas enlazan a cada servicio. Cada servicio enlaza a los otros cuatro.

**Palabras clave por idioma**
- **ES:** termolacado, pintura en polvo, pintura electrostática, lacado al horno, imprimación rica en zinc, lacado de aluminio, acero galvanizado. Siempre con Vitoria-Gasteiz y Álava.
- **FR:** sous-traitance, thermolaquage à façon, peinture poudre, peinture époxy, primaire riche en zinc, Pays basque. El `title` evita el nombre de un competidor («Thermolaquage Pays Basque»).
- **EU:** termolakatzea (el término correcto para el proceso), hauts-pintura, zinkez aberatsa den inprimazioa, Araba, Gasteiz.

**Datos estructurados (schema.org)**
- **En todas las páginas:**
  - `Organization` (Joma), con JomaPaint como departamento.
  - `LocalBusiness` (JomaPaint), con dirección, coordenadas de la planta y catálogo de servicios enlazado.
  - `WebSite`.
- **En los servicios:** además `Service`, `WebPage`, `BreadcrumbList` y `FAQPage`.
- Solo entran en `FAQPage` las preguntas con respuesta real. Las pendientes `[XX]` se quedan fuera.

**Rendimiento y accesibilidad**
- Fuente Archivo autoalojada: woff2 variable, latin y latin-ext, licencia OFL. Sin Google Fonts.
- Imagen del hero con `srcset` (800, 1200 y 2000 px).
- Todas las imágenes llevan medidas, y las que quedan fuera de pantalla cargan en diferido.
- Las partículas arrancan cuando la página ya ha cargado. En móvil hay menos.
- La rejilla de 216 colores RAL se pinta al acercarse a la sección.
- El texto de las muestras RAL es negro o blanco según el contraste WCAG.
- Open Graph con imagen propia por página e idioma (`assets/og/`).

**Lighthouse móvil**, con un build indexable servido en local sin compresión:

| Página | Rendimiento | Accesibilidad | Buenas prácticas | SEO |
|---|---|---|---|---|
| Portada | 95 | 100 | 100 | 100 |
| Servicios | 99 | 100 | 100 | 100 |

En la vista previa el SEO sale 69 porque lleva `noindex`, y es lo esperado.

## Antes de publicar

**Confirmado el 19-10-2026:** cabina 6 m × 2 m × 650 mm, 165 kg por pieza, espesor habitual 60–80 µm, plazo estándar 1 semana, pedido mínimo 120 €, validez del presupuesto 3 meses, entrega y recogida en Legutio con portes a cargo del cliente, sin enmascarado (las zonas llegan protegidas), Pantone y NCS bajo pedido, taladro de cuelgue Ø 5 mm, urgencias caso a caso, control de espesor, adherencia e inspección visual, conversión sin cromo en aluminio, pretratamiento químico y desgasificado en galvanizado, QUALICOAT y QUALISTEELCOAT en proceso, contacto y formulario a marimar@joma.es.

**Ocultos hasta tener el dato** (no aparecen en la web):
- Etapas y temperatura del pretratamiento; temperatura y tiempo de secado y de polimerizado.
- Preparación del acero y espesor de la imprimación de zinc; informes de ensayo del C4-H (laboratorio y n.º).
- Daños mayores en piezas lacadas (reproceso).
- Perfiles con rotura de puente térmico.
- Marcaje: áreas máximas de láser y UV, formato del logotipo.

**Revisiones:**
- **Textos en euskera y francés:** son borradores y necesitan revisión nativa.
- **Logos QUALICOAT y QUALISTEELCOAT:** archivos originales de qualicoat.net y qualisteelcoat.net, con asterisco «en proceso». Sus reglamentos reservan el logo a los titulares de licencia o a quien tenga autorización escrita: decisión de Joma publicarlos antes.
- **ISO 9001:2015:** el certificado de Joma (Bureau Veritas, ES150335-1, válido hasta el 17-11-2027) cubre buzones, cajas y armarios. La web muestra el sello de Joma sin hablar del alcance.

**Para que el cotizador funcione:** la primera solicitud que llegue a marimar@joma.es trae un email de activación de FormSubmit; hay que pulsarlo una vez.

**Dominio:** cuando Igor asigne el dominio, regenerar con `python3 src/build.py --base https://DOMINIO/` (canonical, hreflang, Open Graph y sitemap) y configurarlo en GitHub Pages.

**Fuera de la web:**
- Ficha de Google Business Profile en Legutio.
- Search Console con el sitemap.
- Enlaces desde joma.es, jomaurban.com y normo.es.
- Altas en directorios industriales.

## Imágenes y logotipos

**Portada**
- **Hero y pretratamiento (línea de proceso):** del deck interno de JomaPaint.
- **Secado (piezas colgadas):** Pexels (licencia libre).
- **Aplicación electrostática en cadena:** [«Цех окраски»](https://commons.wikimedia.org/wiki/File:%D0%A6%D0%B5%D1%85_%D0%BE%D0%BA%D1%80%D0%B0%D1%81%D0%BA%D0%B8_.jpg), de OlgaBook, en Wikimedia Commons, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Recortada y reducida; el crédito va en el pie de foto. Sale un operario reconocible.
- **Polimerizado:** curva de curado orientativa (temperatura en la pieza), gráfico propio. Cambiar por una foto del horno de Legutio en cuanto la haya.
- **Control de calidad (espesor de capa):** [«Ultraschallschichtdickenmessung»](https://commons.wikimedia.org/wiki/File:Ultraschallschichtdickenmessung.jpg), de Grey and red fairy, en Wikimedia Commons, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Recortada y reducida; el crédito va en el pie de foto.
- **Fachada de la fábrica de Legutio:** Joma.
- **Reflejos de la placa 3D:** HDRI [Industrial Workshop Foundry](https://polyhaven.com/a/industrial_workshop_foundry) de Poly Haven (CC0), casi en gris y reducido a 512 × 256 (`assets/env/nave.hdr`).
- **Acabados de la página de termolacado** (`assets/img/acabado-*.webp`): renders de la propia placa 3D.

**Fotos de las marcas**
- **Joma:** instalación Skyline negro mate.
- **Joma Urban:** pérgola y tumbona.
- **Normo:** web nueva, staging de Orygo.
- **JomaPaint:** aplicación de pintura en polvo, de Pexels (Full Blown Coatings, licencia libre).

**Páginas de servicio**
- **Termolacado:** pintura en polvo, del deck interno de JomaPaint.
- **Imprimación rica en zinc:** estructura de acero atornillada, Unsplash (imagen de referencia).
- **Aluminio:** Andrey Soldatov en Unsplash.
- **Galvanizado:** Bernard Hermant en Unsplash.
- **Marcaje:** buzones Joma Skyline con numeración láser.

**Logotipos**
- Favicon: el pájaro de Joma en negro (en blanco con el modo oscuro), para distinguir la pestaña de la web de Joma.
- Joma Urban va en su rojo oficial #E44132.
- QUALICOAT y QUALISTEELCOAT: archivos originales de sus webs, sin modificar.
- Los logotipos de proveedores, sellos y marcas pertenecen a sus propietarios.
