# Web JomaPaint en https://paint.joma.es (VPS JOMA, detrás del Traefik del servidor).
# Se regenera con la URL definitiva para que canonical, hreflang, Open Graph y
# sitemap apunten a paint.joma.es y no a la vista previa de GitHub Pages.
FROM python:3.12-slim AS build
WORKDIR /site
RUN pip install --no-cache-dir jinja2
COPY . .
RUN python3 src/build.py --base https://paint.joma.es/ \
 && rm -rf api src deploy Dockerfile docker-compose.yml package.json package-lock.json README.md .gitignore .nojekyll .github

FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /site /usr/share/nginx/html
