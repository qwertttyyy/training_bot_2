from django.contrib import admin

from .models import Sportsman


@admin.register(Sportsman)
class SportsmanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "chat_id",
        "created_date",
        "sheet_id",
        "archive_sheet_id",
        "strava_keys",
        "is_send_morning",
        "is_send_evening",
    )
