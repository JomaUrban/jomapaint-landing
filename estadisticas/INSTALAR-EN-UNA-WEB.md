# Medir visitas con Umami · instrucciones para cada web

Todas las webs del grupo (JomaPaint, Joma Urban, Normo y Joma) se miden en un único panel: **estadisticas.joma.es**. No usa cookies, así que esto no necesita banner de cookies.

## 1. Pegar el script en el `<head>` de todas las páginas

En el layout común, dentro de `<head>`:

```html
<script defer
  src="https://estadisticas.joma.es/script.js"
  data-website-id="ID-DE-LA-WEB"
  data-domains="DOMINIOS-DE-PRODUCCIÓN"></script>
```

| Web | `data-website-id` | `data-domains` |
|---|---|---|
| Joma Urban | `72937a60-e911-4d1e-bf34-4e358686f870` | `jomaurban.com,www.jomaurban.com` |
| Normo | `7d999b89-c4ff-4e67-83cc-b6f5cd541703` | `normo.es,www.normo.es` |
| Joma | `86cc56b6-fb47-4115-87a9-3eda024bf97d` | `joma.es,www.joma.es` |
| Ekilabs | `f9227910-44f9-4cc7-9834-24ef6ec1fb9b` | `ekilabs.com,www.ekilabs.com` |
| Joma Urban (staging, provisional) | `1272970f-f4e1-4967-9c29-0de23b16aee3` | `staging.jomaurban.com` |

- `data-domains` limita la medición a producción: en staging o en local el script se carga pero no cuenta nada. Por eso se puede poner ya en la web de staging.
- **Astro (Joma Urban):** en el layout base, dentro de `<head>`. Si Astro procesa el `<script>`, añadir `is:inline`:
  ```astro
  <script is:inline defer src="https://estadisticas.joma.es/script.js"
    data-website-id="72937a60-e911-4d1e-bf34-4e358686f870"
    data-domains="jomaurban.com,www.jomaurban.com"></script>
  ```
- **Next.js (Normo):** en el layout raíz, con `next/script`:
  ```tsx
  import Script from 'next/script';
  <Script src="https://estadisticas.joma.es/script.js" strategy="afterInteractive"
    data-website-id="7d999b89-c4ff-4e67-83cc-b6f5cd541703"
    data-domains="normo.es,www.normo.es" />
  ```

## 2. Marcar las acciones

Mismos nombres en todas las webs, para poder compararlas.

**Teléfono y email** (todos los enlaces `tel:` y `mailto:` de la web, con un solo script; va justo después del anterior):

```html
<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="tel:"],a[href^="mailto:"]');if(a&&window.umami)umami.track(a.getAttribute('href').indexOf('tel:')===0?'clic-telefono':'clic-email');});</script>
```

(En Astro, también con `is:inline`.)

**Formulario de contacto o presupuesto:** cuando el envío ha ido bien (no al pulsar el botón):

```js
window.umami && umami.track('solicitud-enviada');
```

y si falla:

```js
window.umami && umami.track('solicitud-error');
```

**Otros (si existen en la web):**

| Acción | Cómo |
|---|---|
| WhatsApp | `data-umami-event="clic-whatsapp"` en el enlace |
| Descargar catálogo o ficha | `data-umami-event="descarga"` y `data-umami-event-archivo="nombre-del-archivo"` |

No se mandan datos personales a los eventos (nombre, email, teléfono, texto del formulario).

## 3. Comprobar

1. En producción, abrir la web y, en el panel, entrar en la web → **En tiempo real**: la visita aparece en unos segundos.
2. En staging no debe aparecer nada.
3. Si no aparece: en el navegador, pestaña Red, `script.js` debe dar 200 y `api/send` debe dar 200 al cargar la página.

Dudas: Jox.
