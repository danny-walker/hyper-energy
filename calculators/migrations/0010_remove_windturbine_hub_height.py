# Generated by Django 3.2.5 on 2021-09-22 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("calculators", "0009_auto_20210921_2119"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="windturbine",
            name="hub_height",
        ),
    ]