from logging import getLogger

from django.contrib import admin

from modeemintternet import mailer, models

log = getLogger(__name__)


class NewsAdmin(admin.ModelAdmin):
    """
    Custom admin for News that supports updating posters on post.
    """

    def save_model(self, request, news, form, change):  # pylint: disable=arguments-differ
        news.poster = request.user
        news.save()


class SodaAdmin(admin.ModelAdmin):
    """
    Custom admin view for Soda that supports a compact list view.

    Also supports marking sodas as being in or out of sale in bunch.
    """

    def activate(self, request, queryset):  # pylint: disable=unused-argument
        queryset.update(active=True)

    def deactivate(self, request, queryset):  # pylint: disable=unused-argument
        queryset.update(active=False)

    list_display = ["name", "price", "active"]
    actions = (activate, deactivate)


class MembershipAdmin(admin.ModelAdmin):
    def username(self, membership) -> str:
        return membership.user.username

    username.short_description = "Käyttäjätunnus"  # type: ignore

    list_display = ["username", "municipality", "get_keys", "get_fee"]


class MembershipFeeAdmin(admin.ModelAdmin):
    list_display = ["year"]


class ApplicationAdmin(admin.ModelAdmin):
    """
    Custom admin for approving a membership application.

    Approving an application creates a user from the application.
    """

    def accept(self, request, queryset):  # pylint: disable=unused-argument
        for application in queryset:
            application.accept()

        for application in queryset:
            try:
                mailer.application_accepted(application)
            except Exception as e:
                log.exception("Sending application rejected mail failed", exc_info=e)

    def reject(self, request, queryset):  # pylint: disable=unused-argument
        for application in queryset:
            application.reject()

        for application in queryset:
            try:
                mailer.application_rejected(application)
            except Exception as e:
                log.exception("Sending application accepted mail failed", exc_info=e)

    list_display = [
        "first_name",
        "last_name",
        "username",
        "applied",
        "application_processed",
        "application_accepted",
    ]
    readonly_fields = [
        "application_processed",
        "application_accepted",
        "application_rejected",
    ]
    actions = ["accept", "reject"]
    exclude = ["sha512_crypt", "sha256_crypt", "des_crypt", "md5_crypt"]


class FeedbackAdmin(admin.ModelAdmin):
    def message_column(self, obj):
        return obj.message[:25]

    message_column.short_description = "message"  # type: ignore

    list_display = ["sender", "email", "sent", "message_column"]


class FormatAdmin(admin.ModelAdmin):
    list_display = ["format", "description"]
    readonly_fields = ["format"]


class PasswdAdmin(admin.ModelAdmin):
    list_display = ["username", "uid", "gid", "gecos", "home", "shell"]
    readonly_fields = ["uid", "gid", "home"]
    search_fields = list_display


class ShadowAdmin(admin.ModelAdmin):
    list_display = ["username", "lastchanged"]
    readonly_fields = ["username", "lastchanged"]
    search_fields = list_display


class ShadowFormatAdmin(admin.ModelAdmin):
    list_display = ["username", "format", "last_updated"]
    exclude = ["hash"]
    readonly_fields = ["id", "username", "format", "last_updated"]
    search_fields = list_display


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ["groupname", "gid"]
    readonly_fields = ["groupname", "gid"]
    search_fields = list_display


class UserGroupMemberAdmin(admin.ModelAdmin):
    list_display = ["groupname", "username"]
    readonly_fields = ["groupname", "username"]
    search_fields = list_display


admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Soda, SodaAdmin)
admin.site.register(models.Membership, MembershipAdmin)
admin.site.register(models.MembershipFee, MembershipFeeAdmin)
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)

admin.site.register(models.Format, FormatAdmin)
admin.site.register(models.Passwd, PasswdAdmin)
admin.site.register(models.Shadow, ShadowAdmin)
admin.site.register(models.ShadowFormat, ShadowFormatAdmin)
admin.site.register(models.UserGroup, UserGroupAdmin)
admin.site.register(models.UserGroupMember, UserGroupMemberAdmin)
