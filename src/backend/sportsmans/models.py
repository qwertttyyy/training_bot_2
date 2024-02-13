from django.db import models


class Sportsman(models.Model):
    chat_id = models.PositiveBigIntegerField(verbose_name="Телеграм ID")
    name = models.CharField(max_length=32, verbose_name="Имя")
    surname = models.CharField(max_length=32, verbose_name="Фамилия")
    sheet_id = models.PositiveBigIntegerField(verbose_name="ID листа")
    archive_sheet_id = models.PositiveBigIntegerField(
        verbose_name="ID архивного листа"
    )
    is_send_morning = models.BooleanField(
        default=False, verbose_name="Отправлено ли утренне уведомление"
    )
    is_send_evening = models.BooleanField(
        default=False, verbose_name="Отправлено ли вечернее уведомление"
    )
    strava_keys = models.TextField(
        null=True, blank=True, verbose_name="Ключи API Strava"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"
        ordering = ("created_date",)

    def __str__(self):
        return "{name} {surname} {chat_id}".format(
            name=self.name, surname=self.surname, chat_id=self.chat_id
        )
