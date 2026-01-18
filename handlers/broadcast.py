from config import WAITING_TEXT, WAITING_PHOTO, WAITING_AUDIO
from services.user_service import load_users
from utils.logger import get_logger

logger = get_logger(__name__)


async def broadcast_command(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        logger.warning("Unauthorized broadcast attempt")
        return

    context.user_data[WAITING_TEXT] = True
    context.user_data[WAITING_PHOTO] = True
    context.user_data[WAITING_AUDIO] = True

    await update.message.reply_text("📢 أرسل الآن نصًا أو صورة أو صوتًا ليتم بثه للجميع")


async def handle_photo(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return
    if not context.user_data.get(WAITING_PHOTO):
        return

    users = load_users()
    photo = update.message.photo[-1]
    caption = update.message.caption or ""

    for uid in users:
        try:
            await context.bot.send_photo(chat_id=uid, photo=photo.file_id, caption=caption)
        except Exception as e:
            logger.error(f"Photo broadcast failed to {uid}: {e}")

    context.user_data[WAITING_PHOTO] = False
    await update.message.reply_text("✅ تم إرسال الصورة للجميع")


async def handle_audio(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return
    if not context.user_data.get(WAITING_AUDIO):
        return

    users = load_users()
    audio = update.message.audio or update.message.voice
    if not audio:
        return

    for uid in users:
        try:
            await context.bot.send_audio(chat_id=uid, audio=audio.file_id)
        except Exception as e:
            logger.error(f"Audio broadcast failed to {uid}: {e}")

    context.user_data[WAITING_AUDIO] = False
    await update.message.reply_text("✅ تم إرسال الصوت للجميع")


async def handle_text_broadcast(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    if not context.user_data.get(WAITING_TEXT):
        return

    users = load_users()
    text = update.message.text

    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
        except Exception as e:
            logger.error(f"Text broadcast failed to {uid}: {e}")

    context.user_data[WAITING_TEXT] = False
    await update.message.reply_text("✅ تم إرسال النص للجميع")
