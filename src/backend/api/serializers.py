from rest_framework import serializers

from .models import Sportsman, MorningReport


class SportsmanPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sportsman
        fields = (
            "morning_report_sent",
            "training_report_sent",
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
            "morning_report_sent",
            "training_report_sent",
        )
        extra_kwargs = {
            "name": {"required": True},
            "surname": {"required": True},
            "chat_id": {"required": True},
            "sheet_id": {"required": True},
            "archive_sheet_id": {"required": True},
        }


class MorningReportSerializer(serializers.ModelSerializer):
    chat_id = serializers.SlugRelatedField(
        slug_field="chat_id",
        queryset=Sportsman.objects.all(),
        source="sportsman",
    )
    health_score = serializers.ChoiceField(MorningReport.HEALTH_SCORE_CHOICES)

    class Meta:
        model = MorningReport
        fields = (
            "chat_id",
            "health_score",
            "sleep_hours",
            "heart_rate",
        )
