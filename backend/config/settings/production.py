from .base import *
from .base import _DEFAULT_SECRET
from decouple import config
from django.core.exceptions import ImproperlyConfigured

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')

# Refuse to start if the default dev secret key is still in use.
if SECRET_KEY == _DEFAULT_SECRET:
    raise ImproperlyConfigured(
        "SECRET_KEY must be set to a unique random value in production. "
        "Generate one with: python -c \"import secrets; print(secrets.token_hex(50))\""
    )

# Security headers for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# SSL terminates at the host nginx reverse proxy; trust its forwarded header
# so Django doesn't see internal HTTP traffic as insecure and infinite-redirect.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
