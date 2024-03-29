from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SportsmanViewSet, MorningReportAPIView, TrainingAPIView

router = DefaultRouter()
router.register(r"sportsmans", SportsmanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("morning_reports/", MorningReportAPIView.as_view()),
    path("trainings/", TrainingAPIView.as_view()),
]
