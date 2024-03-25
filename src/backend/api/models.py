from django.db import models


class Sportsman(models.Model):
    chat_id = models.PositiveBigIntegerField(
        verbose_name="Телеграм ID", unique=True
    )
    name = models.CharField(max_length=32, verbose_name="Имя")
    surname = models.CharField(max_length=32, verbose_name="Фамилия")
    sheet_id = models.PositiveBigIntegerField(verbose_name="ID листа")
    archive_sheet_id = models.PositiveBigIntegerField(
        verbose_name="ID архивного листа"
    )
    morning_reminder_sent = models.BooleanField(
        default=False, verbose_name="Отправлено ли утренне уведомление"
    )
    evening_reminder_sent = models.BooleanField(
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
        ordering = ("-created_date",)

    def __str__(self):
        return "{name} {surname} {chat_id}".format(
            name=self.name, surname=self.surname, chat_id=self.chat_id
        )


class Feeling(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )

    rating = models.SmallIntegerField(
        choices=RATING_CHOICES, verbose_name="Оценка самочувствия"
    )
    sleep_hours = models.FloatField(verbose_name="Кол-во часов сна")
    heart_rate = models.PositiveSmallIntegerField(verbose_name="Пульс")
    created_date = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    sportsman = models.ForeignKey(
        Sportsman, on_delete=models.CASCADE, related_name="feelings"
    )

    class Meta:
        verbose_name = "Самочувствие"
        verbose_name_plural = "Самочувствие"
        ordering = ("-created_date",)

    def __str__(self):
        return "{name} {surname} {chat_id}".format(
            name=self.sportsman.name,
            surname=self.sportsman.surname,
            chat_id=self.sportsman.chat_id,
        )
