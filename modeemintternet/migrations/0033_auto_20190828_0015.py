# Generated by Django 2.2.4 on 2019-08-27 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("modeemintternet", "0032_auto_20190828_0014")]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE passwd ADD CONSTRAINT passwd_gid_fkey FOREIGN KEY (gid) REFERENCES usergroup(gid);"
        )
    ]
