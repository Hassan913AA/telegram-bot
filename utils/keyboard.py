from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from services.storage_service import load_json

SECTIONS_FILE = "storage/sections.json"


def main_menu_keyboard(is_admin: bool = False):
    """
    يبني القائمة الرئيسية من sections.json
    """
    data = load_json(SECTIONS_FILE) or {}

    buttons = []

    for section_name in data.keys():
        buttons.append([KeyboardButton(section_name)])

    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة التحكم")])

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def admin_panel_keyboard():
    """
    لوحة تحكم الإدمن
    """
    buttons = [
        [KeyboardButton("➕ إضافة زر جديد")],
        [KeyboardButton("📂 رفع ملف وربطه بزر")],
        [KeyboardButton("📢 بث رسالة")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def inline_file_actions(file_id: str):
    """
    أزرار إنلاين للملفات
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬇️ تحميل", callback_data=f"download:{file_id}"),
            InlineKeyboardButton("🗑 حذف", callback_data=f"delete:{file_id}")
        ]
    ])
