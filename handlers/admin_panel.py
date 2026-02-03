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

    await update.message.reply_text(
        "🛠 لوحة تحكم الأدمن:",
        reply_markup=admin_panel_keyboard()
    )


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🧹 خروج من الحالات فقط – بدون مسح عنيف
    context.user_data.pop("state", None)
    context.user_data.pop("path", None)

    await update.message.reply_text(
        "🏠 رجوع للقائمة الرئيسية",
        reply_markup=main_menu_keyboard(
            is_admin=is_admin(update.effective_user.id, context)
        )
    )
