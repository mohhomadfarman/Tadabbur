# Production — build Vue SPA and serve via nginx
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
# Origin the SSG build fetches sitemap.xml + public content from at build time
# (the build stage can't reach the internal backend, but has outbound network).
ARG SSG_ORIGIN=https://thetadabbur.org
ENV SSG_ORIGIN=$SSG_ORIGIN
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.frontend.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
