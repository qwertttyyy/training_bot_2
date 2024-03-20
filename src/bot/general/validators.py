# from re import fullmatch
#
# from telegram import Update
#
#
# async def validate_input_value(
#     update: Update,
#     value: str,
#     pattern: str,
#     message_text: str,
#     state: int = None,
# ):
#     if not fullmatch(pattern, value):
#         await update.message.reply_text(message_text)
#         return state
