# handlers/broadcast.py

from config import logger
from services.user_service import load_users
from telegram import Update
from telegram.ext import ContextTypes

USERS = load_users()


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data.get("ADMIN"):
        return await update.message.reply_text("❌ أنت لست الإدمن.")

    context.user_data["state"] = "BROADCAST"
    await update.message.reply_text("📢 أرسل نص / صورة / صوت للبث:")


async def handle_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data.get("ADMIN"):
        return

    if context.user_data.get("state") != "BROADCAST":
        return

    text = update.message.text
    failed = 0
    for uid in USERS:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast text failed for {uid}: {e}")

    context.user_data["state"] = None
    await update.message.reply_text(f"✅ تم إرسال النص للبث.\nفشل الإرسال: {failed}")


async def handle_broadcast_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data.get("ADMIN"):
        return

    if context.user_data.get("state") != "BROADCAST":
        return

    photo = update.message.photo[-1] if update.message.photo else None
    if not photo:
        return await update.message.reply_text("❌ أرسل صورة صالحة.")

    caption = update.message.caption or ""
    failed = 0
    for uid in USERS:
        try:
            await context.bot.send_photo(chat_id=uid, photo=photo.file_id, caption=caption)
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast photo failed for {uid}: {e}")

    context.user_data["state"] = None
    await update.message.reply_text(f"✅ تم إرسال الصورة للبث.\nفشل الإرسال: {failed}")


async def handle_broadcast_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data.get("ADMIN"):
        return

    if context.user_data.get("state") != "BROADCAST":
        return

    audio = update.message.audio or update.message.voice
    if not audio:
        return await update.message.reply_text("❌ أرسل صوت أو ملف صوتي صالح.")

    failed = 0
    for uid in USERS:
        try:
            await context.bot.send_audio(chat_id=uid, audio=audio.file_id)
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast audio failed for {uid}: {e}")

    context.user_data["state"] = None
    await update.message.reply_text(f"✅ تم إرسال الصوت للبث.\nفشل الإرسال: {failed}")
