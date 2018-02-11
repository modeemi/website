# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.core.wsgi import get_wsgi_application

'''
WSGI config for modeemintternet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()
