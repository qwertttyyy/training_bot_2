from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MorningReport, Sportsman, TrainingReport


@receiver(post_save, sender=TrainingReport)
@receiver(post_save, sender=MorningReport)
def set_report_sent(sender, instance, **kwargs):
    sportsman: Sportsman = instance.sportsman
    if isinstance(sender, MorningReport):
        sportsman.morning_report_sent = True
    else:
        sportsman.training_report_sent = True
    sportsman.save()
