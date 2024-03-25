from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SportsmanViewSet, FeelingAPIView

router = DefaultRouter()
router.register(r"sportsmans", SportsmanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("feelings/", FeelingAPIView.as_view()),
]
