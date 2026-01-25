# admin_panel.py
import os
import shutil
from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard, add_menu_keyboard, broadcast_keyboard
from services.storage_service import load_json, save_json

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
SECTIONS_FILE = "storage/sections.json"
BACKUP_FILE = "storage/sections_backup.json"

def backup_sections():
    if os.path.exists(SECTIONS_FILE):
        shutil.copy(SECTIONS_FILE, BACKUP_FILE)

def is_admin(user_id):
    return user_id == ADMIN_ID

async def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=admin_panel_keyboard())

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 رجوع للقائمة الرئيسية", reply_markup=main_menu_keyboard(is_admin=is_admin(update.effective_user.id)))
