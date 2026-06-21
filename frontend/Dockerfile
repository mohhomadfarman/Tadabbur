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
# The SSG build fetches the live sitemap/content at build time, but Docker can't
# see that changed and would reuse a cached `npm run build`. Passing a unique
# CACHEBUST each deploy invalidates this layer so the prerender always reflects
# currently-published content. (npm install above stays cached.)
ARG CACHEBUST=0
RUN echo "cachebust=$CACHEBUST" && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.frontend.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
