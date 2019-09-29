from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("modeemintternet", "0004_auto_20150315_0131")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="lat",
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="event",
            name="lon",
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
