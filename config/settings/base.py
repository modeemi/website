"""
Django settings for modeemintternet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
"""

import warnings

import environ


PROJECT_ROOT = environ.Path(__file__) - 3  # type: environ.Path
PROJECT_DIR = PROJECT_ROOT.path('modeemintternet')

env = environ.Env()

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    env.read_env('.env')
    env.read_env('/etc/modeemintternet/env')

DEBUG = env('DJANGO_DEBUG', cast=bool, default=False)
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Mailer settings
EMAIL_HOST = 'mail.modeemi.fi'
EMAIL_SUBJECT_PREFIX = '[Modeemi] '
DEFAULT_FROM_EMAIL = 'Modeemi ryn hallitus <hallitus@modeemi.fi>'

# Sites configuration
SITE_ID = 1

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

DATABASE_ROUTERS = [
    'modeemintternet.routers.Router'
]

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='postgres://modeemi:modeemi@127.0.0.1:5432/modeemi'
    ),
    'modeemiuserdb': env.db(
        'MODEEMIUSERDB_URL',
        default='postgres://modeemiuserdb:modeemiuserdb@127.0.0.1:5432/modeemiuserdb'
    )
}

CACHES = {
    'default': env.cache(default='locmemcache://')
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (
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
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'crispy_forms',
    'rest_framework',
    'snowpenguin.django.recaptcha2',

    'modeemintternet',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
        'django.request': {
            'handlers': ['console'],
            'level': env('DJANGO_REQUEST_LOG_LEVEL', default='INFO'),
        },
    },
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'
