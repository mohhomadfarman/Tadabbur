FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collectstatic only needs Django settings, not a live MongoDB connection.
# MONGO_HOST is intentionally left unset during build so MongoEngine skips connecting.
RUN python manage.py collectstatic --noinput --settings=config.settings.production

EXPOSE 8000
