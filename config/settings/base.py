"""
Django settings for modeemintternet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
"""

import datetime
import warnings

import environ

PROJECT_ROOT = environ.Path(__file__) - 3  # type: environ.Path
PROJECT_DIR = PROJECT_ROOT.path("modeemintternet")

env = environ.Env()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_env(".env")

# Custom flags for feature toggles
MODE_TESTING = env("DJANGO_MODE_TESTING", cast=bool, default=False)
MODE_DRY_RUN = env("DJANGO_MODE_DRY_RUN", cast=bool, default=False)

# Custom flags for application features
MODEEMI_SHELL_INACTIVE = env(
    "MODEEMI_SHELL_INACTIVE", cast=str, default="/home/adm/bin/maksa"
)

VERSION = env("SOURCE_COMMIT", cast=str, default="HEAD")

DEBUG = env("DJANGO_DEBUG", cast=bool, default=False)
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", cast=bool, default=False)

SECURE_PROXY_SSL_HEADER = env(
    "DJANGO_SECURE_PROXY_SSL_HEADER", cast=tuple, default=None
)

# Mailer settings
ADMINS = [("Velhot", "root@modeemi.fi")]
EMAIL_HOST = "mail.modeemi.fi"
EMAIL_SUBJECT_PREFIX = "[Modeemi] "
DEFAULT_FROM_EMAIL = "Modeemi ryn hallitus <hallitus@modeemi.fi>"

# Sites configuration
SITE_ID = 1

INTERNAL_IPS = ("127.0.0.1", "localhost")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "modeemi.fi",
    "www.modeemi.fi",
    "beta.modeemi.fi",
    "cherry.modeemi.fi",
    "modeemi.cs.tut.fi",
    "www.modeemi.cs.tut.fi",
]

CSRF_TRUSTED_ORIGINS = ["https://modeemi.fi", "https://www.modeemi.fi"]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://modeemintternet:modeemintternet@127.0.0.1:5432/modeemiuserdb",
    )
}

CACHES = {"default": env.cache(default="locmemcache://")}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = "fi"
TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (PROJECT_DIR("static"),)

STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"
MEDIA_ROOT = "mediafiles"

# Application definition
INSTALLED_APPS = (
    # Built-ins
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "axes",
    "crispy_forms",
    "crispy_bootstrap3",
    "markdownify",
    "rest_framework",
    "modeemintternet",
)

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "modeemintternet.auth.ModeemiUserDBBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 9},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/tili/sisaan/"
LOGIN_REDIRECT_URL = "/tili/tiedot/"
LOGOUT_REDIRECT_URL = "/"

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "axes.middleware.AxesMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": env("DJANGO_TEMPLATE_DEBUG", cast=bool, default=DEBUG),
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": env("DJANGO_LOG_LEVEL", default="INFO")},
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
        },
        "django.request": {
            "handlers": ["console"],
            "level": env("DJANGO_REQUEST_LOG_LEVEL", default="INFO"),
        },
    },
}

AXES_COOLOFF_TIME = datetime.timedelta(minutes=5)
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_META_PRECEDENCE_ORDER = ["HTTP_X_FORWARDED_FOR", "REMOTE_ADDR"]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"
CRISPY_TEMPLATE_PACK = "bootstrap3"

MARKDOWNIFY = {
    "default": {
        "LINKIFY_TEXT": {
            "PARSE_URLS": True,
            "PARSE_EMAIL": True,
        },
        "SKIP_TAGS": ["pre", "code"],
        "MARKDOWN_EXTENSIONS": ["extra", "nl2br"],
        "WHITELIST_TAGS": [
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "br",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "p",
            "pre",
            "strong",
            "table",
            "tbody",
            "td",
            "th",
            "tr",
            "ul",
        ],
    }
}
