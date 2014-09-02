# -*- coding: utf-8 -*-

from time import sleep
from django.db import models
from django.db.models.signals import post_save

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

    applied = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    bank_reference = models.CharField(max_length=16, editable=False)

    email = models.EmailField()

    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.CharField(max_length=32)

    reason = models.CharField(max_length=32)

    primary_nick = models.CharField(max_length=32)
    secondary_nick = models.CharField(max_length=32)

    shell = models.CharField(max_length=32, choices=SHELL_OPTIONS, default=BASH)

    funet_rules_accepted = models.BooleanField(blank=False)


def create_bank_reference(sender, instance, created, **kwargs):
    def checksum(raw):
        """ Get check number for given reference number """

        multiplicators = (7, 3, 1)
        string_raw = str(raw).zfill(16)
        inverse = map(int, string_raw[::-1])
        result = sum(multiplicators[i % 3] * x for i, x in enumerate(inverse))
        return (10 - (result % 10)) % 10

    def reference(pk):
        padded = str(pk).zfill(16)
        return padded[0:15] + str(checksum(pk))

    instance.bank_reference = reference(instance.id)
    print instance.bank_reference

post_save.connect(create_bank_reference, Application)
