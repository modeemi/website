# -*- coding: utf-8 -*-

"""
Django settings for modeemintternet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
"""

from __future__ import unicode_literals

import os
import json
import random
import string
import sys
import warnings

import environ

from django.core.exceptions import ImproperlyConfigured


def get_random_secret(length=42):
    return ''.join(random.choice(string.printable.replace('$', 'S')) for _ in range(length))

PROJECT_ROOT = environ.Path(__file__) - 3  # type: environ.Path
PROJECT_DIR = PROJECT_ROOT.path('modeemintternet')

env = environ.Env()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_env('.env')
    env.read_env('/etc/modeemintternet/env')

# Quick-start settings, check for deployment
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

DEBUG = env('DJANGO_DEBUG', cast=bool, default=True)
SECRET_KEY = env('DJANGO_SECRET_KEY', cast=str, default=get_random_secret())

if not (isinstance(SECRET_KEY, str) and len(SECRET_KEY) >= 42):
    raise ImproperlyConfigured('Django SECRET_KEY is too short {}, type {}'.format(len(SECRET_KEY), type(SECRET_KEY)))

try:
    with open(PROJECT_ROOT('bower.json')) as f:
        VERSION_NUMBER = json.loads(f.read()).get('version')
except Exception as e:
    VERSION_NUMBER = 'EOS'

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30

# Mailer settings
EMAIL_HOST = 'mail.modeemi.fi'
EMAIL_SUBJECT_PREFIX = '[Modeemi] '
DEFAULT_FROM_EMAIL = 'Modeemi ryn hallitus <hallitus@modeemi.fi>'

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
STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = 'mediafiles'

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
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
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
            'debug': env('DJANGO_TEMPLATE_DEBUG', cast=bool, default=DEBUG),
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

CRISPY_TEMPLATE_PACK = 'bootstrap3'

OPBEAT = {
    'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID', cast=str, default=None),
    'APP_ID': env('DJANGO_OPBEAT_APP_ID', cast=str, default=None),
    'SECRET_TOKEN': env('DJANGO_OPBEAT_SECRET_TOKEN', cast=str, default=None),
    'DEBUG': env('DJANGO_OPBEAT_DEBUG', cast=bool, default=False),
}
