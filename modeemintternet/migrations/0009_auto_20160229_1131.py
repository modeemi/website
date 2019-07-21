from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeemintternet', '0008_auto_20150403_0333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='soda',
            options={'verbose_name': 'Lim', 'verbose_name_plural': 'Limut'},
        ),
    ]
