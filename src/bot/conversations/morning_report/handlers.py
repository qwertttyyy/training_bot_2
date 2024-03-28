from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CommandHandler,
    ConversationHandler,
)

from src.bot.commands.templates import MORNING_REPORT_COMMAND
from src.bot.conversations.morning_report import callback_funcs
from src.bot.conversations.morning_report.states import States
from src.bot.general.callback_funcs import cancel_conversation
from src.bot.general.templates import BTN_CANCEL

morning_report_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command=MORNING_REPORT_COMMAND,
            callback=callback_funcs.start_morning_report,
        )
    ],
    states={
        States.HEALTH_SCORE: [
            CallbackQueryHandler(cancel_conversation, BTN_CANCEL),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_health_score,
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
                callback_funcs.handle_heart_rate_save_morning_report,
            ),
        ],
    },
    fallbacks=[],
)
