from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("modeemintternet", "0005_auto_20150329_1547")]

    operations = [
        migrations.RenameField(
            model_name="application", old_name="sha512", new_name="sha512_crypt"
        )
    ]
