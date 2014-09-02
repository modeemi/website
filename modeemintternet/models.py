from django.db import models

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

    email = models.EmailField()

    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.CharField(max_length=32)

    reason = models.CharField(max_length=32)

    primary_nick = models.CharField(max_length=32)
    secondary_nick = models.CharField(max_length=32)

    shell = models.CharField(max_length=32, choices=SHELL_OPTIONS, default=BASH)

    funet_rules_accepted = models.BooleanField(blank=False)
