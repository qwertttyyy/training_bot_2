# Generated by Django 5.0.1 on 2024-02-14 17:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sportsman",
            old_name="is_send_evening",
            new_name="evening_reminder_sent",
        ),
        migrations.RenameField(
            model_name="sportsman",
            old_name="is_send_morning",
            new_name="morning_reminder_sent",
        ),
    ]