# -*- coding: utf-8 -*-

from .base import *  # noqa

DEBUG = True
SECRET_KEY = env('DJANGO_SECRETKEY', default='thisisthedummydjangosecretkey')
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY', default='thisisthedummyrecaptchapublickey')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY', default='thisisthedummyrecaptchaprivatekey')
