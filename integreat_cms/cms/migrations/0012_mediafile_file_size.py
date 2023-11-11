# Generated by Django 3.2.12 on 2022-03-17 20:03
from __future__ import annotations

from datetime import datetime
from os.path import getmtime
from typing import TYPE_CHECKING

from django.db import migrations, models
from django.utils.timezone import make_aware

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor


# pylint: disable=unused-argument
def calculate_file_fields(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """
    Calculates the file size for already existing MediaFiles on the system.
    :param apps: The configuration of installed applications
    :param schema_editor: The database abstraction layer that creates actual SQL code
    """

    MediaFiles = apps.get_model("cms", "MediaFile")
    for media in MediaFiles.objects.all():
        media.file_size = media.file.size
        media.last_modified = make_aware(
            datetime.fromtimestamp(getmtime(media.file.path))
        )
        media.save()


class Migration(migrations.Migration):
    """
    Migration file to add the file size to the media model and add a last modified field for the physical data.
    """

    dependencies = [
        ("cms", "0011_default_pushnotification_channel"),
    ]

    operations = [
        migrations.AddField(
            model_name="mediafile",
            name="last_modified",
            field=models.DateTimeField(null=True, verbose_name="last modified"),
        ),
        migrations.AddField(
            model_name="mediafile",
            name="file_size",
            field=models.IntegerField(default=0, verbose_name="file size"),
            preserve_default=False,
        ),
        migrations.RunPython(calculate_file_fields, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="mediafile",
            name="file_size",
            field=models.IntegerField(verbose_name="file size"),
        ),
        migrations.AlterField(
            model_name="mediafile",
            name="last_modified",
            field=models.DateTimeField(
                help_text="The date and time when the physical media file was last modified",
                verbose_name="last modified",
            ),
        ),
    ]
