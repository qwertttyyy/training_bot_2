from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Sportsman, Feeling


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


class FeelingSerializer(serializers.ModelSerializer):
    chat_id = serializers.SlugRelatedField(
        slug_field="chat_id",
        queryset=Sportsman.objects.all(),
        source="sportsman",
    )
    rating = serializers.ChoiceField(Feeling.RATING_CHOICES)

    class Meta:
        model = Feeling
        fields = (
            "rating",
            "sleep_hours",
            "heart_rate",
            "chat_id",
        )
