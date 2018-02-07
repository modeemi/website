# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from passlib.context import CryptContext

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class News(models.Model):
    title = models.TextField(blank=False)
    text = models.TextField(blank=True)

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


class Event(models.Model):
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
        verbose_name = 'Tapahtuma'
        verbose_name_plural = 'Tapahtumat'

    def __str__(self):
        return '{0} (alkaa {1} UTC)'.format(self.title, self.starts)

    def get_absolute_url(self):
        return reverse('tapahtumat', args=[self.id])


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
    BASH = '/bin/bash'
    SH = '/bin/sh'
    ZSH = '/bin/zsh'
    TCSH = '/bin/tcsh'
    FALSE = '/bin/false'

    SHELL_OPTIONS = (
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
    primary_nick = models.CharField(max_length=32)
    secondary_nick = models.CharField(max_length=32)
    shell = models.CharField(max_length=32, choices=SHELL_OPTIONS, default=BASH)
    funet_rules_accepted = models.BooleanField(default=False)
    virtual_key_required = models.BooleanField(default=False)

    # Timestamps
    applied = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Password hashes
    pbkdf2_sha256 = models.CharField(max_length=128)
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
        Generate password hashes with SHA512, PBKDF2/SHA-256 and DES crypt.

        Refer to passlib documentation for adding new hashers:

            https://pythonhosted.org/passlib/lib/passlib.hash.html
        """

        password_schemes = ['pbkdf2_sha256', 'sha512_crypt', 'sha256_crypt', 'des_crypt', 'md5_crypt']
        pwd_context = CryptContext(schemes=password_schemes)

        self.pbkdf2_sha256 = pwd_context.hash(password, 'pbkdf2_sha256')
        self.sha512_crypt = pwd_context.hash(password, 'sha512_crypt')
        self.sha256_crypt = pwd_context.hash(password, 'sha256_crypt')
        self.des_crypt = pwd_context.hash(password, 'des_crypt')
        self.md5_crypt = pwd_context.hash(password, 'des_crypt')

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
    shell = models.CharField(max_length=255)

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
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=64)
    format = models.CharField(max_length=32)
    hash = models.CharField(max_length=1024)
    last_updated = models.DateTimeField()

    class Meta:
        db_table = 'shadowformat'
        managed = False


class UserGroup(models.Model):
    groupname = models.CharField(primary_key=True, max_length=64)
    gid = models.IntegerField()

    class Meta:
        db_table = 'usergroup'
        managed = False


class UserGroupMember(models.Model):
    id = models.IntegerField(primary_key=True)
    groupname = models.CharField(max_length=64)
    username = models.CharField(max_length=64)

    class Meta:
        db_table = 'usergroupmember'
        managed = False
