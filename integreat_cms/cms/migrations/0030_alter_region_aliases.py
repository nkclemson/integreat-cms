# Generated by Django 3.2.13 on 2022-05-31 13:01

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Convert the aliases field of the region model to a JSON field
    """

    dependencies = [
        ("cms", "0029_region_fallback_translations_enabled"),
    ]

    operations = [
        migrations.AlterField(
            model_name="region",
            name="aliases",
            field=models.JSONField(
                default=dict,
                blank=True,
                help_text="E.g. smaller municipalities in that area. If empty, the CMS will try to fill this automatically. Specify as JSON.",
                verbose_name="aliases",
            ),
        ),
    ]
