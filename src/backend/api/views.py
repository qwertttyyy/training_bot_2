from rest_framework import generics

from .models import Sportsman, MorningReport, Training, TrainingReport
from .serializers import (
    SportsmanSerializer,
    MorningReportSerializer,
    TrainingSerializer,
    TrainingReportSerializer,
)
from .utils import CreateRetrieveListDeleteViewSet


class SportsmanViewSet(CreateRetrieveListDeleteViewSet):
    queryset = Sportsman.objects.prefetch_related("trainings")
    serializer_class = SportsmanSerializer
    lookup_field = "chat_id"


class MorningReportView(generics.CreateAPIView):
    queryset = MorningReport.objects.select_related("sportsman")
    serializer_class = MorningReportSerializer


class TrainingView(generics.CreateAPIView):
    queryset = Training.objects.select_related("sportsman")
    serializer_class = TrainingSerializer


class TrainingReportView(generics.CreateAPIView):
    queryset = TrainingReport.objects.select_related("sportsman")
    serializer_class = TrainingReportSerializer
