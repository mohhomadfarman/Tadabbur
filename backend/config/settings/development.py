from .base import *

DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True

# In dev, Vite's proxy rewrites Host to 'backend:8000', so 'backend' must be allowed.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend']

# Allow self-signed TLS certs for local MinIO in dev.
AWS_S3_VERIFY = False

# More verbose logging in dev
import logging
logging.basicConfig(level=logging.DEBUG)
