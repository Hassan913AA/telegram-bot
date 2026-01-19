# handlers/admin_panel.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard

SECTIONS_FILE = "storage/sections.json"


def admin_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("➕ إضافة قائمة أو زر")],
            [KeyboardButton("✏️ تعديل زر أو قائمة")],
            [KeyboardButton("🗑 حذف زر أو قائمة")],
            [KeyboardButton("📂 ربط زر بملف")],
            [KeyboardButton("📢 بث رسالة")],
            [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
        ],
        resize_keyboard=True
    )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return await update.message.reply_text("❌ أنت لست الإدمن.")

    await update.message.reply_text(
        "🛠 لوحة تحكم الأدمن",
        reply_markup=admin_keyboard()
    )


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ========== أوامر اللوحة ==========
    if text == "➕ إضافة قائمة أو زر":
        context.user_data["state"] = "ADD_NAME"
        return await update.message.reply_text("✍️ أرسل اسم الزر أو القائمة الجديدة:")

    if text == "📂 ربط زر بملف":
        context.user_data["state"] = "LINK_BUTTON"
        return await update.message.reply_text("🔗 أرسل اسم الزر الذي تريد ربطه بملف:")

    if text == "📢 بث رسالة":
        context.user_data["state"] = "BROADCAST"
        return await update.message.reply_text("📢 أرسل النص / الصورة / الصوت للبث:")

    if text == "🔙 رجوع للقائمة الرئيسية":
        context.user_data.clear()
        return await update.message.reply_text(
            "🏠 القائمة الرئيسية",
            reply_markup=main_menu_keyboard(is_admin=True)
        )

    # ========== إضافة زر ==========
    if state == "ADD_NAME":
        if text in data:
            return await update.message.reply_text("⚠️ الاسم موجود مسبقًا.")

        context.user_data["new_name"] = text
        context.user_data["state"] = "ADD_TYPE"
        return await update.message.reply_text("📌 هل هذا زر قائمة أم زر ملف؟ أرسل: menu أو file")

    if state == "ADD_TYPE":
        name = context.user_data["new_name"]

        if text.lower() == "menu":
            data[name] = {"type": "menu", "items": {}}
            save_json(SECTIONS_FILE, data)
            context.user_data.clear()
            return await update.message.reply_text(f"✅ تم إنشاء قائمة: {name}")

        if text.lower() == "file":
            data[name] = {"type": "file", "path": None, "caption": name}
            save_json(SECTIONS_FILE, data)
            context.user_data.clear()
            return await update.message.reply_text(f"✅ تم إنشاء زر ملف: {name}")

        return await update.message.reply_text("❌ أرسل فقط: menu أو file")

    # ========== ربط زر بملف ==========
    if state == "LINK_BUTTON":
        if text not in data or data[text]["type"] != "file":
            return await update.message.reply_text("❌ هذا ليس زر ملف.")

        context.user_data["target_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        return await update.message.reply_text("📎 الآن أرسل الملف:")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    if not doc:
        return await update.message.reply_text("❌ أرسل ملفًا.")

    data = load_json(SECTIONS_FILE) or {}
    name = context.user_data["target_button"]

    file = await doc.get_file()
    path = f"uploads/{doc.file_name}"
    await file.download_to_drive(path)

    data[name]["path"] = path
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {name}")
