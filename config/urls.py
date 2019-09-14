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
    path('ry/saannot/', views.rules, name='rules'),
    path('ry/rekisteriseloste/', views.policy, name='policy'),
    path('ry/hallitus/', views.board, name='board'),
    path('ry/yhteystiedot/', views.contact, name='contact'),

    path('palvelut/', views.services, name='services'),
    path('palvelut/backup/', views.backup, name='backup'),
    path('palvelut/password/', views.password, name='password'),

    path('laitteisto/', views.hardware, name='hardware'),
    path('laitteisto/halutaan/', views.wishlist, name='wishlist'),

    path('jaseneksi/', views.application, name='application'),
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
