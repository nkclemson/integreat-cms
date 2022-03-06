# Generated by Django 3.2.12 on 2022-03-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration file to change the FCM channel name
    """

    dependencies = [
        ("cms", "0007_change_role_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pushnotification",
            name="channel",
            field=models.CharField(
                choices=[("news", "News")], max_length=60, verbose_name="channel"
            ),
        ),
    ]