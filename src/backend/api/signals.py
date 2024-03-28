from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MorningReport, Sportsman


@receiver(post_save, sender=MorningReport)
def set_report_sent(instance, **kwargs):
    sportsman: Sportsman = instance.sportsman
    sportsman.morning_report_sent = True
    sportsman.save()
