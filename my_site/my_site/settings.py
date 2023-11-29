"""
Django settings for my_site project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
# from shop_app import *
from os import getenv
# settings.py
import sentry_sdk
import logging.config




sentry_sdk.init(
    dsn="https://6b9b69c8e27f4bd451eb6d84b77f3b8a@o4506067518750720.ingest.sentry.io/4506067527008256",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY",
    'django-insecure-=cddahi5^u@%uot+-b@p_ty3qc@klow%zu1e6ul$37xrylkpb9',
)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = getenv("DJANGO_DEBUG", "0") == "1"
DEBUG = True

ALLOWED_HOSTS = [
                    '0.0.0.0',
                    "127.0.0.1",
                ] + getenv('DJANGO_ALLOWED_HOSTS', "").split(",")

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS.append('10.0.2.2')
    INTERNAL_IPS.append(
        [ip[:ip.rfind('.')] + '.1' for ip in ips]
    )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    "debug_toolbar",
    'rest_framework',
    'django_filters',
    'drf_spectacular',

    'shop_app.apps.ShopAppConfig',
    'requestdataapp.apps.RequeststartappConfig',
    'my_auth.apps.MyAuthConfig',
    'my_api_app.apps.MyApiAppConfig',
    'blogapp.apps.BlogappConfig',
    'sitemap.apps.SitemapConfig',

    'django.contrib.sitemaps',

]

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.locale.LocaleMiddleware',
    'requestdataapp.middlewares.set_useragent_on_request_middleware',
    'requestdataapp.middlewares.CountRequestMiddleware',
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = 'my_site.urls'

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

WSGI_APPLICATION = 'my_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'c:/boo/bar',
    }
}

CACHE_MIDDLEWARE_SECONDS = 60

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]


LANGUAGES = [
    ('en', ('English')),
    ('ru', ('Russian')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy('my_auth:about')
LOGIN_URL = reverse_lazy('my_auth:login')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

# SPECTACULAR_SETTINGS = {
#     "TITLE": "My site Project API",                     # �������� �������
#     'DESCRIPTION': "MY site shop_app and custom auth",  #
#     'VERSION': '1.0.0',                                 # ������ �������
#     'SERVE_INCLUDE_SCHEMA': False,                      #
# }


LOGGING = {
    'version': 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        },
    },

    'handlers': {
        'console': {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'logfile': {
            "class": "logging.handlers.RotatingFileHandler",
            'filename': BASE_DIR / 'log.txt',
            'maxBytes': 400,
            'backupCount': 3,
            'formatter': "verbose",
        },
    },
    'root': {
        'handlers': [
            'console',
            'logfile',
        ],
        'level': "INFO",
    },
}

LOGLEVEL = getenv("DJANGO_LOGLEVEL", "info").upper()

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(message)s",
        },
    },
    "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
    },
    "loggers": {
            "": {
                "level": LOGLEVEL,
                "handlers": [
                    "console",
                ],
            },
        },
})