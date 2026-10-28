# Cortelaser · recepción de solicitudes de presupuesto (POST /api/solicitud). Sin dependencias.
FROM node:22-alpine
WORKDIR /app
COPY server.mjs .
RUN mkdir -p /data && chown node:node /data
USER node
ENV NODE_ENV=production PORT=3000 DATA_DIR=/data
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO /dev/null http://127.0.0.1:3000/api/salud || exit 1
CMD ["node", "server.mjs"]
