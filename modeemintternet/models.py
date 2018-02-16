# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
from logging import getLogger
from passlib.context import CryptContext
from time import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction, utils
from django.urls import reverse
from django.utils.timezone import now

log = getLogger(__name__)


def validate_username(username):
    if not re.match(r'^[a-z]+$', username):
        raise ValidationError('Käyttäjätunnuksen pitää koostua pienistä kirjaimista.')
    try:
        if Passwd.objects.filter(username__iexact=username).exists():
            raise ValidationError('Käyttäjätunnus ei ole saatavilla.')
    except Exception as e:
        log.exception('Error in querying passwd objects', exc_info=e)


class News(models.Model):
    title = models.TextField(blank=False)
    text = models.TextField(blank=True)

    location = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    starts = models.DateTimeField(blank=True, null=True)
    ends = models.DateTimeField(blank=True, null=True)

    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, editable=False, null=True, on_delete=models.SET_NULL)

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
    username = models.CharField(
        max_length=32,
        validators=[
            validate_username
        ]
    )
    secondary_nick = models.CharField(max_length=32)  # TODO: Remove this after processing current applications
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

        password_schemes = ['pbkdf2_sha256', 'sha512_crypt', 'sha256_crypt', 'des_crypt', 'md5_crypt']
        pwd_context = CryptContext(schemes=password_schemes)

        self.sha512_crypt = pwd_context.hash(password, 'sha512_crypt')
        self.sha256_crypt = pwd_context.hash(password, 'sha256_crypt')
        self.des_crypt = pwd_context.hash(password, 'des_crypt')
        self.md5_crypt = pwd_context.hash(password, 'md5_crypt')

        self.save()

    @transaction.atomic('default')
    @transaction.atomic('modeemiuserdb')
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

    @transaction.atomic('default')
    @transaction.atomic('modeemiuserdb')
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
        return '{0} ({1})'.format(self.message[:25], self.sent)


class Format(models.Model):
    format = models.CharField(primary_key=True, max_length=32)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'format'
        managed = False


class Passwd(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
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
        managed = False


class Shadow(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    lastchanged = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    warn = models.IntegerField()
    inact = models.IntegerField()
    expire = models.IntegerField()
    flags = models.IntegerField()

    class Meta:
        db_table = 'shadow'
        managed = False


class ShadowFormat(models.Model):
    username = models.CharField(max_length=64)
    format = models.CharField(max_length=32)
    hash = models.CharField(max_length=1024)
    last_updated = models.DateTimeField()

    class Meta:
        db_table = 'shadowformat'
        managed = False
        unique_together = ('username', 'format')


class UserGroup(models.Model):
    groupname = models.CharField(primary_key=True, max_length=64)
    gid = models.IntegerField()

    class Meta:
        db_table = 'usergroup'
        managed = False


class UserGroupMember(models.Model):
    groupname = models.CharField(max_length=64)
    username = models.CharField(max_length=64)

    class Meta:
        db_table = 'usergroupmember'
        managed = False
