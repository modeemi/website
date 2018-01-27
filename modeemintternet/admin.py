# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from modeemintternet.models import News, Event, Soda, Application, Feedback
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
    name_column.short_description = 'Nimi'

    def price_column(self, obj):
        return '{0}e'.format(obj.price)
    price_column.short_description = 'Hinta'

    def active_column(self, obj):
        return obj.active
    active_column.boolean = True
    active_column.short_description = 'Myynnissä'

    def activate(self, request, queryset):
        queryset.update(active=True)
    activate.short_description = 'Lisää myyntiin'

    def deactivate(self, request, queryset):
        queryset.update(active=False)
    deactivate.short_description = 'Poista myynnistä'

    list_display = ('name_column', 'price_column', 'active_column')
    actions = (activate, deactivate)


class ApplicationAdmin(admin.ModelAdmin):
    """
    Custom admin for approving a membership application.

    Approving an application creates a user from the application.
    """

    def name_column(self, obj):
        return '{0} {1} ({2})'.format(obj.first_name,
                obj.last_name, obj.primary_nick)
    name_column.short_description = 'Hakijan nimi (nick)'

    def applied_column(self, obj):
        return obj.applied
    applied_column.short_description = 'Hakemus tehty'

    def processed_column(self, obj):
        return obj.application_processed
    processed_column.boolean = True
    processed_column.short_description = 'Hakemus käsitelty'

    def accept(self, request, queryset):
        queryset.update(application_accepted=True,
                        application_rejected=False,
                        application_processed=True)

        for application in queryset:
            # TODO: create actual users, send mail with credentials
            mailer.application_accepted(application)

    accept.short_description = 'Hyväksy valitut hakemukset'

    def reject(self, request, queryset):
        queryset.update(application_rejected=True,
                        application_accepted=False,
                        application_processed=True)

        for application in queryset:
            mailer.application_rejected(application)

    reject.short_description = 'Hylkää valitut hakemukset'

    list_display = ('name_column', 'applied_column', 'processed_column')
    actions = ('accept', 'reject')


class FeedbackAdmin(admin.ModelAdmin):
    pass


admin.site.register(News, NewsAdmin)
admin.site.register(Event)
admin.site.register(Soda, SodaAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
