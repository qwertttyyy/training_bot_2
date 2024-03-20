from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def cancel_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await update.effective_chat.send_message("Отменено, диалог завершён!")
    context.user_data.clear()
    return ConversationHandler.END
