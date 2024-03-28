from django.contrib import admin

from .models import Sportsman, MorningReport, Training


@admin.register(Sportsman)
class SportsmanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "surname",
        "chat_id",
        "created_date",
        "sheet_id",
        "archive_sheet_id",
        "strava_keys",
        "morning_report_sent",
        "training_report_sent",
    )


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "strava_id",
        "distance",
        "avg_temp",
        "avg_heart_rate",
        "date",
        "sportsman",
    )


@admin.register(MorningReport)
class MorningReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "health_score",
        "sleep_hours",
        "heart_rate",
        "created_date",
        "sportsman",
    )
