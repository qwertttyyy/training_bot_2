from rest_framework import generics

from .models import Sportsman, MorningReport, Training
from .serializers import (
    SportsmanSerializer,
    MorningReportSerializer,
    TrainingSerializer,
)
from .utils import CreateRetrieveListDeleteViewSet


class SportsmanViewSet(CreateRetrieveListDeleteViewSet):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmanSerializer
    lookup_field = "chat_id"


class MorningReportAPIView(generics.CreateAPIView):
    queryset = MorningReport.objects.select_related("sportsman")
    serializer_class = MorningReportSerializer


class TrainingAPIView(generics.CreateAPIView):
    queryset = Training.objects.select_related("sportsman")
    serializer_class = TrainingSerializer
