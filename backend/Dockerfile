FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collectstatic only needs Django settings — no live DB or real secrets.
# MONGO_HOST is left unset so MongoEngine skips connecting.
# SECRET_KEY uses a build-time placeholder that is NOT the known default value,
# so the production ImproperlyConfigured guard passes. The real key is injected
# at runtime via .env and never baked into the image.
ARG SECRET_KEY=build-time-placeholder-not-a-real-secret
ENV SECRET_KEY=$SECRET_KEY
RUN python manage.py collectstatic --noinput --settings=config.settings.production

EXPOSE 8000
