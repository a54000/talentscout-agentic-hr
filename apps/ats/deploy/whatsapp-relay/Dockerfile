# WhatsApp relay for the ATS reports (TS-EA-14). Uses Debian's Chromium, which also runs on arm64 (M2 Mac).
FROM node:22-bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends chromium fonts-liberation ca-certificates \
 && rm -rf /var/lib/apt/lists/*
ENV PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    RELAY_HOST=0.0.0.0 \
    WWEBJS_SESSION_DIR=/data/wwebjs_session \
    NODE_ENV=production
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund
COPY server.js ./
RUN mkdir -p /data && chown -R node:node /data /app
USER node
EXPOSE 8090
HEALTHCHECK --interval=60s --timeout=5s CMD node -e "fetch('http://127.0.0.1:8090/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "server.js"]
