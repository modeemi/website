# -*- coding: utf-8 -*-

"""
Django settings for modeemintternet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
"""

import os
import json

SETTINGS_DIR = '/etc/modeemintternet'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, 'modeemintternet'))

# Quick-start settings, check for deployment
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DummyDevelopmentDjangoSecret'

try:
    with open(os.path.join(SETTINGS_DIR, 'secret.txt'), 'r') as f:
        SECRET_KEY = f.read().strip()
except Exception as e:
    print 'No overriding Django secret key file found, using default dummy development key'

# Version number is mandatory and imported from bower.json
with open(os.path.abspath(os.path.join(__file__, '..', '..', 'bower.json'))) as f:
    VERSION_NUMBER = json.loads(f.read()).get('version')

# SECURITY WARNING: don't run with debug turned on in production!
TEST = os.environ.get('TEST', False)
DEBUG = os.environ.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'modeemi.fi', 'www.modeemi.fi']
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Mailer settings
EMAIL_HOST = 'mail.modeemi.fi'

# Application definition
INSTALLED_APPS = (
    # Custom admin panel
    'suit',

    # Built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Opbeat monitoring
    'opbeat.contrib.django',

    # Custom additions
    'crispy_forms',
    'rest_framework',

    # Own modules
    'modeemintternet',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', )

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'modeemintternet.urls'
WSGI_APPLICATION = 'modeemintternet.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'modeemintternet',
        'USER': 'modeemintternet',
        'PASSWORD': 'modeemintternetonparraim',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Override database with in-memory SQLite if running test mode
if TEST:
    DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory'
    }

try:
    with open(os.path.join(SETTINGS_DIR, 'psql.txt'), 'r') as f:
        DATABASES['default']['PASSWORD'] = f.read().strip()
except Exception as e:
    print 'No overriding PostgreSQL password file found, using default password'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Templates and static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "vendor"),
    os.path.join(PROJECT_DIR, "static"),
)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www//modeemintternet/static'
MEDIA_ROOT = '/var/www/modeemintternet/media'

# LDAP configuration
# This requires that you have the python-ldap module installed

try:
    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType

    try:
        with open(os.path.join(SETTINGS_DIR, 'ldap.txt'), 'r') as f:
            AUTH_LDAP_BIND_PASSWORD = f.read().strip()
    except Exception as e:
        print 'No overriding LDAP secret could be loaded, using default dummy development key'

    # Some example settings, you will probably have to revise these
    CN_BIND = 'web'
    CN_MEMBER = 'jasenet'
    CN_STAFF = 'guru'
    CN_ADMIN = 'hallitus'

    # the primary is the user group, the second marks activity, revise for LDAP DC settings
    DC_PRIMARY = 'modeemi'
    DC_SECONDARY = 'active'

    # LDAP configuration, refer to: http://pythonhosted.org/django-auth-ldap/
    AUTH_LDAP_SERVER_URI = "ldap://ldappest.modeemi.fi"  # please revise for production
    AUTH_LDAP_BIND_DN = "cn={0},dc={1},dc={2}".format(CN_BIND, DC_PRIMARY, DC_SECONDARY)
    AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=People,dc={0},dc={1}".format(DC_PRIMARY, DC_SECONDARY)
    AUTH_LDAP_GROUP_TYPE = PosixGroupType()
    AUTH_LDAP_REQUIRE_GROUP = "cn={0},ou=Group,dc={1},dc={2}".format(CN_STAFF, DC_PRIMARY, DC_SECONDARY)

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Group,dc={0},dc={1}".format(DC_PRIMARY, DC_SECONDARY),
                                        ldap.SCOPE_SUBTREE, "(objectClass=posixAccount)")

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active":    "cn={0},ou=Group,dc={1},dc={2}".format(CN_MEMBER, DC_PRIMARY, DC_SECONDARY),
        "is_staff":     "cn={0},ou=Group,dc={1},dc={2}".format(CN_STAFF,  DC_PRIMARY, DC_SECONDARY),
        "is_superuser": "cn={0},ou=Group,dc={1},dc={2}".format(CN_ADMIN,  DC_PRIMARY, DC_SECONDARY)
    }

    AUTH_LDAP_CACHE_GROUPS = True
    AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600  # or one hour

except Exception as e:
    print e

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django suit configuration for a customized admin panel
SUIT_CONFIG = {
    'ADMIN_NAME': 'modeemintternet - ylläpito',
}

try:
    from modeemintternet.local_settings import *
except ImportError as e:
    print e
    print 'No local settings available, skipping'
