# -*- coding: utf-8 -*-

from passlib.hash import sha512_crypt
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class News(models.Model):
    title = models.TextField(blank=False)
    text = models.TextField(blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)
    poster = models.ForeignKey(User, editable=False, null=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.title, self.posted)

    class Meta:
        verbose_name = 'Uutine'
        verbose_name_plural = 'Uutineet'


class Soda(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=3, decimal_places=2)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)

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
    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    reason = models.CharField(max_length=256, blank=True)
    primary_nick = models.CharField(max_length=32)
    secondary_nick = models.CharField(max_length=32)
    shell = models.CharField(max_length=32, choices=SHELL_OPTIONS, default=BASH)
    funet_rules_accepted = models.BooleanField(blank=False, default=False)

    # Timestamps
    applied = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    # Bank reference for paying the membership fee
    bank_reference = models.CharField(max_length=6, editable=False)

    # Password hashes
    sha512 = models.CharField(max_length=128)
    pbkdf2_sha256 = models.CharField(max_length=128)

    # Processing status
    application_accepted = models.BooleanField(default=False)
    application_rejected = models.BooleanField(default=False)
    application_processed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{0} {1} ({2})'.format(self.first_name, self.last_name, self.applied)

    def generate_password_hashes(self, password):
        """
        Generate password hashes with SHA1, SHA-256
        """

        self.sha512 = sha512_crypt.encrypt(password)
        self.pbkdf2_sha256 = make_password(password, hasher='pbkdf2_sha256')

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
        verbose_name = u'Hakemus'
        verbose_name_plural = u'Hakemukset'


class Feedback(models.Model):
    sender = models.CharField(blank=True, max_length=64)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=False)
    sent = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.message[:25], self.sent)

    class Meta:
        verbose_name = u'Palaute'
        verbose_name_plural = u'Palautteet'
