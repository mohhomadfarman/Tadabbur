# Rendertron — headless-Chrome pre-renderer for crawlers.
# Built from the official source (the documented way to run Rendertron) so we
# don't depend on an unmaintained third-party image. Uses Debian's Chromium
# instead of letting Puppeteer download its own.
#
# NOTE: This service is opt-in infrastructure flagged for approval. Test-build
# it (`docker compose build rendertron`) before relying on it in production.
FROM node:18-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git ca-certificates chromium fonts-liberation \
        libnss3 libatk-bridge2.0-0 libgtk-3-0 libasound2 libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app
RUN git clone --depth 1 https://github.com/GoogleChrome/rendertron.git . \
    && npm install \
    && npm run build

# Our render/cache config (overrides the repo default).
COPY config.json /app/config.json

EXPOSE 3000
CMD ["npm", "start"]
