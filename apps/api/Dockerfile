# Build context: repository root (npm workspaces).
FROM node:22-alpine AS build
WORKDIR /repo
COPY package.json package-lock.json tsconfig.base.json ./
COPY apps/api/package.json apps/api/
COPY apps/web/package.json apps/web/
RUN npm ci -w @talentscout/api --include-workspace-root --no-audit --no-fund
COPY apps/api apps/api
RUN npm run build -w @talentscout/api

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps/api/package.json apps/api/
COPY apps/web/package.json apps/web/
RUN npm ci -w @talentscout/api --omit=dev --no-audit --no-fund && npm cache clean --force
COPY --from=build /repo/apps/api/dist apps/api/dist
USER node
EXPOSE 4000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:4000/api/v1/health || exit 1
CMD ["node", "apps/api/dist/server.js"]
