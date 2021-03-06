# Generated by Django 3.2.4 on 2021-07-09 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
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
                    "post_unique_mark",
                    models.SlugField(
                        max_length=250, unique_for_date="post_published_date"
                    ),
                ),
                ("post_title", models.CharField(max_length=250)),
                ("post_text", models.TextField()),
                ("post_created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "post_published_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("post_updated_date", models.DateTimeField(auto_now=True)),
                (
                    "post_status",
                    models.CharField(
                        choices=[
                            ("черновик", "Черновик"),
                            ("опубликовано", "Опубликовано"),
                        ],
                        default="черновик",
                        max_length=12,
                    ),
                ),
                (
                    "post_author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-post_published_date",),
            },
        ),
    ]
