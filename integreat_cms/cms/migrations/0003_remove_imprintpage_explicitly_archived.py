# Generated by Django 3.2.12 on 2022-02-09 14:48

from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration file to remove the explicitly_archived field.
    """

    dependencies = [
        ("cms", "0002_roles"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="imprintpage",
            name="explicitly_archived",
        ),
    ]
