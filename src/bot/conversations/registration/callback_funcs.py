from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.bot.conversations.registration import templates
from src.bot.conversations.registration.states import States
from src.bot.general import templates as base_templates
from src.bot.general.keyboards import CANCEL_KEYBOARD
from src.bot.general.validators import validate_input_value
from src.bot.services.api import api_service
from src.bot.services.google.sheets_service import GoogleSheetsService
from src.bot.utils.configs import TRAINER_ID


async def start_registration(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id

    if chat_id == TRAINER_ID:
        await update.message.reply_text(text=templates.REPLY_MSG_IF_TRAINER)
        return ConversationHandler.END

    sportsmans = await api_service.get_sportsmans_list()
    context.user_data[templates.EXISTING_SHEET_IDS_FIELD] = []

    for sportsman in sportsmans:
        if sportsman.chat_id == chat_id:
            await update.message.reply_text(
                text=templates.REPLY_MSG_ALREADY_REGISTERED
            )
            return ConversationHandler.END
        context.user_data[templates.EXISTING_SHEET_IDS_FIELD].append(
            (sportsman.sheet_id, sportsman.archive_sheet_id)
        )

    await update.message.reply_text(
        text=templates.REPLY_MSG_ASK_NAME, reply_markup=CANCEL_KEYBOARD
    )
    return States.NAME


async def handel_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()

    if not await validate_input_value(
        update, name, templates.NAME_PATTERN, templates.NAME_VALIDATION_ERR_MSG
    ):
        return States.NAME

    context.user_data[templates.NAME_FIELD] = name
    await update.message.reply_text(
        text=templates.REPLY_MSG_ASK_SURNAME, reply_markup=CANCEL_KEYBOARD
    )
    return States.SURNAME


async def handel_surname_save_sportsman(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    surname = update.message.text.strip()

    if not await validate_input_value(
        update,
        surname,
        templates.NAME_PATTERN,
        templates.NAME_VALIDATION_ERR_MSG,
    ):
        return States.SURNAME

    existing_sheet_ids = context.user_data[templates.EXISTING_SHEET_IDS_FIELD]
    if existing_sheet_ids:
        sheet_id = sorted(existing_sheet_ids)[-1][-1] + 1
        archive_sheet_id = sheet_id + 1
    else:
        sheet_id, archive_sheet_id = context.user_data[
            templates.EXISTING_SHEET_IDS_FIELD
        ]

    chat_id = update.effective_chat.id
    name = context.user_data[templates.NAME_FIELD]

    async with GoogleSheetsService() as sheet_service:
        await sheet_service.create_sportsman_sheets(
            f"{name} {surname}", sheet_id, archive_sheet_id
        )
    await api_service.save_sportsman(
        chat_id, name, surname, sheet_id, archive_sheet_id
    )
    await update.message.reply_text(templates.REPLY_MSG_SUCCESS_REGISTRATION)
    await context.bot.send_message(
        TRAINER_ID,
        templates.NEW_SPORTSMAN_REGISTERED.format(name=name, surname=surname),
    )
    return ConversationHandler.END
