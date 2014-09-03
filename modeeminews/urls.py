from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url(r'^$', views.read),
    url(r'^(?P<pk>\d+)/$', views.read),
    url(r'^uusi/$', views.create),
    url(r'^(?P<pk>\d+)/muokkaa/$', views.update),
)

