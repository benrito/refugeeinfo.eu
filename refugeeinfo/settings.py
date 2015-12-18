# -*- coding: utf-8 -*-

"""
Django settings for refugeeinfo project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os
from gettext import gettext as _
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
CACHE_LENGTH = int(os.environ.get('CACHE_LENGTH', 60 * 15))

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        # GeoDjango - Using mysql now, possibly Postres in the future.
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'refugeeinfo',
        'HOST': 'localhost',
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '0v7dglx7%_ani!lq7_v5xpe6uc(=^vobcmhjk4cj-^y%$m68kd')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if 'DATABASE_URL' in os.environ else True
ENABLE_SERVICES = DEBUG or 'ENABLE_SERVICES' in os.environ
CMS_URL = os.environ.get('CMS_URL', 'http://localhost:9090')
CMS_USER = os.environ.get('CMS_USER', 'user')
CMS_PASSWORD = os.environ.get('CMS_PASSWORD', 'password')
CMS_ENVIRONMENT = os.environ.get('CMS_ENVIRONMENT', 'staging')

# Application definition

INSTALLED_APPS = (

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'rest_framework',

    'main',
    'content'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'refugeeinfo.urls'

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

WSGI_APPLICATION = 'refugeeinfo.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
APPEND_SLASH = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'main/templates'),
)

# Parse database configuration from $DATABASE_URL
import dj_database_url

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}


def get_cache():
    try:
        if 'MEMCACHE_SERVERS' not in os.environ and 'MEMCACHEDCLOUD_SERVERS' in os.environ:
            os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHEDCLOUD_SERVERS'].replace(',', ';')

        if 'MEMCACHE_USERNAME' not in os.environ and 'MEMCACHEDCLOUD_USERNAME' in os.environ:
            os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHEDCLOUD_USERNAME']

        if 'MEMCACHE_PASSWORD' not in os.environ and 'MEMCACHEDCLOUD_PASSWORD' in os.environ:
            os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHEDCLOUD_PASSWORD']
        if 'MEMCACHE_SERVERS' in os.environ:
            return {
                'default': {
                    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                    'TIMEOUT': 500,
                    'BINARY': True,
                    'OPTIONS': {'tcp_nodelay': True}
                }
            }
        else:
            return {
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    'LOCATION': 'unique-snowflake',
                }

            }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }


CACHES = get_cache()

"""
This has to be moved to the base sooner or later
"""
LOCATIONS = (
    ('lesvos', _('Lesvos')),
    ('kos', _('Kos')),
    ('athens', _('Athens')),
    ('gevgelija', _('Gevgelija')),
    ('tabanovce', _(u'Tabanovce/Preševo')),
    ('sid', _(u'Šid')),
    ('slavonski-brod', _('Slavonski Brod'))
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# Storages

# Amazon S3 credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Amazon S3 URL
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
CLOUDFRONT_URL = os.environ.get('CLOUDFRONT_URL', 'https://dttv0ybwk2jfe.cloudfront.net/')

# Static files location
STATICFILES_STORAGE = 'refugeeinfo.custom_storages.StaticFilesStorage'

# Default File storage
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

MEDIA_URL = "%s%s/" % (CLOUDFRONT_URL, MEDIAFILES_LOCATION,)
STATIC_URL = CLOUDFRONT_URL


FEEDBACK_URL = os.environ.get("FEEDBACK_URL", "http://goo.gl/forms/NPJVLMbHQt")

"""
Below are links to be hardcoded into the landing page

format of the dictionary:
"<destination parent": [<list of foreign children>]

"""
OVERRIDE_SLUG_LINKS = {
    "serbia": [
        "tabanovce"
    ]
}


try:
    from local_settings import *
except ImportError:
    pass
