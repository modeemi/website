# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from passlib.context import CryptContext

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class News(models.Model):
    title = models.TextField(blank=False)
    text = models.TextField(blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, editable=False, null=True)

    def __unicode__(self):
        return '{0} (luotu {1} UTC)'.format(self.title, self.posted)

    def get_absolute_url(self):
        return reverse('uutiset', args=[self.id])

    class Meta:
        verbose_name = 'Uutinen'
        verbose_name_plural = 'Uutiset'


class Event(models.Model):
    title = models.TextField(blank=False)
    description = models.TextField(blank=True)
    location = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    starts = models.DateTimeField()
    ends = models.DateTimeField(blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, editable=False, null=True)

    def __unicode__(self):
        return '{0} (alkaa {1} UTC)'.format(self.title, self.starts)

    def get_absolute_url(self):
        return reverse('tapahtumat', args=[self.id])

    class Meta:
        verbose_name = 'Tapahtuma'
        verbose_name_plural = 'Tapahtumat'


class Soda(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=3, decimal_places=2)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Limu'
        verbose_name_plural = 'Limut'


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
    funet_rules_accepted = models.BooleanField(blank=False, default=False)

    # Timestamps
    applied = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Bank reference for paying the membership fee
    bank_reference = models.CharField(max_length=6, editable=False)

    # Password hashes
    pbkdf2_sha256 = models.CharField(max_length=128)
    sha512_crypt = models.CharField(max_length=128)
    des_crypt = models.CharField(max_length=128)

    # Processing status
    application_accepted = models.BooleanField(default=False)
    application_rejected = models.BooleanField(default=False)
    application_processed = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name, self.applied)

    def generate_password_hashes(self, password):
        """
        Generate password hashes with SHA512, PBKDF2/SHA-256 and DES crypt.

        Refer to passlib documentation for adding new hashers:

            https://pythonhosted.org/passlib/lib/passlib.hash.html
        """

        password_schemes = ['pbkdf2_sha256', 'sha512_crypt', 'des_crypt']
        pwd_context = CryptContext(schemes=password_schemes)

        self.pbkdf2_sha256 = pwd_context.hash(password, 'pbkdf2_sha256')
        self.sha512_crypt = pwd_context.hash(password, 'sha512_crypt')
        self.des_crypt = pwd_context.hash(password, 'des_crypt')

        self.save()

    def update_bank_reference(self):
        """
        Update the user's bank payment reference number.
        This method has to be called AFTER the object has been saved.

        Reference to:

            https://www.fkl.fi/en/material/publications/Publications/The_reference_number_and_the_check_digit.pdf
        """

        padded = str(self.id).zfill(4)
        multiplicators = (7, 3, 1)
        inverse = map(int, padded[::-1])
        result = sum(multiplicators[i % 3] * x for i, x in enumerate(inverse))
        checksum = str((10 - (result % 10)) % 10)

        self.bank_reference = padded + checksum
        self.save()

        return self.bank_reference

    class Meta:
        verbose_name = 'Hakemus'
        verbose_name_plural = 'Hakemukset'


class Feedback(models.Model):
    sender = models.CharField(blank=True, max_length=64)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=False)
    sent = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0} ({1})'.format(
                self.message[:25]
                , self.sent)

    class Meta:
        verbose_name = 'Palaute'
        verbose_name_plural = 'Palautteet'
