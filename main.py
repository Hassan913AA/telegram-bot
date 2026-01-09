from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.constants import ChatAction

import json
import os

# ===== إعدادات =====
ADMIN_ID = 8094390739
USERS = {ADMIN_ID}

# ===== متغيرات البث لكل نوع =====
WAITING_TEXT = "waiting_text"
WAITING_PHOTO = "waiting_photo"
WAITING_AUDIO = "waiting_audio"

# ===== نظام حفظ المستخدمين =====
def load_users():
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_users():
    try:
        with open("users.json", "w") as f:
            json.dump(list(USERS), f)
    except:
        pass


# تحميل المستخدمين عند تشغيل البوت
USERS = load_users() or USERS


# ===== القوائم =====
MAIN_MENU = ReplyKeyboardMarkup(
    [
       
        [KeyboardButton("🎓 بكالوريا علمي"), KeyboardButton("📚 بكالوريا أدبي")],
       
        [KeyboardButton("ℹ️ Info")]
    ],
    resize_keyboard=True
)


BOOKS_MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📘 Grammar PDF")],
        [KeyboardButton("📗 Vocabulary PDF")],
        [KeyboardButton("📕 Reading PDF")],
        [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
    ],
    resize_keyboard=True
)

SUB_MENU = ReplyKeyboardMarkup(
    [[KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]],
    resize_keyboard=True
)


# ===== start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.add(update.effective_user.id)
    save_users()

    await update.message.reply_text(
        "Welcome 👋\nChoose an option:",
        reply_markup=MAIN_MENU
    )


# ===== أمر البث =====
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data[WAITING_TEXT] = True
    context.user_data[WAITING_PHOTO] = True
    context.user_data[WAITING_AUDIO] = True

    await update.message.reply_text("📢 أرسل الآن نص / صورة / صوت")


# ===== بث صورة =====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.user_data.get(WAITING_PHOTO):
        return

    photo = update.message.photo[-1]
    caption = update.message.caption or ""

    for uid in USERS:
        try:
            await context.bot.send_photo(chat_id=uid, photo=photo.file_id, caption=caption)
        except:
            pass

    context.user_data[WAITING_PHOTO] = False
    await update.message.reply_text("✅ Broadcast sent (photo)")

# ===== بث صوت =====
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.user_data.get(WAITING_AUDIO):
        return

    audio = update.message.audio or update.message.voice
    if not audio:
        return

    for uid in USERS:
        try:
            await context.bot.send_audio(chat_id=uid, audio=audio.file_id)
        except:
            pass

    context.user_data[WAITING_AUDIO] = False
    await update.message.reply_text("✅ Broadcast sent (audio)")

# ===== الرسائل النصية + وظائف البوت =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    USERS.add(update.effective_user.id)
    save_users()

    # ===== بث نص =====
    if context.user_data.get(WAITING_TEXT) and update.effective_user.id == ADMIN_ID:
        for uid in USERS:
            try:
                await context.bot.send_message(chat_id=uid, text=text)
            except:
                pass

        context.user_data[WAITING_TEXT] = False
        await update.message.reply_text("✅ Broadcast sent (text)")
        return

    # ===== كتب PDF =====
    if text == "📘 Grammar PDF":
        waiting = await update.message.reply_text("⏳ جاري تجهيز Grammar…")
        try:
            await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
            with open("pdfs/grammar.pdf", "rb") as f:
                await context.bot.send_document(update.effective_chat.id, f, caption="📘 Grammar PDF")
            await waiting.edit_text("📘 تم إرسال Grammar")
        except:
            await waiting.edit_text("❌ الملف غير موجود!")

    elif text == "📗 Vocabulary PDF":
        waiting = await update.message.reply_text("⏳ جاري تجهيز Vocabulary…")
        try:
            await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
            with open("pdfs/vocabulary.pdf", "rb") as f:
                await context.bot.send_document(update.effective_chat.id, f, caption="📗 Vocabulary PDF")
            await waiting.edit_text("📗 تم إرسال Vocabulary")
        except:
            await waiting.edit_text("❌ الملف غير موجود!")

    elif text == "📕 Reading PDF":
        waiting = await update.message.reply_text("⏳ جاري تجهيز Reading…")
        try:
            await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
            with open("pdfs/reading.pdf", "rb") as f:
                await context.bot.send_document(update.effective_chat.id, f, caption="📕 Reading PDF")
            await waiting.edit_text("📕 تم إرسال Reading")
        except:
            await waiting.edit_text("❌ الملف غير موجود!")

    # ===== قوائم =====
    elif text in ["🎓 بكالوريا علمي", "📚 بكالوريا أدبي"]:
        await update.message.reply_text("📚 اختر الكتاب:", reply_markup=BOOKS_MENU)

    elif text == "✏️ Exercises":
        await update.message.reply_text("Coming soon", reply_markup=SUB_MENU)

    elif text == "ℹ️ Info":
        await update.message.reply_text("بوت تعليمي", reply_markup=SUB_MENU)

    elif text in ["🔙 Back", "🏠 Main Menu"]:
        await update.message.reply_text("Main menu", reply_markup=MAIN_MENU)


# ===== تشغيل =====
def main():
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("⚠️ يرجى ضبط TELEGRAM_BOT_TOKEN في متغيرات البيئة!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
