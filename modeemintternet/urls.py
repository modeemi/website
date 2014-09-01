from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from . import settings, views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.etusivu),
    url(r'^ry/$', views.yhdistys),
    url(r'^yhdistys/$', views.yhdistys),
    url(r'^palvelut/$', views.palvelut),
    url(r'^jaseneksi/$', views.jaseneksi),
    url(r'^laitteisto/$', views.laitteisto),

    # url(r'^en/$', views.index),
    # url(r'^club/$', views.club),
    # url(r'^services/$', views.services),
    # url(r'^join/$', views.join),
    # url(r'^hardware/$', views.hardware),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

