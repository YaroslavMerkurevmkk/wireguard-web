import json
from pathlib import Path

from core.utils import get_default_interface

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "config.json", "r", encoding="utf-8") as conf_file:
    config = json.load(conf_file)

SECRET_KEY = config.get("SECRET_KEY")
DEBUG = config.get("DEBUG", False)

ALLOWED_HOSTS = config.get("ALLOWED_HOSTS", [])
CSRF_TRUSTED_ORIGINS = config.get("CSRF_TRUSTED_ORIGINS", [])

INSTALLED_APPS = [
    'wireguard.apps.WireguardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SERVER_IP, SERVER_INTERFACE = get_default_interface()

WG_DIR = config.get("WIREGUARD_DIR", None)
WG_DIR = WG_DIR if WG_DIR else None

WG_PORT = config.get("WIREGUARD_DIR", None)
WG_PORT = WG_PORT if WG_PORT else None
