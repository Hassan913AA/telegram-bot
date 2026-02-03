# admin_panel.py
import os
import shutil
from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard

SECTIONS_FILE = "storage/sections.json"
BACKUP_FILE = "storage/sections_backup.json"


def backup_sections():
    if os.path.exists(SECTIONS_FILE):
        shutil.copy(SECTIONS_FILE, BACKUP_FILE)


def is_admin(user_id, context):
    return user_id == context.bot_data.get("ADMIN")


async def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id, context):
        return

    # 🧠 توحيد الحالة
    context.user_data["state"] = "ADMIN_PANEL"
    context.user_data["path"] = []

    # 🧩 إضافة هندسية: تسجيل أننا داخل لوحة الأدمن (لـ UX و Router)
    context.user_data["in_admin"] = True

    await update.message.reply_text(
        "🛠 لوحة تحكم الأدمن:",
        reply_markup=admin_panel_keyboard()
    )


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🧹 خروج من الحالات فقط – بدون مسح عنيف
    context.user_data.pop("state", None)
    context.user_data.pop("path", None)

    # 🧩 إضافة هندسية: الخروج من وضع الأدمن
    context.user_data.pop("in_admin", None)

    await update.message.reply_text(
        "🏠 رجوع للقائمة الرئيسية",
        reply_markup=main_menu_keyboard(
            is_admin=is_admin(update.effective_user.id, context)
        )
    )


# 🧩 ================= إضافات هندسية جديدة =================

async def handle_admin_panel_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    🧠 Router خاص بلوحة الأدمن
    يمنع التضارب مع menu_handler و admin_add_menu
    """
    if not context.user_data.get("in_admin"):
        return

    text = update.message.text.strip()

    # ➕ إضافة زر / قائمة
    if text == "➕ إضافة زر / قائمة":
        context.user_data["state"] = "ADMIN_ADD_MENU"
        await update.message.reply_text("📂 اختر نوع الإضافة:")
        return

    # ✏️ تعديل زر / قائمة
    if text == "✏️ تعديل زر / قائمة":
        context.user_data["state"] = "ADMIN_EDIT"
        await update.message.reply_text("✏️ اختر نوع التعديل:")
        return

    # 🗑 حذف زر / قائمة
    if text == "🗑 حذف زر / قائمة":
        context.user_data["state"] = "ADMIN_DELETE"
        await update.message.reply_text("🗑 اختر نوع الحذف:")
        return

    # 📢 إرسال رسالة جماعية
    if text == "📢 إرسال رسالة جماعية":
        context.user_data["state"] = "BROADCAST_TEXT"
        await update.message.reply_text("📣 أرسل نص الرسالة:")
        return

    # 🔙 رجوع
    if text == "🔙 Back":
        return await back_to_main(update, context)
