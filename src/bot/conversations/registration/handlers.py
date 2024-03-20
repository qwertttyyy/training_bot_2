from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from src.bot.commands.templates import REGISTRATION_COMMAND
from src.bot.conversations.registration import callback_funcs
from src.bot.conversations.registration.states import States
from src.bot.general.callback_funcs import cancel_conversation
from src.bot.general.templates import BTN_CANCEL

registration_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command=REGISTRATION_COMMAND,
            callback=callback_funcs.start_registration,
        )
    ],
    states={
        States.NAME: [
            CallbackQueryHandler(cancel_conversation, BTN_CANCEL),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handel_name
            ),
        ],
        States.SURNAME: [
            CallbackQueryHandler(cancel_conversation, BTN_CANCEL),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handel_surname_create_spreadsheet,
            ),
        ],
    },
    fallbacks=[],
)
