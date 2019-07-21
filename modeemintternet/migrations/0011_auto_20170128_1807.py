from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeemintternet', '0010_auto_20160229_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='shell',
            field=models.CharField(choices=[('/bin/sh', '/bin/sh'), ('/bin/bash', '/bin/bash'), ('/bin/zsh', '/bin/zsh'), ('/bin/tcsh', '/bin/tcsh'), ('/bin/false', '/bin/false')], default='/bin/bash', max_length=32),
        ),
    ]
