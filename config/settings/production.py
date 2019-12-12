from logging import getLogger

from django.core.exceptions import ImproperlyConfigured

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

log = getLogger(__name__)

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")

if len(SECRET_KEY) < 18:
    raise ImproperlyConfigured(
        "Django SECRET_KEY is too short, length is {}".format(len(SECRET_KEY))
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

sentry_sdk.init(
    env("SENTRY_DSN", cast=str, default=""), integrations=[DjangoIntegration()]
)
