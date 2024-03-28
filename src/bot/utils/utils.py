from datetime import datetime

from telegram.ext import ContextTypes


def get_user_data_value(context: ContextTypes.DEFAULT_TYPE, user_data_key):
    return context.user_data.get(user_data_key)


def convert_to_number(string_number: str) -> int | float:
    try:
        return int(string_number)
    except ValueError:
        return float(string_number)


def get_formatted_date(format: str, date=None) -> str:
    if not date:
        date = datetime.today()
    return f"{date:{format}}".lower()
