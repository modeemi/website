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

    bank_reference = models.CharField(max_length=6, editable=False)

    email = models.EmailField()

    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.CharField(max_length=32)

    reason = models.CharField(max_length=32)

    primary_nick = models.CharField(max_length=32)
    secondary_nick = models.CharField(max_length=32)

    shell = models.CharField(max_length=32, choices=SHELL_OPTIONS, default=BASH)

    funet_rules_accepted = models.BooleanField(blank=False)


    def update_bank_reference(self):
        """
        Update the user's bank payment reference number.
        This method has to be called AFTER the object has been saved.
        """

        padded = str(self.id).zfill(6)
        multiplicators = (7, 3, 1)
        inverse = map(int, padded[::-1])
        result = sum(multiplicators[i % 3] * x for i, x in enumerate(inverse))
        checksum = str((10 - (result % 10)) % 10)

        self.bank_reference = padded[0:-1] + checksum
        self.save()

        return self.bank_reference
