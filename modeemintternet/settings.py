# -*- coding: utf-8 -*-

"""
Django settings for modeemintternet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
"""

import os
import json
import warnings

import environ

from django.core.exceptions import ImproperlyConfigured

PROJECT_ROOT = environ.Path(__file__) - 2  # type: environ.Path
PROJECT_DIR = PROJECT_ROOT.path('modeemintternet')

env = environ.Env()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_env('.env')
    env.read_env('/etc/modeemintternet/env')

# Quick-start settings, check for deployment
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

DEBUG = env('DJANGO_DEBUG', cast=bool, default=False)
TEMPLATE_DEBUG = env('DJANGO_TEMPLATE_DEBUG', cast=bool, default=DEBUG)
SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    cast=str,
    default='n8mll7c7zkdsmc0fz=7o9xqry!mzj3i48ggk=e_j0)#^3f-fn_'
)

if not (isinstance(SECRET_KEY, str) and len(SECRET_KEY) >= 42):
    raise ImproperlyConfigured('Django SECRET_KEY is too short {}'.format(len(SECRET_KEY)))

# Version number is mandatory and imported from bower.json
with open(PROJECT_ROOT('bower.json')) as f:
    VERSION_NUMBER = json.loads(f.read()).get('version')

INTERNAL_IPS = (
    '127.0.0.1',
    'localhost',
)

ALLOWED_HOSTS = (
    '127.0.0.1',
    'localhost',
    'modeemi.fi',
    'www.modeemi.fi',
    'beta.modeemi.fi',
    'cherry.modeemi.fi',
    'modeemi.cs.tut.fi',
    'www.modeemi.cs.tut.fi',
)

# Mailer settings
EMAIL_HOST = 'mail.modeemi.fi'

# Application definition
INSTALLED_APPS = (
    # Built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'opbeat.contrib.django',
    'crispy_forms',
    'rest_framework',

    'modeemintternet',
)

MIDDLEWARE = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': TEMPLATE_DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', )
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

ROOT_URLCONF = 'modeemintternet.urls'
WSGI_APPLICATION = 'modeemintternet.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': env.db(default='postgres://modeemi:modeemi@127.0.0.1:5432/modeemi')
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (
    PROJECT_ROOT('vendor'),
    PROJECT_DIR('static'),
)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www//modeemintternet/static'
MEDIA_ROOT = '/var/www/modeemintternet/media'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
