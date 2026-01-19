# bot/handlers/admin_panel.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard

SECTIONS_FILE = "storage/sections.json"


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ أنت لست الإدمن.")
        return

    buttons = [
        [KeyboardButton("➕ إضافة زر جديد")],
        [KeyboardButton("✏️ تعديل زر")],
        [KeyboardButton("🗑 حذف زر")],
        [KeyboardButton("📂 رفع ملف وربطه بزر")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]

    await update.message.reply_text(
        "🛠 لوحة تحكم الإدمن",
        reply_markup=ReplyKeyboardMarkup(
            buttons, resize_keyboard=True
        )
    )


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ أنت لست الإدمن.")
        return

    context.user_data["state"] = "ADDING_BUTTON"
    await update.message.reply_text("📌 أرسل اسم الزر الجديد:")


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data["ADMIN"]:
        return

    context.user_data["state"] = "UPLOADING_FILE"
    await update.message.reply_text("📂 أرسل اسم الزر الذي تريد ربط ملف به:")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 تم الرجوع للقائمة الرئيسية",
        reply_markup=main_menu_keyboard(is_admin=True)
    )


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data["ADMIN"]:
        return

    state = context.user_data.get("state")
    text = update.message.text.strip()

    sections = load_json(SECTIONS_FILE) or {}

    if state == "ADDING_BUTTON":
        if text in sections:
            await update.message.reply_text("⚠️ هذا الزر موجود مسبقًا.")
            return

        sections[text] = {"file": None}
        save_json(SECTIONS_FILE, sections)

        context.user_data["state"] = None
        await update.message.reply_text(f"✅ تم إنشاء الزر: {text}")

    elif state == "UPLOADING_FILE":
        if text not in sections:
            await update.message.reply_text("❌ هذا الزر غير موجود.")
            return

        context.user_data["target_button"] = text
        context.user_data["state"] = "WAITING_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف لربطه بهذا الزر:")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data["ADMIN"]:
        return

    if context.user_data.get("state") != "WAITING_FILE":
        return

    doc = update.message.document
    if not doc:
        await update.message.reply_text("❌ أرسل ملفًا من فضلك.")
        return

    file_name = doc.file_name
    file_id = doc.file_id

    sections = load_json(SECTIONS_FILE) or {}
    button = context.user_data.get("target_button")

    sections[button]["file"] = {
        "file_id": file_id,
        "file_name": file_name
    }

    save_json(SECTIONS_FILE, sections)

    context.user_data["state"] = None
    context.user_data["target_button"] = None

    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {button}")
