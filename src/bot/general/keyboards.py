from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.general.templates import BTN_LABEL_CANCEL, BTN_CANCEL

CANCEL_BUTTON = InlineKeyboardButton(
    text=BTN_LABEL_CANCEL, callback_data=BTN_CANCEL
)
CANCEL_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(CANCEL_BUTTON,)
)
