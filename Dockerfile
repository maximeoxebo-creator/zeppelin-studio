# Site Zeppelin Studio : documentation d'Opaline et accuse de reception du
# formulaire de support. Deploye par Coolify sur le VPS OVH.
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY server.js ./
COPY api ./api
COPY site ./site
EXPOSE 3000
USER node
CMD ["node", "server.js"]
