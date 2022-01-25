from .local import *  # noqa

MODE_TESTING = True

SECRET_KEY = env("DJANGO_SECRETKEY", default="thisisthedummydjangosecretkey")

# http://www.eatsomecode.com/faster-django-tests

DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_LOGGING = False
THUMBNAIL_DEBUG = False  # sorl
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
