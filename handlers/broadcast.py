from config import WAITING_TEXT, WAITING_PHOTO, WAITING_AUDIO, logger
from services.user_service import load_users

USERS = load_users()

async def broadcast_command(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        logger.warning("Unauthorized broadcast attempt")
        return

    context.user_data[WAITING_TEXT] = True
    context.user_data[WAITING_PHOTO] = True
    context.user_data[WAITING_AUDIO] = True

    await update.message.reply_text("📢 أرسل نص / صورة / صوت الآن")

async def handle_photo(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return
    if not context.user_data.get(WAITING_PHOTO):
        return

    photo = update.message.photo[-1]
    caption = update.message.caption or ""

    for uid in USERS:
        try:
            await context.bot.send_photo(uid, photo.file_id, caption=caption)
        except Exception as e:
            logger.error(f"Photo broadcast failed: {e}")

    context.user_data[WAITING_PHOTO] = False
    await update.message.reply_text("✅ Photo Broadcast Sent")

async def handle_audio(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return
    if not context.user_data.get(WAITING_AUDIO):
        return

    audio = update.message.audio or update.message.voice
    if not audio:
        return

    for uid in USERS:
        try:
            await context.bot.send_audio(uid, audio.file_id)
        except Exception as e:
            logger.error(f"Audio broadcast failed: {e}")

    context.user_data[WAITING_AUDIO] = False
    await update.message.reply_text("✅ Audio Broadcast Sent")
    async def handle_text_broadcast(update, context):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return
    
    # نتأكد إننا فعلًا ننتظر رسالة نصية
    if not context.user_data.get(WAITING_TEXT):
        return

    text = update.message.text

    for uid in USERS:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
        except Exception as e:
            logger.error(f"Text broadcast failed: {e}")

    # إيقاف وضع الانتظار بعد الإرسال
    context.user_data[WAITING_TEXT] = False
    await update.message.reply_text("✅ Text Broadcast Sent")


