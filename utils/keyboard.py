from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu(is_admin: bool = False):
    buttons = [
        [KeyboardButton("📚 تصفح الكتب"), KeyboardButton("🔍 بحث")],
        [KeyboardButton("ℹ️ معلومات")]
    ]

    if is_admin:
        buttons.append([KeyboardButton("📢 بث رسالة")])

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )


def get_books_menu():
    buttons = [
        [KeyboardButton("📘 Grammar PDF")],
        [KeyboardButton("📗 Vocabulary PDF")],
        [KeyboardButton("📕 Reading PDF")],
        [KeyboardButton("🔙 رجوع")]
    ]

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )


def get_admin_broadcast_menu():
    buttons = [
        [KeyboardButton("✍️ إرسال نص")],
        [KeyboardButton("🖼 إرسال صورة")],
        [KeyboardButton("🎵 إرسال صوت")],
        [KeyboardButton("🔙 رجوع")]
    ]

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )


def inline_file_actions(file_id: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬇️ تحميل", callback_data=f"download:{file_id}"),
            InlineKeyboardButton("🗑 حذف", callback_data=f"delete:{file_id}")
        ]
    ])
