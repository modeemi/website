from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from modeemintternet import settings, views, apiviews

router = routers.DefaultRouter()
router.register(r'news', apiviews.NewsViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Main level views
    url(r'^$', views.etusivu),
    url(r'^ry/$', views.yhdistys),
    url(r'^palvelut/$', views.palvelut),
    url(r'^jaseneksi/$', views.jaseneksi),
    url(r'^laitteisto/$', views.laitteisto),
    url(r'^palaute/$', views.palaute),

    url(r'^uutiset/$', views.uutiset),
    url(r'^uutiset/(?P<pk>\d+)/$', views.uutiset),

    # Sub level views
    url(r'^ry/saannot/$', views.saannot),
    url(r'^ry/hallitus/$', views.hallitus),
    url(r'^ry/yhteystiedot/$', views.yhteystiedot),
    url(r'^palvelut/backup/$', views.backup),
    url(r'^palvelut/password/$', views.password),
    url(r'^laitteisto/halutaan/$', views.halutaan),

    url(r'^api/', include(router.urls)),
    url(r'^viitenumero/(?P<username>.+)/$', views.viitenumero),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
