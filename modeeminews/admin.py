from django.contrib import admin
from .models import News

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, news, form, change):
        news.poster = request.user
        news.save()

admin.site.register(News, NewsAdmin)
