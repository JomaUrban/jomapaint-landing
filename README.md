# JomaPaint · web

Propuesta de web para **JomaPaint**, la división de termolacado y pintura en polvo para terceros de Joma (Legutio, Álava).

- **Vista previa:** https://jomaurban.github.io/jomapaint-landing/ (ES) · `/eu/` (euskera) · `/fr/` (francés)
- **Estado:** maqueta para revisar con el equipo y con diseño. Los datos pendientes aparecen en azul `[XX]`.
- La vista previa lleva `noindex`: Google no la indexa hasta publicarla en el dominio definitivo.

## Páginas

15 páginas: la portada y cuatro páginas de servicio, en tres idiomas.

| Página | ES | EU | FR |
|---|---|---|---|
| Portada | `/` | `/eu/` | `/fr/` |
| Cataforesis y sistema Marine C5-M | `/cataforesis/` | `/eu/kataforesia/` | `/fr/cataphorese/` |
| Lacado de perfiles de aluminio | `/lacado-perfiles-aluminio/` | `/eu/aluminiozko-profilen-lakatzea/` | `/fr/thermolaquage-profiles-aluminium/` |
| Termolacado de acero galvanizado | `/pintura-acero-galvanizado/` | `/eu/altzairu-galbanizatuaren-termolakatzea/` | `/fr/thermolaquage-acier-galvanise/` |
| Grabado láser e impresión UV | `/grabado-laser-impresion-uv/` | `/eu/laser-grabatua-uv-inprimaketa/` | `/fr/gravure-laser-impression-uv/` |

Además, `seguimiento.html` es la página de ejemplo del seguimiento de pedido (solo ES, `noindex`).

### Portada

- **Hero** con subida de plano y presupuesto en 24 h, y partículas de polvo animadas.
- **Servicios**, con enlace a cada página de servicio.
- **Proceso** en cinco estaciones, interactivo.
- **Explorador RAL Classic** con los 213 colores, textura y brillo.
- **Cotizador guiado** en tres pasos. Es una maqueta: todavía no envía datos.
- **Seguimiento de pedido** (vista previa).
- **Calidad**: Marine C5-M, sellos y fabricantes de polvo.
- **Grupo Joma**: historia, fábrica de Legutio y marcas del grupo.

### Páginas de servicio

Cada una explica el servicio con datos contrastados, sin relleno. Todas siguen la misma estructura:

1. Cabecera con foto.
2. Datos clave.
3. Secciones técnicas.
4. Datos de la línea pendientes de confirmar.
5. Preguntas frecuentes.
6. Enlaces al resto de servicios.
7. Contacto.

No llevan JavaScript.

## Editar y regenerar

- Textos de la portada: `src/content.py`.
- Textos de las páginas de servicio: `src/services.py`.
- Plantillas: `src/page.html.j2` (portada) y `src/service.html.j2` (servicios). Cabecera, barra superior y pie son comunes y están en `src/_head.html.j2`, `src/_topbar.html.j2` y `src/_end.html.j2`.

Después de editar:

```bash
pip install jinja2
python3 src/build.py
```

Para publicar en el dominio definitivo (canonical, hreflang, Open Graph y sitemap con la URL buena, y sin `noindex`):

```bash
python3 src/build.py --base https://DOMINIO-DEFINITIVO/ --index
```

El build avisa si algún `title` pasa de 62 caracteres o alguna `description` se sale de 110–165.

## SEO incluido

**Arquitectura**
- Una URL por idioma y por servicio, con `hreflang` recíproco entre las tres versiones y `x-default`.
- `sitemap.xml` con las 15 URL y sus alternativas de idioma.
- Enlazado interno: los servicios de la portada y el pie de todas las páginas enlazan a cada servicio. Cada servicio enlaza a los otros tres.

