# bot/keyboards.py

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard(is_admin: bool = False):
    """
    لوحة المفاتيح الرئيسية
    """
    buttons = [
        [KeyboardButton("📚 تصفح الكتب"), KeyboardButton("📤 رفع كتاب")],
        [KeyboardButton("🔍 بحث"), KeyboardButton("ℹ️ معلومات")]
    ]

    if is_admin:
        buttons.append([KeyboardButton("📢 بث رسالة")])

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def admin_broadcast_keyboard():
    """
    لوحة خاصة بخيارات البث للإدمن
    """
    buttons = [
        [KeyboardButton("✍️ إرسال نص")],
        [KeyboardButton("🖼 إرسال صورة")],
        [KeyboardButton("🎵 إرسال صوت")],
        [KeyboardButton("🔙 رجوع للقائمة")]
    ]

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def inline_file_actions(file_id: str):
    """
    أزرار إنلاين خاصة بالملفات (تحميل / حذف مثلاً)
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬇️ تحميل", callback_data=f"download:{file_id}"),
            InlineKeyboardButton("🗑 حذف", callback_data=f"delete:{file_id}")
        ]
    ])
