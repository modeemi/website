from django.contrib import admin
from modeemintternet.models import Application, News


class NewsAdmin(admin.ModelAdmin):
    """
    Custom ModelAdmin for News that supports setting user
    for a News object.
    """

    def save_model(self, request, news, form, change):
        news.poster = request.user
        news.save()

admin.site.register(Application)
admin.site.register(News, NewsAdmin)
