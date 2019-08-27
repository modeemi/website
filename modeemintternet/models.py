import re
from logging import getLogger
from time import time

from passlib.hash import (
    des_crypt,
    md5_crypt,
    sha256_crypt,
    sha512_crypt,
)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.urls import reverse
from django.utils.timezone import now

log = getLogger(__name__)


def validate_username(username):
    User = get_user_model()
    if not re.match(r'^[a-z]+$', username):
        raise ValidationError('Käyttäjätunnuksen pitää koostua pienistä kirjaimista.')
    try:
        if (
            Passwd.objects.filter(username__iexact=username).exists()
            or User.objects.filter(username__iexact=username).exists()
        ):
            raise ValidationError('Käyttäjätunnus ei ole saatavilla.')
    except Exception as e:
        log.exception('Error in querying passwd objects', exc_info=e)


class News(models.Model):
    title = models.TextField(blank=False)
    text = models.TextField()

    location = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    starts = models.DateTimeField(blank=True, null=True)
    ends = models.DateTimeField(blank=True, null=True)

    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Uutinen'
        verbose_name_plural = 'Uutiset'

    def __str__(self):
        return '{0} (luotu {1} UTC)'.format(self.title, self.posted)

    def get_absolute_url(self):
        return reverse('uutiset', args=[self.id])


class Soda(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=3, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Limu'
        verbose_name_plural = 'Limut'

    def __str__(self):
        return '{0}'.format(self.name)


class MembershipFee(models.Model):
    year = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        validators=[
            MinValueValidator(1975),
            MaxValueValidator(now().year + 1),
        ],
        verbose_name='Vuosi',
    )

    def __str__(self) -> str:
        return str(self.year)

    class Meta:
        ordering = ['-year']
        get_latest_by = ['year']
        verbose_name = 'Jäsenmaksu'
        verbose_name_plural = 'Jäsenmaksut'


class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Käyttäjä')
    fee = models.ManyToManyField(MembershipFee, blank=True, verbose_name='Jäsenmaksut')
    lifetime = models.BooleanField(default=False, verbose_name='Ainaisjäsenyys')

    municipality = models.CharField(max_length=128, blank=True, default='', verbose_name='Kotipaikka')
    key_engineering = models.BooleanField(default=False, verbose_name='Konehuoneen kova-avain')
    key_physical = models.BooleanField(default=False, verbose_name='Kerhohuoneen kova-avain')
    key_virtual = models.BooleanField(default=False, verbose_name='Kerhohuoneen virtuaaliavain')

    def __str__(self) -> str:
        return self.user.username

    def get_fee(self) -> str:
        if self.lifetime:
            return 'Ainaisjäsen'
        try:
            return str(self.fee.latest())
        except MembershipFee.DoesNotExist:
            return ''
    get_fee.short_description = 'Jäsenmaksu'  # type: ignore

    def get_keys(self) -> str:
        keys = []

        if self.key_engineering:
            keys.append('kovo')
        if self.key_physical:
            keys.append('kerhohuone')
        if self.key_virtual:
            keys.append('virtuaalinen')

        return ', '.join(keys).capitalize()
    get_keys.short_description = 'Avaimet'  # type: ignore

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Jäsenyys'
        verbose_name_plural = 'Jäsenyydet'


