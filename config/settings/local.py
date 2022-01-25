from .base import *  # noqa

DEBUG = True
SECRET_KEY = env("DJANGO_SECRETKEY", default="thisisthedummydjangosecretkey")

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
