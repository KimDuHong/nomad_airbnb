# Generated by Django 4.1.5 on 2023-01-09 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="amenity",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="amenity",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="room",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="room",
            old_name="updated",
            new_name="updated_at",
        ),
    ]