**Palabras clave por idioma**
- **ES:** termolacado, pintura en polvo, pintura electrostática, lacado al horno, cataforesis, lacado de aluminio, acero galvanizado. Siempre con Vitoria-Gasteiz y Álava.
- **FR:** sous-traitance, thermolaquage à façon, peinture poudre, peinture époxy, cataphorèse, Pays basque. El `title` evita el nombre de un competidor («Thermolaquage Pays Basque»).
- **EU:** termolakatzea (el término correcto para el proceso), hauts-pintura, kataforesia, Araba, Gasteiz.

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
- La rejilla de 213 colores RAL se pinta al acercarse a la sección.
- El texto de las muestras RAL es negro o blanco según el contraste WCAG.
- Open Graph con imagen propia por página e idioma (`assets/og/`).

**Lighthouse móvil**, con un build indexable servido en local sin compresión:

| Página | Rendimiento | Accesibilidad | Buenas prácticas | SEO |
|---|---|---|---|---|
| Portada | 95 | 100 | 100 | 100 |
| Servicios | 99 | 100 | 100 | 100 |

En la vista previa el SEO sale 69 porque lleva `noindex`, y es lo esperado.

## Antes de publicar

**Datos pendientes `[XX]`:**
- Cabina, peso máximo y plazo estándar.
- Temperaturas, tiempos y espesores de cada estación.
- Tamaño máximo de archivo y hora de corte.
- Pedido mínimo, validez del presupuesto, recogidas y entregas, y política de reproceso.
- Zonas de servicio.
- Condiciones para Francia.
- **Cataforesis:** medidas y peso máximo de la cuba, espesor de cataforesis.
- **Aluminio:** longitud máxima de perfil, tipo de pretratamiento y si se lacan perfiles con rotura de puente térmico.
- **Galvanizado:** pasos de preparación, temperatura de precalentamiento y si se chorrea.
- **Marcaje:** áreas máximas de láser y de UV, formato de archivo del logotipo.

**Revisiones:**
- **Textos en euskera y francés:** son borradores y necesitan revisión nativa.
- **Qualisteelcoat:** se muestra en gris con asterisco. Antes de publicar el logo hay que confirmar con QUALISTEELCOAT que puede usarse sin licencia.
- **ISO 9001:2015:** el certificado de Joma (Bureau Veritas, ES150335-1, válido hasta el 17-11-2027) cubre buzones, cajas y armarios. Conviene ampliar el alcance a la pintura para terceros.
- **Marine:** el sistema de capas y las 1.000 h de niebla salina salen de jomaurban.com y de Joma. Hay que confirmar que el servicio a terceros usa el mismo sistema.
- **QUALICOAT (aluminio):** la página de perfiles explica que muchos pliegos de arquitectura lo exigen, sin decir que JomaPaint lo tenga.

**Para que el cotizador funcione:** conectar el formulario a un destino real. Por ejemplo, un lead en Odoo CRM o un email al equipo.

**Fuera de la web:**
- Ficha de Google Business Profile en Legutio.
- Search Console con el sitemap.
- Enlaces desde joma.es, jomaurban.com y normo.es.
- Altas en directorios industriales.

## Imágenes y logotipos

**Portada**
- **Hero y línea de proceso:** del deck interno de JomaPaint.
- **Piezas colgadas y cabina:** Pexels (licencia libre).
- **Nave y pieza terminada:** Unsplash (licencia libre).
- **Fachada de la fábrica de Legutio:** Joma.

**Fotos de las marcas**
- **Joma:** instalación Skyline negro mate.
- **Joma Urban:** pérgola y tumbona.
- **Normo:** web nueva, staging de Orygo.
- **JomaPaint:** aplicación de pintura en polvo, de Pexels (Full Blown Coatings, licencia libre).

**Páginas de servicio**
- **Cataforesis:** línea de cataforesis de Joma (jomaurban.com).
- **Aluminio:** Andrey Soldatov en Unsplash.
- **Galvanizado:** Bernard Hermant en Unsplash.
- **Marcaje:** buzones Joma Skyline con numeración láser.

**Logotipos**
- Joma Urban va en su rojo oficial #E44132.
- Los logotipos de proveedores, sellos y marcas pertenecen a sus propietarios. Aquí solo se usan como referencia y hay que confirmarlos antes de publicar.