class Application(models.Model):
    class Shell:
        BASH = '/bin/bash'
        SH = '/bin/sh'
        ZSH = '/bin/zsh'
        TCSH = '/bin/tcsh'
        FALSE = '/bin/false'

        CHOICES = (
            (SH, SH),
            (BASH, BASH),
            (ZSH, ZSH),
            (TCSH, TCSH),
            (FALSE, FALSE)
        )

    # Actual application options
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    municipality = models.CharField(max_length=64)

    username = models.CharField(
        max_length=32,
        validators=[
            validate_username
        ]
    )
    shell = models.CharField(max_length=32, choices=Shell.CHOICES, default=Shell.BASH)
    funet_rules_accepted = models.BooleanField(default=False)
    virtual_key_required = models.BooleanField(default=False)

    # Timestamps
    applied = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Password hashes
    sha512_crypt = models.CharField(max_length=128)
    sha256_crypt = models.CharField(max_length=128)
    des_crypt = models.CharField(max_length=128)
    md5_crypt = models.CharField(max_length=128)

    # Processing status
    application_accepted = models.BooleanField(default=False)
    application_rejected = models.BooleanField(default=False)
    application_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Hakemus'
        verbose_name_plural = 'Hakemukset'

    def __str__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name, self.applied)

    def generate_password_hashes(self, password):
        """
        Refer to passlib documentation for adding new hashers:

            https://pythonhosted.org/passlib/lib/passlib.hash.html
        """

        self.sha512_crypt = sha512_crypt.hash(password)
        self.sha256_crypt = sha256_crypt.hash(password)
        self.md5_crypt = md5_crypt.hash(password)
        self.des_crypt = des_crypt.hash(password)

        self.save()

    @transaction.atomic
    def accept(self):
        if self.application_processed:
            raise ValidationError('Application {} has already been accepted'.format(self.username))

        def get_hash(method):
            return {
                'SHA512': self.sha512_crypt,
                'SHA256': self.sha256_crypt,
                'MD5': self.md5_crypt,
                'DES': self.des_crypt,
            }.get(method, None)

        User = get_user_model()
        user = User.objects.create(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        Membership.objects.create(user=user, municipality=self.municipality)

        group = UserGroup.objects.get(groupname='modeemi')

        passwd = Passwd.objects.create(
            username=self.username,
            uid=Passwd.get_free_uid(),
            gid=group.gid,
            gecos='{} {}'.format(self.first_name, self.last_name),
            home='/home/{}'.format(self.username),
            shell=self.shell,
        )

        UserGroupMember.objects.create(
            username=passwd.username,
            groupname=group.groupname,
        )

        Shadow.objects.create(
            username=passwd.username,
            lastchanged=int(time()) // 86400,
            min=0,
        )

        for f in Format.objects.values_list('format', flat=True):
            h = get_hash(f)
            if h:
                ShadowFormat.objects.create(
                    username=passwd.username,
                    format=f,
                    hash=h,
                    last_updated=now(),
                )

        if self.virtual_key_required:
            group = UserGroup.objects.get(groupname='ovi')
            UserGroupMember.objects.create(
                username=passwd.username,
                groupname=group.groupname,
            )

        self.application_accepted = True
        self.application_processed = True
        self.save()

    @transaction.atomic
    def reject(self):
        if self.application_processed:
            raise ValidationError('Application {} has already been rejected'.format(self.username))

        self.application_rejected = True
        self.application_processed = True
        self.save()


class Feedback(models.Model):
    sender = models.CharField(blank=True, max_length=64)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=False)
    sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Palaute'
        verbose_name_plural = 'Palautteet'

    def __str__(self):
        return '{0} ({1})'.format(self.message[:25], self.sent)  # pylint: disable=unsubscriptable-object


# Existing modeemiuserdb models that have been created manually and previously handled by the custom database router.
# Feel free to rename the models, but don't rename db_table values or field names.
# Do not change model properties unless you know what you are doing, they are used by other programs.


class Format(models.Model):
    format = models.CharField(primary_key=True, max_length=32, db_index=False)
    description = models.TextField(default='')

    class Meta:
        db_table = 'format'


class Passwd(models.Model):
    username = models.CharField(primary_key=True, max_length=64, db_index=False)
    uid = models.IntegerField()
    gid = models.IntegerField()
    gecos = models.CharField(max_length=255)
    home = models.CharField(max_length=255)
    shell = models.CharField(max_length=255, choices=Application.Shell.CHOICES)

    @staticmethod
    def get_free_uid():
        return 1 + Passwd.objects.order_by('uid').last().uid

    class Meta:
        db_table = 'passwd'


class Shadow(models.Model):
    username = models.OneToOneField(
        Passwd,
        db_index=False, db_constraint=False, db_column='username',
        on_delete=models.PROTECT,
        primary_key=True,
    )
    lastchanged = models.IntegerField()
    min = models.IntegerField(default=0)
    max = models.IntegerField(blank=True, null=True)
    warn = models.IntegerField(blank=True, null=True)
    inact = models.IntegerField(blank=True, null=True)
    expire = models.IntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'shadow'


class ShadowFormat(models.Model):
    username = models.ForeignKey(
        Passwd,
        db_index=False, db_constraint=False, db_column='username',
        on_delete=models.PROTECT,
    )
    format = models.ForeignKey(
        Format,
        db_index=False, db_constraint=False, db_column='format',
        on_delete=models.PROTECT,
    )
    hash = models.CharField(max_length=1024)
    last_updated = models.DateTimeField(default=now)

    class Meta:
        db_table = 'shadowformat'
        constraints = [
            models.UniqueConstraint(fields=['username', 'format'], name='shadowformat_username_key'),
        ]


class UserGroup(models.Model):
    groupname = models.CharField(primary_key=True, db_index=False, max_length=64)
    gid = models.IntegerField()

    class Meta:
        db_table = 'usergroup'
        constraints = [
            models.UniqueConstraint(fields=['gid'], name='usergroup_gid_key'),
        ]


class UserGroupMember(models.Model):
    groupname = models.ForeignKey(
        UserGroup,
        db_constraint=False, db_index=False, db_column='groupname',
        on_delete=models.PROTECT,
    )
    username = models.ForeignKey(
        Passwd,
        db_constraint=False, db_index=False, db_column='username',
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'usergroupmember'
