"""
Django settings for modeemintternet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SETTINGS_DIR = '/etc/modeemintternet'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'modeemintternet')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'my_bestest_secret_key_look_below_for_filesystem_loaders'

try:
    with open(os.path.join(SETTINGS_DIR, 'secret.key'), 'r') as f:
        SECRET_KEY = f.read().strip()
except Exception as e:
    print 'No overriding secret key file found, using default dummy development key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = (
    # Built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom additions
    # 'debug_toolbar',
    'crispy_forms',

    # Own modules
    'modeemintternet',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PREPROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
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
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Templates and static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "vendor"),
    os.path.join(PROJECT_DIR, "static"),
)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/modeemintternet/static'

# LDAP configuration
# This requires that you have the python-ldap module installed

try:
    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType

    with open(os.path.join(SETTINGS_DIR, 'ldap.key'), 'r') as f:
        AUTH_LDAP_BIND_PASSWORD = f.read().strip()

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
