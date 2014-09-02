from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from . import settings, views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Main level views
    url(r'^$', views.etusivu),
    url(r'^ry/$', views.yhdistys),
    url(r'^palvelut/$', views.palvelut),
    url(r'^jaseneksi/$', views.jaseneksi),
    url(r'^laitteisto/$', views.laitteisto),

    # Sub level views
    url(r'^halutaan/$', views.halutaan),
    url(r'^hakemus/$', views.hakemus),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

