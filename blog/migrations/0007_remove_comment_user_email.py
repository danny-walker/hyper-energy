# Generated by Django 3.2.5 on 2021-08-16 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_auto_20210815_1832"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="user_email",
        ),
    ]
