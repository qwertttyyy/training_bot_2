from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from src.bot.conversations.feeling import templates
from src.bot.conversations.feeling.states import States
from src.bot.general import templates as base_templates
from src.bot.general.keyboards import CANCEL_KEYBOARD
from src.bot.general.validators import validate_input_value
from src.bot.services.api import api_service
from src.bot.services.api.entities import Feeling, Sportsman
from src.bot.services.google.sheets_service import GoogleSheetsService
from src.bot.utils.configs import TRAINER_ID, DATE_FORMAT
from src.bot.utils.utils import (
    convert_to_number,
    get_user_data_value,
    get_formatted_today_date,
)


async def start_feeling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id == TRAINER_ID:
        await update.message.reply_text(text=templates.REPLY_MSG_IF_TRAINER)
        return ConversationHandler.END

    sportsman = await api_service.get_sportsman(chat_id)

    if not sportsman:
        await update.message.reply_text(
            text=base_templates.REPLY_MSG_IF_NOT_REGISTERED
        )
        return ConversationHandler.END

    context.user_data[templates.SPORTSMAN_FIELD] = sportsman

    await update.message.reply_text(
        text=templates.REPLY_MSG_ASK_RATING, reply_markup=CANCEL_KEYBOARD
    )
    return States.RATING


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rating = update.message.text.strip()

    if not await validate_input_value(
        update,
        rating,
        templates.RATING_PATTERN,
        templates.RATING_VALIDATION_ERR_MSG,
    ):
        return States.RATING

    context.user_data[templates.FEELING_FIELD] = Feeling()
    context.user_data[templates.FEELING_FIELD].rating = int(rating)
    await update.message.reply_text(
        text=templates.REPLY_MSG_ASK_SLEEP_HOURS, reply_markup=CANCEL_KEYBOARD
    )
    return States.SLEEP_HOURS


async def handle_sleep_hours(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    sleep_hours = update.message.text.strip()
    if not await validate_input_value(
        update,
        sleep_hours,
        templates.SLEEP_HOURS_PATTERN,
        templates.SLEEP_HOURS_VALIDATION_ERR_MSG,
    ):
        return States.SLEEP_HOURS

    context.user_data[templates.FEELING_FIELD].sleep_hours = convert_to_number(
        sleep_hours
    )
    await update.message.reply_text(
        text=templates.REPLY_MSG_ASK_HEART_RATE, reply_markup=CANCEL_KEYBOARD
    )
    return States.HEART_RATE


async def handle_heart_rate_save_feeling(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    heart_rate = update.message.text.strip()

    if not await validate_input_value(
        update,
        heart_rate,
        templates.HEART_RATE_PATTERN,
        templates.HEART_RATE_VALIDATION_ERR_MSG,
    ):
        return States.HEART_RATE

    feeling: Feeling = get_user_data_value(context, templates.FEELING_FIELD)
    sportsman: Sportsman = get_user_data_value(
        context, templates.SPORTSMAN_FIELD
    )
    heart_rate = convert_to_number(heart_rate)

    async with GoogleSheetsService() as sheet_service:
        await sheet_service.send_data_to_sheet(
            sportsman.full_name,
            "B",
            [
                feeling.rating,
                feeling.sleep_hours,
                heart_rate,
            ],
        )

    chat_id = update.effective_chat.id

    await api_service.save_feeling(
        chat_id, feeling.rating, feeling.sleep_hours, heart_rate
    )

    report_massage = templates.MORNING_REPORT_MSG.format(
        full_name=sportsman.full_name,
        date=get_formatted_today_date(DATE_FORMAT),
        rating=feeling.rating,
        sleep_hours=feeling.sleep_hours,
        heart_rate=heart_rate,
    )

    await context.bot.send_message(
        TRAINER_ID, report_massage, parse_mode=ParseMode.HTML
    )
    await update.message.reply_text(base_templates.REPLY_MSG_REPORT_SENT)
    await update.message.reply_text(report_massage, parse_mode=ParseMode.HTML)

    return ConversationHandler.END
