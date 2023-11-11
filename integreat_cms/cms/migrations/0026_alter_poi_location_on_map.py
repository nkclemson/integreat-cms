# Generated by Django 3.2.13 on 2022-05-23 12:13

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration file to not show POIs on map by default.
    """

    dependencies = [
        ("cms", "0025_update_roles"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poi",
            name="location_on_map",
            field=models.BooleanField(
                default=False,
                help_text="Tick if you want to show this location on map",
                verbose_name="Show this location on map",
            ),
        ),
    ]
