# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

from rest_framework import routers

from modeemintternet import views, apiviews
from modeemintternet.feeds import NewsRSSFeed, EventRSSFeed, EventICalFeed

router = routers.DefaultRouter()
router.register(r'news', apiviews.NewsViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Main level views
    url(r'^$', views.etusivu, name='etusivu'),
    url(r'^ry/$', views.yhdistys, name='yhdistys'),
    url(r'^palvelut/$', views.palvelut, name='palvelut'),
    url(r'^jaseneksi/$', views.jaseneksi, name='jaseneksi'),
    url(r'^laitteisto/$', views.laitteisto, name='laitteisto'),
    url(r'^palaute/$', views.palaute, name='palaute'),

    url(r'^uutiset/$', views.uutiset, name='uutiset'),
    url(r'^uutiset/(?P<pk>\d+)/$', views.uutiset, name='uutiset'),

    url(r'^tapahtumat/$', views.tapahtumat, name='tapahtumat'),
    url(r'^tapahtumat/(?P<pk>\d+)/$', views.tapahtumat, name='tapahtumat'),

    # Sub level views
    url(r'^ry/saannot/$', views.saannot, name='saannot'),
    url(r'^ry/rekisteriseloste/$', views.rekisteriseloste, name='rekisteriseloste'),
    url(r'^ry/hallitus/$', views.hallitus, name='hallitus'),
    url(r'^ry/yhteystiedot/$', views.yhteystiedot, name='yhteystiedot'),
    url(r'^palvelut/backup/$', views.backup, name='backup'),
    url(r'^palvelut/password/$', views.password, name='password'),
    url(r'^laitteisto/halutaan/$', views.halutaan, name='halutaan'),

    url(r'^feed/uutiset.rss$', NewsRSSFeed(), name='uutiset.rss'),
    url(r'^feed/tapahtumat.rss$', EventRSSFeed(), name='tapahtumat.rss'),
    url(r'^feed/tapahtumat.ics$', EventICalFeed(), name='tapahtumat.ics'),

    url(r'^api/', include(router.urls)),
    url(r'^viitenumero/(?P<username>.+)/$', views.viitenumero, name='viitenumero'),

    url(r'^sitemap/?$', views.sitemap, name='sitemap'),
    url(r'^sitemap\.xml/?$', views.sitemap, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
