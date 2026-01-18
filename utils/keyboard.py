# utils/keyboard.py

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# =======================
# القوائم العادية
# =======================
def get_main_menu(is_admin: bool = False):
    """
    القائمة الرئيسية لجميع المستخدمين
    """
    buttons = [
        [KeyboardButton("📚 تصفح الكتب"), KeyboardButton("🔍 بحث")],
        [KeyboardButton("ℹ️ معلومات")]
    ]

    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة الإدارة")])

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_books_menu():
    """
    قائمة الكتب
    """
    buttons = [
        [KeyboardButton("📘 Grammar PDF"), KeyboardButton("📗 Vocabulary PDF")],
        [KeyboardButton("📕 Reading PDF"), KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

# =======================
# قوائم البث للإدمن
# =======================
def get_admin_broadcast_menu():
    """
    قائمة البث الخاصة بالإدمن
    """
    buttons = [
        [KeyboardButton("✍️ إرسال نص")],
        [KeyboardButton("🖼 إرسال صورة")],
        [KeyboardButton("🎵 إرسال صوت")],
        [KeyboardButton("🔙 رجوع")]
    ]
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

# =======================
# القائمة الخاصة بالإدمن العامة
# =======================
def get_admin_menu():
    """
    لوحة التحكم الرئيسية للادمن
    """
    buttons = [
        [KeyboardButton("📢 بث رسالة")],
        [KeyboardButton("📤 رفع كتاب")],
        [KeyboardButton("🛠 إدارة البوت")],
        [KeyboardButton("🔙 رجوع")]
    ]
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

# =======================
# أزرار إنلاين للملفات
# =======================
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
