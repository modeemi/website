from django.contrib import admin
from modeemintternet.models import News, Application, Feedback


class NewsAdmin(admin.ModelAdmin):
    """
    Custom ModelAdmin for News that supports setting user
    for a News object.
    """

    def save_model(self, request, news, form, change):
        news.poster = request.user
        news.save()


admin.site.register(News, NewsAdmin)
admin.site.register(Feedback)
admin.site.register(Application)
