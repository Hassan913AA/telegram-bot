# handlers/admin_panel.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


# ============================
# لوحة تحكم الأدمن
# ============================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        await update.message.reply_text("❌ أنت لست الأدمن.")
        return

    buttons = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📂 ربط ملف بزر")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]

    await update.message.reply_text(
        "🛠 لوحة تحكم الأدمن",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


# ============================
# أوضاع الأدمن
# ============================
async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PARENT"
    await update.message.reply_text("📌 أرسل اسم القائمة التي تريد الإضافة داخلها (أو اكتب /root للقائمة الرئيسية):")


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_TARGET"
    await update.message.reply_text("📎 أرسل اسم الزر الذي تريد ربط ملف به:")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🏠 تم الرجوع للقائمة الرئيسية",
        reply_markup=main_menu_keyboard(is_admin=True)
    )


# ============================
# معالجة النصوص حسب الحالة
# ============================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != context.bot_data.get("ADMIN"):
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة زر داخل قائمة =====
    if state == "ADD_PARENT":
        context.user_data["parent"] = None if text == "/root" else text
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        parent = context.user_data.get("parent")

        if parent:
            if parent not in data:
                await update.message.reply_text("❌ هذه القائمة غير موجودة.")
                return
            data[parent].setdefault("sub_buttons", {})
            data[parent]["sub_buttons"][text] = {"file": None, "sub_buttons": {}}
        else:
            data[text] = {"file": None, "sub_buttons": {}}

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء الزر/القائمة: {text}")
        return

    # ===== ربط ملف بزر =====
    if state == "FILE_TARGET":
        context.user_data["target_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return

    # ===== بث جماعي =====
    if state == "BROADCAST":
        context.bot_data["BROADCAST_CONTENT"] = update.message
        context.user_data.clear()
        await update.message.reply_text("✅ تم حفظ رسالة البث.")
        return


# ============================
# استقبال الملفات من الأدمن
# ============================
async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    if not doc:
        await update.message.reply_text("❌ أرسل ملفًا فقط.")
        return

    data = load_json(SECTIONS_FILE) or {}
    target = context.user_data.get("target_button")

    if target not in data:
        await update.message.reply_text("❌ هذا الزر غير موجود.")
        return

    data[target]["file"] = {
        "file_id": doc.file_id,
        "file_name": doc.file_name
    }

    save_json(SECTIONS_FILE, data)
    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {target}")
