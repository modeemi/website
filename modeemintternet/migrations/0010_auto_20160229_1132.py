from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeemintternet', '0009_auto_20160229_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='soda',
            options={'verbose_name': 'Limu', 'verbose_name_plural': 'Limut'},
        ),
    ]
