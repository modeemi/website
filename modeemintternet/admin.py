# -*- coding: utf-8 -*-

from django.contrib import admin
from modeemintternet.models import News, Soda, Application, Feedback


class NewsAdmin(admin.ModelAdmin):
    """
    Custom admin for News that supports updating posters on post.
    """

    def save_model(self, request, news, form, change):
        news.poster = request.user
        news.save()

class SodaAdmin(admin.ModelAdmin):
    """
    Custom admin view for Soda that supports a compact list view.

    Also supports marking sodas as being in or out of sale in bunch.
    """

    def name_column(self, obj):
        return obj.name
    name_column.short_description = u'Nimi'

    def price_column(self, obj):
        return u'{0}e'.format(obj.price)
    price_column.short_description = u'Hinta'

    def active_column(self, obj):
        return obj.active
    active_column.boolean = True
    active_column.short_description = u'Myynnissä'

    def activate(self, request, queryset):
        queryset.update(active=True)
    activate.short_description = u'Lisää myyntiin'

    def deactivate(self, request, queryset):
        queryset.update(active=False)
    deactivate.short_description = u'Poista myynnistä'

    list_display = ('name_column', 'price_column', 'active_column')
    actions = (activate, deactivate)


admin.site.register(News, NewsAdmin)
admin.site.register(Soda, SodaAdmin)
admin.site.register(Feedback)
admin.site.register(Application)
