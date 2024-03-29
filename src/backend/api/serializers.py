from rest_framework import serializers

from .models import Sportsman, MorningReport, Training, TrainingReport


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


class TrainingSerializer(serializers.ModelSerializer):
    chat_id = serializers.SlugRelatedField(
        slug_field="chat_id",
        queryset=Sportsman.objects.all(),
        source="sportsman",
    )
    report = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Training
        fields = (
            "chat_id",
            "distance",
            "avg_temp",
            "avg_heart_rate",
            "date",
            "report",
        )

    def create(self, validated_data):
        report = validated_data.pop("report", None)
        training = Training.objects.create(**validated_data)
        if report is not None:
            TrainingReport.objects.create(
                sportsman=training.sportsman, report=report
            )
        return training


class TrainingReportSerializer(serializers.ModelSerializer):
    chat_id = serializers.SlugRelatedField(
        slug_field="chat_id",
        queryset=Sportsman.objects.all(),
        source="sportsman",
    )

    class Meta:
        model = TrainingReport
        fields = ("chat_id", "report")
