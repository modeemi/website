from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework import routers

from modeemintternet import views, apiviews
from modeemintternet.feeds import NewsRSSFeed, NewsICalFeed

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'news', apiviews.NewsViewSet)

urlpatterns = [
    path('sitemap/?', views.sitemap, name='sitemap'),
    path('sitemap.xml/?', views.sitemap, name='sitemap'),

    path('feed/uutiset.rss', NewsRSSFeed(), name='uutiset.rss'),
    path('feed/uutiset.ics', NewsICalFeed(), name='uutiset.ics'),

    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    path('ry/', views.society, name='society'),
    path('ry/saannot/', views.saannot, name='saannot'),
    path('ry/rekisteriseloste/', views.rekisteriseloste, name='rekisteriseloste'),
    path('ry/hallitus/', views.hallitus, name='hallitus'),
    path('ry/yhteystiedot/', views.yhteystiedot, name='yhteystiedot'),

    path('palvelut/', views.palvelut, name='palvelut'),
    path('palvelut/backup/', views.backup, name='backup'),
    path('palvelut/password/', views.password, name='password'),

    path('laitteisto/', views.laitteisto, name='laitteisto'),
    path('laitteisto/halutaan/', views.halutaan, name='halutaan'),

    path('jaseneksi/', views.jaseneksi, name='jaseneksi'),
    path('palaute/', views.palaute, name='palaute'),

    path('uutiset/', views.uutiset, name='uutiset'),
    path('uutiset/<int:pk>/', views.uutiset, name='uutiset'),

    path('tili/sisaan/', auth_views.LoginView.as_view(template_name='tili/sisaan.html'), name='sisaan'),
    path('tili/ulos/', auth_views.LogoutView.as_view(), name='ulos'),
    path('tili/tiedot/', views.kayttajatiedot, name='kayttajatiedot'),
    path('tili/paivita/', views.kayttajatiedot_paivita, name='kayttajatiedot_paivita'),
    path('tili/rekisteri/', views.kayttajarekisteri, name='kayttajarekisteri'),
    path('tili/rekisteri/listat/', views.kayttajarekisteri_listat, name='kayttajarekisteri_listat'),
    path('tili/rekisteri/jasenmaksut/', views.kayttajarekisteri_jasenmaksut, name='kayttajarekisteri_jasenmaksut'),
    path('tili/rekisteri/<str:username>/', views.kayttajarekisteri_paivita, name='kayttajarekisteri_paivita'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]
