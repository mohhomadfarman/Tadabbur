from pathlib import Path
from decouple import config
import mongoengine

BASE_DIR = Path(__file__).resolve().parent.parent.parent

_DEFAULT_SECRET = 'dev-secret-key-change-in-production'
SECRET_KEY = config('SECRET_KEY', default=_DEFAULT_SECRET)
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Public-facing site origin (no trailing slash) — used for sitemap/canonical URLs.
SITE_URL = config('SITE_URL', default='https://thetadabbur.org').rstrip('/')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',
    'apps.users',
    'apps.curriculum',
    'apps.lessons',
    'apps.progress',
    'apps.media',
    'apps.library',
    'apps.videos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# SQLite is used ONLY for Django admin panel.
# All API-facing models (users, curriculum, lessons, progress) live in MongoDB.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB via MongoEngine.
# Only connects when MONGO_HOST is set — intentionally skipped during Docker build.
_MONGO_HOST = config('MONGO_HOST', default='')
if _MONGO_HOST:
    mongoengine.connect(
        db=config('MONGO_DB_NAME', default='tadabbur'),
        host=_MONGO_HOST,
        port=config('MONGO_PORT', default=27017, cast=int),
        username=config('MONGO_USERNAME', default=''),
        password=config('MONGO_PASSWORD', default=''),
        authentication_source='admin',
    )

# DRF — custom JWT auth backed by MongoEngine User documents.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.users.auth.MongoJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173'
).split(',')

# MinIO S3 storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('MINIO_ACCESS_KEY', default='')
AWS_SECRET_ACCESS_KEY = config('MINIO_SECRET_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('MINIO_BUCKET_NAME', default='tadabbur-media')
AWS_S3_ENDPOINT_URL = config('MINIO_ENDPOINT', default='http://localhost:9000')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
# Public URL the browser uses to reach MinIO — differs from AWS_S3_ENDPOINT_URL
# inside Docker (where the backend uses the container hostname 'minio').
MINIO_PUBLIC_URL = config('MINIO_PUBLIC_URL', default='http://localhost:9000')

# Celery (wired Phase A, actual jobs added in Phase 3)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# YouTube Data API v3
YOUTUBE_API_KEY    = config('YOUTUBE_API_KEY',    default='')
YOUTUBE_CHANNEL_ID = config('YOUTUBE_CHANNEL_ID', default='')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Silence verbose pymongo internals — they log every query at DEBUG
        # including full document contents (user passwords, emails, etc.)
        'pymongo': {'level': 'WARNING', 'handlers': ['console'], 'propagate': False},
        # Keep Django request logs at INFO
        'django.request': {'level': 'INFO', 'handlers': ['console'], 'propagate': False},
    },
}
