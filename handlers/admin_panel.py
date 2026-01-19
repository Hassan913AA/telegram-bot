# handlers/admin_panel.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    لوحة تحكم الإدمن الرئيسية
    """
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        await update.message.reply_text("❌ أنت لست الإدمن.")
        return

    buttons = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📂 رفع ملف وربطه بزر")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]

    await update.message.reply_text(
        "🛠 لوحة تحكم الأدمن",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


# ============================
# إضافة زر / قائمة
# ============================
async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    context.user_data["state"] = "ADDING_BUTTON"
    await update.message.reply_text(
        "📌 أرسل اسم الزر الجديد أو اسم القائمة الجديدة:"
    )


# ============================
# رفع ملف وربطه بزر
# ============================
async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    context.user_data["state"] = "UPLOADING_FILE"
    await update.message.reply_text(
        "📂 أرسل اسم الزر الذي تريد ربط ملف به:"
    )


# ============================
# تعديل زر أو قائمة
# ============================
async def edit_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    context.user_data["state"] = "EDITING_BUTTON"
    await update.message.reply_text(
        "✏️ أرسل اسم الزر أو القائمة التي تريد تعديلها:"
    )


# ============================
# حذف زر أو قائمة
# ============================
async def delete_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    context.user_data["state"] = "DELETING_BUTTON"
    await update.message.reply_text(
        "🗑 أرسل اسم الزر أو القائمة التي تريد حذفها:"
    )


# ============================
# الرجوع للقائمة الرئيسية
# ============================
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 تم الرجوع للقائمة الرئيسية",
        reply_markup=main_menu_keyboard(is_admin=True)
    )


# ============================
# معالجة النصوص داخل لوحة الأدمن
# ============================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    sections = load_json(SECTIONS_FILE) or {}

    # -----------------------------
    # إضافة زر أو قائمة جديدة
    # -----------------------------
    if state == "ADDING_BUTTON":
        if text in sections:
            await update.message.reply_text("⚠️ هذا الزر أو القائمة موجود مسبقًا.")
            return

        sections[text] = {"file": None, "sub_buttons": {}}
        save_json(SECTIONS_FILE, sections)
        context.user_data["state"] = None
        await update.message.reply_text(f"✅ تم إنشاء الزر/القائمة: {text}")
        return

    # -----------------------------
    # رفع ملف وربطه بزر
    # -----------------------------
    elif state == "UPLOADING_FILE":
        if text not in sections:
            await update.message.reply_text("❌ هذا الزر غير موجود.")
            return

        context.user_data["target_button"] = text
        context.user_data["state"] = "WAITING_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف لربطه بهذا الزر:")
        return

    # -----------------------------
    # تعديل زر أو قائمة
    # -----------------------------
    elif state == "EDITING_BUTTON":
        if text not in sections:
            await update.message.reply_text("❌ هذا الزر/القائمة غير موجود.")
            return

        context.user_data["target_button"] = text
        context.user_data["state"] = "WAITING_EDIT"
        await update.message.reply_text(
            "✏️ أرسل الاسم الجديد للزر/القائمة:"
        )
        return

    # -----------------------------
    # حذف زر أو قائمة
    # -----------------------------
    elif state == "DELETING_BUTTON":
        if text not in sections:
            await update.message.reply_text("❌ هذا الزر/القائمة غير موجود.")
            return

        del sections[text]
        save_json(SECTIONS_FILE, sections)
        context.user_data["state"] = None
        await update.message.reply_text(f"✅ تم حذف الزر/القائمة: {text}")
        return


# ============================
# معالجة الملفات المرفوعة من الأدمن
# ============================
async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    if context.user_data.get("state") != "WAITING_FILE":
        return

    doc = update.message.document
    if not doc:
        await update.message.reply_text("❌ أرسل ملفًا من فضلك.")
        return

    file_name = doc.file_name
    file_id = doc.file_id
    button = context.user_data.get("target_button")
    sections = load_json(SECTIONS_FILE) or {}

    sections[button]["file"] = {"file_name": file_name, "file_id": file_id}
    save_json(SECTIONS_FILE, sections)

    context.user_data["state"] = None
    context.user_data["target_button"] = None

    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {button}")
