from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SportsmanViewSet,
    MorningReportView,
    TrainingView,
    TrainingReportView,
)

router = DefaultRouter()
router.register(r"sportsmans", SportsmanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("morning_reports/", MorningReportView.as_view()),
    path("trainings/", TrainingView.as_view()),
    path("training_reports/", TrainingReportView.as_view()),
]
