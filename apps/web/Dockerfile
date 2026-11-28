# Build context: repository root (npm workspaces).
FROM node:22-alpine AS build
WORKDIR /repo
COPY package.json package-lock.json tsconfig.base.json ./
COPY apps/api/package.json apps/api/
COPY apps/web/package.json apps/web/
RUN npm ci -w @talentscout/web --include-workspace-root --no-audit --no-fund
COPY apps/web apps/web
RUN npm run build -w @talentscout/web

# Alpine's own nginx package gets security fixes sooner than the nginx.org builds in the
# nginx-unprivileged image (CVE-2026-113425 and others were fixed in Alpine 1.30.7-r0 first).
FROM alpine:3.24 AS runtime
RUN apk upgrade --no-cache \
 && apk add --no-cache nginx \
 && rm -f /etc/nginx/http.d/default.conf \
 && sed -i '/^user /d' /etc/nginx/nginx.conf \
 && mkdir -p /run/nginx /usr/share/nginx/html \
 && chown -R nginx:nginx /run/nginx /var/lib/nginx /var/log/nginx \
 && ln -sf /dev/stdout /var/log/nginx/access.log \
 && ln -sf /dev/stderr /var/log/nginx/error.log
COPY apps/web/nginx.conf /etc/nginx/http.d/default.conf
COPY --from=build /repo/apps/web/dist /usr/share/nginx/html
USER nginx
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:8080/ >/dev/null || exit 1
CMD ["nginx", "-g", "daemon off;"]
