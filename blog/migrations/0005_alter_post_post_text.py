# Generated by Django 3.2.5 on 2021-08-10 12:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_post_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="post_text",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
