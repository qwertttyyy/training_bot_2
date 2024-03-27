from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CommandHandler,
    ConversationHandler,
)

from src.bot.commands.templates import FEELING_COMMAND
from src.bot.conversations.feeling import callback_funcs
from src.bot.conversations.feeling.states import States
from src.bot.general.callback_funcs import cancel_conversation
from src.bot.general.templates import BTN_CANCEL

feeling_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command=FEELING_COMMAND,
            callback=callback_funcs.start_feeling,
        )
    ],
    states={
        States.RATING: [
            CallbackQueryHandler(cancel_conversation, BTN_CANCEL),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_rating
            ),
        ],
        States.SLEEP_HOURS: [
            CallbackQueryHandler(cancel_conversation, BTN_CANCEL),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_sleep_hours,
            ),
        ],
        States.HEART_RATE: [
            CallbackQueryHandler(cancel_conversation, BTN_CANCEL),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_heart_rate_save_feeling,
            ),
        ],
    },
    fallbacks=[],
)
