from rest_framework import serializers

from .models import Sportsman


class SportsmanPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sportsman
        fields = (
            "morning_reminder_sent",
            "evening_reminder_sent",
        )


class SportsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sportsman
        fields = (
            "name",
            "surname",
            "chat_id",
            "sheet_id",
            "archive_sheet_id",
            "morning_reminder_sent",
            "evening_reminder_sent",
        )
        extra_kwargs = {
            "name": {"required": True},
            "surname": {"required": True},
            "chat_id": {"required": True},
            "sheet_id": {"required": True},
            "archive_sheet_id": {"required": True},
        }
