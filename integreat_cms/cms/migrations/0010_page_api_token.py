# Generated by Django 3.2.12 on 2022-03-05 16:41

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration file that adds the api access token field to pages.
    """

    dependencies = [
        ("cms", "0009_alter_translation_model_ordering"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="api_token",
            field=models.CharField(
                blank=True,
                help_text="API token to allow writing content to translations.",
                max_length=36,
                verbose_name="API access token",
            ),
        ),
    ]
