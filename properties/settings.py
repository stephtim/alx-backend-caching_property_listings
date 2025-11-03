"""
Django settings for alx-backend-caching_property_listings project.
"""

import os
from pathlib import Path

# ---------------------------
# BASE DIRECTORIES
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# SECURITY SETTINGS
# ---------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-temp-key')
DEBUG = True
ALLOWED_HOSTS = ['*']

# ---------------------------
# INSTALLED APPS
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_redis',             # Redis cache backend
    'properties',               # Your app
]

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# ROOT URL AND WSGI
# ---------------------------
ROOT_URLCONF = 'alx-backend-caching_property_listings.urls'
WSGI_APPLICATION = 'alx-backend-caching_property_listings.wsgi.application'

# ---------------------------
# DATABASE (PostgreSQL)
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'property_db'),
        'USER': os.environ.get('POSTGRES_USER', 'property_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'property_pass'),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),  # service name in docker-compose.yml
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# ---------------------------
# CACHES (Redis)
# ---------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # service name and port in docker-compose.yml
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ---------------------------
# SESSION CONFIGURATION
# ---------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ---------------------------
# STATIC FILES
# ---------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------
# TIME AND LANGUAGE
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# DEFAULT AUTO FIELD
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
