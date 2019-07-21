from logging import getLogger

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

log = getLogger(__name__)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_env('.env')
    env.read_env('/etc/modeemintternet/env')

DEBUG = False
SECRET_KEY = env('DJANGO_SECRET_KEY')
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

if len(SECRET_KEY) < 18:
    raise ImproperlyConfigured('Django SECRET_KEY is too short, length is {}'.format(len(SECRET_KEY)))

DATABASES = {
    'default': env.db(),
    'modeemiuserdb': env.db('MODEEMIUSERDB_URL'),
}

STATICFILES_STORAGE = env(
    'DJANGO_STATICFILES_STORAGE',
    default='whitenoise.storage.CompressedStaticFilesStorage',
)

STATIC_ROOT = '/var/www/modeemintternet/static'
MEDIA_ROOT = '/var/www/modeemintternet/media'

