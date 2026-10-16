# JomaPaint · landing

Propuesta de web para **JomaPaint**, la división de termolacado y pintura en polvo para terceros de Joma (Legutio, Álava).

- **Vista previa:** https://jomaurban.github.io/jomapaint-landing/ (ES) · `/eu/` (euskera) · `/fr/` (francés)
- **Estado:** maqueta para revisar con el equipo y con diseño. Los datos pendientes aparecen en azul `[XX]`.
- La vista previa lleva `noindex`: Google no la indexa hasta publicarla en el dominio definitivo.

## Qué incluye

- **Hero** con subida de plano y presupuesto en 24 h, y partículas de polvo animadas.
- **Servicios**: termolacado, cataforesis y sistema Marine, perfiles de aluminio, gran formato, tampografía, serigrafía y grabado láser, montaje y embalaje.
- **Proceso** en cinco estaciones, interactivo.
- **Explorador RAL Classic** con los 213 colores, textura y brillo.
- **Cotizador guiado** en tres pasos. Es una maqueta: todavía no envía datos.
- **Seguimiento de pedido**: vista previa en la portada y página de ejemplo en `seguimiento.html`.
- **Calidad**: Marine C5-M, sellos y fabricantes de polvo.
- **Grupo Joma**: historia, fábrica de Legutio y marcas del grupo.

## Editar y regenerar

Los textos de los tres idiomas están en `src/content.py` y la estructura en `src/page.html.j2`. Después de editar:

```bash
pip install jinja2
python3 src/build.py
```

Para publicar en el dominio definitivo (canonical, hreflang, Open Graph y sitemap con la URL buena, y sin `noindex`):

```bash
python3 src/build.py --base https://DOMINIO-DEFINITIVO/ --index
```

## SEO incluido

- Una URL por idioma (`/`, `/eu/`, `/fr/`) con `hreflang` recíproco y `x-default`. El cambio de idioma va por enlaces, no por JavaScript.
- `title` y `description` por idioma, orientados a búsquedas locales: termolacado, pintura en polvo, lacado, cataforesis, Álava, Vitoria-Gasteiz, Pays basque.
- H1 con la búsqueda principal y el mensaje comercial.
- Datos estructurados schema.org: `LocalBusiness` (JomaPaint), `Organization` (Joma), `WebPage` y `FAQPage`. Solo entran las preguntas que ya tienen respuesta real.
- Open Graph y Twitter Card con imagen por idioma para compartir en LinkedIn o WhatsApp.
- `sitemap.xml`, `robots.txt`, favicon e icono de iOS.
- Todo el texto va en el HTML, sin depender de JavaScript. Imágenes en WebP con medidas y carga diferida.

## Antes de publicar

**Datos pendientes `[XX]`:**
- Cabina, peso máximo y plazo estándar.
- Temperaturas, tiempos y espesores de cada estación.
- Tamaño máximo de archivo y hora de corte.
- Pedido mínimo, validez del presupuesto, recogidas y entregas, y política de reproceso.
- Zonas de servicio.
- Condiciones para Francia.

**Revisiones:**
- **Textos en euskera y francés:** son borradores y necesitan revisión nativa.
- **Qualisteelcoat:** se muestra en gris con asterisco. Antes de publicar el logo hay que confirmar con QUALISTEELCOAT que puede usarse sin licencia.
- **ISO 9001:2015:** el certificado de Joma (Bureau Veritas, ES150335-1, válido hasta el 17-11-2027) cubre buzones, cajas y armarios. Conviene ampliar el alcance a la pintura para terceros.
- **Marine:** el sistema de capas y las 1.000 h de niebla salina salen de jomaurban.com y de Joma. Hay que confirmar que el servicio a terceros usa el mismo sistema.

**Para que el cotizador funcione:** conectar el formulario a un destino real. Por ejemplo, un lead en Odoo CRM o un email al equipo.

## Imágenes y logotipos

- **Hero y línea de proceso:** del deck interno de JomaPaint.
- **Piezas colgadas y cabina:** Pexels (licencia libre).
- **Nave y pieza terminada:** Unsplash (licencia libre).
- **Línea de cataforesis de Legutio y fotos de marcas:** joma.es y jomaurban.com. La foto de la fábrica está retocada en color.
- **Logotipos de proveedores, sellos y marcas:** pertenecen a sus propietarios. Aquí solo se usan como referencia y hay que confirmarlos antes de publicar.
