# -*- coding: utf-8 -*-

import os
import raven
from logging import getLogger

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

log = getLogger(__name__)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_env('.env')
    env.read_env('/etc/modeemintternet/env')

DEBUG = False
SECRET_KEY = env('DJANGO_SECRET_KEY', cast=str)

if len(SECRET_KEY) < 42:
    raise ImproperlyConfigured('Django SECRET_KEY is too short, length is {}'.format(len(SECRET_KEY)))

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': env.db()
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATIC_ROOT = '/var/www/modeemintternet/static'
MEDIA_ROOT = '/var/www/modeemintternet/media'

try:
    RAVEN_CONFIG = {
        'dsn': env('RAVEN_DSN'),
        'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
    }
except Exception as e:
    log.error(e)
