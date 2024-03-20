from telegram.ext import Application, ApplicationBuilder

from src.bot.conversations.registration.handlers import registration_handler
from utils.configs import API_TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(API_TOKEN).build()
    application.add_handler(handler=registration_handler)
    return application
