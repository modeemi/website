from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeemintternet', '0002_soda'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_accepted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='application_processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='application_rejected',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
