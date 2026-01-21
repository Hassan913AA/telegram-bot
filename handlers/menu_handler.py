# handlers/menu_handler.py

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard

SECTIONS_FILE = "storage/sections.json"


def get_section_by_path(data, path):
    """يرجع القسم حسب المسار: ['القائمة', 'زر', 'زر فرعي']"""
    current = data
    for p in path:
        current = current.get(p, {}).get("sub_buttons", {})
    return current


async def handle_menu(update, context):
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text.strip()

    try:
        data = load_json(SECTIONS_FILE) or {}
        path = context.user_data.get("path", [])

        # ===== رجوع =====
        if text == "🔙 رجوع":
            if path:
                path.pop()
                context.user_data["path"] = path
            return await show_current_menu(update, context, data, path, is_admin)

        # ===== رجوع للقائمة الرئيسية =====
        if text == "🏠 القائمة الرئيسية":
            context.user_data["path"] = []
            return await update.message.reply_text(
                "🏠 القائمة الرئيسية:",
                reply_markup=main_menu_keyboard(is_admin=is
