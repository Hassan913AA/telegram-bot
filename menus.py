from telegram import ReplyKeyboardMarkup, KeyboardButton

MAIN_MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🎓 بكالوريا علمي"), KeyboardButton("📚 بكالوريا أدبي")],
        [KeyboardButton("ℹ️ Info")]
    ],
    resize_keyboard=True
)

BOOKS_MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📘 Grammar PDF")],
        [KeyboardButton("📗 Vocabulary PDF")],
        [KeyboardButton("📕 Reading PDF")],
        [KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]
    ],
    resize_keyboard=True
)

SUB_MENU = ReplyKeyboardMarkup(
    [[KeyboardButton("🔙 Back"), KeyboardButton("🏠 Main Menu")]],
    resize_keyboard=True
)
