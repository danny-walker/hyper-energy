# Generated by Django 3.2.5 on 2021-09-05 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("calculators", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SMManufacturer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company",
                    models.CharField(max_length=250, verbose_name="производитель"),
                ),
                ("country", models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name="windturbine",
            name="model_name",
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="SolarModule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_name", models.CharField(max_length=250)),
                ("nominal_power", models.FloatField(max_length=250)),
                ("sm_size", models.FloatField(max_length=250)),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calculators.smmanufacturer",
                    ),
                ),
            ],
        ),
    ]
