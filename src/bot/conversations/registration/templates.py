NAME_PATTERN = r"^[А-Яа-яA-Za-z'-]{3,30}$"

NAME_FIELD = "name"
SURNAME_FIELD = "surname"
EXISTING_SHEET_IDS_FIELD = "existing_sheet_ids"

REPLY_MSG_ASK_NAME = (
    "Привет! Тебе нужно зарегистрироваться." "\nВведи своё имя:"
)
REPLY_MSG_ASK_SURNAME = "Введи свою фамилию:"
REPLY_MSG_SUCCESS_REGISTRATION = "Ты зарегистрирован!"
REPLY_MSG_IF_TRAINER = "Ты тренер, тебе не нужно регистрироваться!"
REPLY_MSG_ALREADY_REGISTERED = "Ты уже зарегистрирован!"

NAME_VALIDATION_ERR_MSG = (
    "Некорректный ввод. Может содержать только буквы! Введите ещё раз:"
)
NEW_SPORTSMAN_REGISTERED = (
    "Зарегистрировался новый спортсмен: {name} {surname}"
)
