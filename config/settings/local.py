import os

from .base import *  # noqa

DEBUG = True
SECRET_KEY = env("DJANGO_SECRETKEY", default="thisisthedummydjangosecretkey")

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY", default=None)
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY", default=None)
os.environ.setdefault(
    "RECAPTCHA_DISABLE",
    "True" if not (RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY) else "",
)
