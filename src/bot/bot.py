from telegram.ext import Application, ApplicationBuilder

from src.bot.conversations.morning_report.handlers import (
    morning_report_handler,
)
from src.bot.conversations.registration.handlers import registration_handler
from utils.configs import API_TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(API_TOKEN).build()
    application.add_handler(handler=registration_handler)
    application.add_handler(handler=morning_report_handler)
    return application
