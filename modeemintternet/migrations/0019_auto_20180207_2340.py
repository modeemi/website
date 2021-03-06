# Generated by Django 2.0.2 on 2018-02-07 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("modeemintternet", "0018_remove_application_bank_reference")]

    operations = [
        migrations.AddField(
            model_name="news",
            name="ends",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="news", name="lat", field=models.FloatField(default=0.0)
        ),
        migrations.AddField(
            model_name="news", name="location", field=models.TextField(blank=True)
        ),
        migrations.AddField(
            model_name="news", name="lon", field=models.FloatField(default=0.0)
        ),
        migrations.AddField(
            model_name="news",
            name="starts",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
