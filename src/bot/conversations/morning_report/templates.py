HEALTH_SCORE_PATTERN = r"^(10|[1-9])$"
SLEEP_HOURS_PATTERN = r"^\d{1,2}([.,]\d{1,2})?$"
HEART_RATE_PATTERN = r"^\d{2,3}$"

SPORTSMAN_FIELD = "sportsman"
MORNING_REPORT_FIELD = "morning_report"

REPLY_MSG_IF_TRAINER = "Ты тренер, тебе не нужно отправлять отчёты)"
REPLY_MSG_ASK_HEALTH_SCORE = "Оцени своё самочувствие от 1 до 10:"
REPLY_MSG_ASK_SLEEP_HOURS = "Сколько часов ты спал?"
REPLY_MSG_ASK_HEART_RATE = "Какой у тебя пульс?"

HEALTH_SCORE_VALIDATION_ERR_MSG = (
    "Число должно быть от 1 до 10. Введите ещё раз:"
)
SLEEP_HOURS_VALIDATION_ERR_MSG = (
    "Должно быть целое или десятичное число. Введите ещё раз:"
)
HEART_RATE_VALIDATION_ERR_MSG = (
    "Пульс должен быть целым числом. Введите ещё раз:"
)

MORNING_REPORT_MSG = (
    "Утренний отчёт студента {full_name}:\n"
    "<b>Дата:</b> {date}\n"
    "<b>Оценка самочувствия:</b> {health_score}\n"
    "<b>Количество часов сна:</b> {sleep_hours}\n"
    "<b>Пульс:</b> {heart_rate}"
)
