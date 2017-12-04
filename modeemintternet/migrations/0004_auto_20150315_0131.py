# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modeemintternet', '0003_auto_20141014_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('location', models.TextField(blank=True)),
                ('lat', models.FloatField(default=61.44999)),
                ('lon', models.FloatField(default=23.8568)),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField(blank=True)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('poster', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Tapahtuma',
                'verbose_name_plural': 'Tapahtumat',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='application',
            name='reason',
        ),
    ]
