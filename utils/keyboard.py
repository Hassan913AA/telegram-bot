from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard(is_admin=False):
    buttons = []

    # القوائم التي أنشأها المستخدم (تظهر لاحقاً من التخزين)
    buttons.append([KeyboardButton("📂 القوائم")])

    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة الادمن")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def admin_panel_keyboard():
    buttons = [
        [KeyboardButton("➕ إضافة زر / قائمة")],
        [KeyboardButton("✏️ تعديل زر أو قائمة")],
        [KeyboardButton("🗑 حذف زر أو قائمة")],
        [KeyboardButton("📢 إرسال رسالة للمستخدمين")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def add_menu_keyboard():
    buttons = [
        [KeyboardButton("📁 إنشاء قائمة")],
        [KeyboardButton("📎 إضافة زر يرسل ملف")],
        [KeyboardButton("✏️ تعديل زر أو قائمة")],
        [KeyboardButton("🗑 حذف زر")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def broadcast_keyboard():
    buttons = [
        [KeyboardButton("✉️ إرسال نص")],
        [KeyboardButton("🖼 إرسال صورة")],
        [KeyboardButton("🎵 إرسال صوت")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def back_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 Back")]], resize_keyboard=True)


def user_back_only_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 رجوع")]], resize_keyboard=True)
