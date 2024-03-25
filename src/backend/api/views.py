from rest_framework import exceptions, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Sportsman, Feeling
from .serializers import SportsmanSerializer, FeelingSerializer
from .utils import CreateRetrieveListDeleteViewSet


class SportsmanViewSet(CreateRetrieveListDeleteViewSet):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmanSerializer
    lookup_field = "chat_id"

    @action(detail=True, methods=["patch"], url_path="set-reminder-sent")
    def set_reminder_sent(self, request, chat_id=None):
        obj = get_object_or_404(self.queryset, chat_id=chat_id)
        if "morning_reminder_sent" in request.data:
            obj.morning_reminder_sent = request.data["morning_reminder_sent"]
        elif "evening_reminder_sent" in request.data:
            obj.evening_reminder_sent = request.data["evening_reminder_sent"]
        else:
            raise exceptions.ValidationError(
                "Отсутствует поле morning_reminder_sent или evening_reminder_sent"
            )
        obj.save()
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class FeelingAPIView(generics.CreateAPIView):
    queryset = Feeling.objects.select_related("sportsman")
    serializer_class = FeelingSerializer
