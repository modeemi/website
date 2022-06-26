from logging import getLogger

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

log = getLogger(__name__)

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")

if len(SECRET_KEY) < 18:
    raise ImproperlyConfigured(
        f"Django SECRET_KEY is too short, length is {len(SECRET_KEY)}"
    )

DATABASES = {"default": env.db()}

STATICFILES_STORAGE = env(
    "DJANGO_STATICFILES_STORAGE",
    default="whitenoise.storage.CompressedStaticFilesStorage",
)

STATIC_ROOT = "/var/www/modeemintternet/static"
MEDIA_ROOT = "/var/www/modeemintternet/media"

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
