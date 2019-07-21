from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeemintternet', '0006_auto_20150329_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='des_crypt',
            field=models.CharField(default='x', max_length=128),
            preserve_default=False,
        ),
    ]
