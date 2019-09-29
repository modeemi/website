from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("modeemintternet", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Soda",
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
                ("name", models.CharField(max_length=128)),
                ("price", models.DecimalField(max_digits=3, decimal_places=2)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "Limu", "verbose_name_plural": "Limut"},
            bases=(models.Model,),
        )
    ]
