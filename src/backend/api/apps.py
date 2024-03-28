from django.apps import AppConfig
from django.db.models.signals import post_save


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self, *args, **kwargs):
        from . import signals

        morning_report_model = self.get_model("MorningReport")
        post_save.connect(signals.set_report_sent, sender=morning_report_model)
