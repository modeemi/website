from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("first_name", models.CharField(max_length=32)),
                ("last_name", models.CharField(max_length=32)),
                ("email", models.EmailField(max_length=75)),
                ("reason", models.CharField(max_length=256, blank=True)),
                ("primary_nick", models.CharField(max_length=32)),
                ("secondary_nick", models.CharField(max_length=32)),
                (
                    "shell",
                    models.CharField(
                        default=b"/bin/bash",
                        max_length=32,
                        choices=[
                            (b"/bin/sh", b"/bin/sh"),
                            (b"/bin/bash", b"/bin/bash"),
                            (b"/bin/zsh", b"/bin/zsh"),
                            (b"/bin/tcsh", b"/bin/tcsh"),
                            (b"/bin/false", b"/bin/false"),
                        ],
                    ),
                ),
                ("funet_rules_accepted", models.BooleanField(default=False)),
                ("applied", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True, auto_now_add=True)),
                ("bank_reference", models.CharField(max_length=6, editable=False)),
                ("sha512", models.CharField(max_length=128)),
                ("pbkdf2_sha256", models.CharField(max_length=128)),
            ],
            options={"verbose_name": "Hakemus", "verbose_name_plural": "Hakemukset"},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("sender", models.CharField(max_length=64, blank=True)),
                ("email", models.EmailField(max_length=75, blank=True)),
                ("message", models.TextField()),
                ("sent", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name": "Palaute", "verbose_name_plural": "Palautteet"},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.TextField()),
                ("text", models.TextField(blank=True)),
                ("posted", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True, auto_now_add=True)),
                (
                    "poster",
                    models.ForeignKey(
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={"verbose_name": "Uutinen", "verbose_name_plural": "Uutiset"},
            bases=(models.Model,),
        ),
    ]
