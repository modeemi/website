# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from modeemintternet.models import News, Soda, Application, Feedback
from modeemintternet import mailer


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


class ApplicationAdmin(admin.ModelAdmin):
    """
    Custom admin for approving a membership application.

    Approving an application creates a user from the application.
    """

    def name_column(self, obj):
        return u'{0} {1} ({2})'.format(obj.first_name,
                obj.last_name, obj.primary_nick)
    name_column.short_description = u'Hakijan nimi (nick)'

    def applied_column(self, obj):
        return obj.applied
    applied_column.short_description = u'Hakemus tehty'

    def processed_column(self, obj):
        return obj.application_processed
    processed_column.boolean = True
    processed_column.short_description = u'Hakemus käsitelty'

    def accept(self, request, queryset):
        queryset.update(application_accepted=True,
                        application_rejected=False,
                        application_processed=True)

        for application in queryset:
            # TODO: create actual users, send mail with credentials
            mailer.application_accepted(application)

    accept.short_description = u'Hyväksy valitut hakemukset'

    def reject(self, request, queryset):
        queryset.update(application_rejected=True,
                        application_accepted=False,
                        application_processed=True)

        for application in queryset:
            mailer.application_rejected(application)

    reject.short_description = u'Hylkää valitut hakemukset'

    list_display = ('name_column', 'applied_column', 'processed_column')
    actions = ('accept', 'reject')

admin.site.register(News, NewsAdmin)
admin.site.register(Soda, SodaAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Feedback)
