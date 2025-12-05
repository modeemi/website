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
router.register(r"news", apiviews.NewsViewSet)

urlpatterns = [
    path("sitemap/?", views.sitemap, name="sitemap"),
    path("sitemap.xml/?", views.sitemap, name="sitemap"),
    path("feed/uutiset.rss", NewsRSSFeed(), name="news.rss"),
    path("feed/uutiset.ics", NewsICalFeed(), name="news.ics"),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("ry/", views.society, name="society"),
    path("ry/saannot/", views.rules, name="rules"),
    path("ry/saannot/en/", views.rules_en, name="rules_en"),
    path("ry/rekisteriseloste/", views.policy, name="policy"),
    path("ry/hallitus/", views.board, name="board"),
    path("ry/yhteystiedot/", views.contact, name="contact"),
    path("palvelut/", views.services, name="services"),
    path("palvelut/password/", views.password, name="password"),
    path("laitteisto/", views.hardware, name="hardware"),
    path("laitteisto/halutaan/", views.wishlist, name="wishlist"),
    path("jaseneksi/", views.application, name="application"),
    path("palaute/", views.feedback, name="feedback"),
    path("uutiset/", views.news, name="news"),
    path("uutiset/<int:pk>/", views.news, name="news"),
    path(
        "tili/sisaan/",
        auth_views.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path("tili/ulos/", auth_views.LogoutView.as_view(), name="logout"),
    path("tili/tiedot/", views.account_read, name="account_read"),
    path("tili/paivita/", views.account_update, name="account_update"),
    path("tili/salasana/", views.password_update, name="password_update"),
    path("tili/rekisteri/", views.register_read, name="register_read"),
    path("tili/rekisteri/listat/", views.register_emails, name="register_emails"),
    path("tili/rekisteri/jasenmaksut/", views.register_fees, name="register_fees"),
    path(
        "tili/rekisteri/<str:username>/", views.register_update, name="register_update"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [path(r"__debug__/", include(debug_toolbar.urls))]
