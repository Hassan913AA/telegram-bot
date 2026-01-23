from telegram import ReplyKeyboardMarkup, KeyboardButton


# ====== القائمة الرئيسية ======
def main_menu_keyboard(is_admin=False):
    buttons = [
        [KeyboardButton("📂 القوائم")],
    ]

    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة الادمن")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== لوحة الأدمن ======
def admin_panel_keyboard():
    buttons = [
        [KeyboardButton("➕ إضافة زر / قائمة")],
        [KeyboardButton("✏️ تعديل زر أو قائمة")],
        [KeyboardButton("🗑 حذف زر أو قائمة")],
        [KeyboardButton("📢 إرسال رسالة للمستخدمين")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== إضافة زر أو قائمة ======
def add_menu_keyboard():
    buttons = [
        [KeyboardButton("📁 إنشاء قائمة جديدة")],
        [KeyboardButton("🔘 إنشاء زر يرسل رسالة")],
        [KeyboardButton("📎 إنشاء زر يرسل ملف")],
        [KeyboardButton("🔙 رجوع للوحة الادمن")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== التعديل ======
def edit_menu_keyboard():
    buttons = [
        [KeyboardButton("✏️ تعديل اسم زر")],
        [KeyboardButton("📂 نقل زر إلى قائمة أخرى")],
        [KeyboardButton("📁 تعديل اسم قائمة")],
        [KeyboardButton("↩️ تراجع عن آخر تعديل")],
        [KeyboardButton("🔙 رجوع للوحة الادمن")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== الحذف ======
def delete_menu_keyboard():
    buttons = [
        [KeyboardButton("🗑 حذف زر")],
        [KeyboardButton("🗑 حذف قائمة كاملة")],
        [KeyboardButton("🔙 رجوع للوحة الادمن")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== الإرسال الجماعي ======
def broadcast_keyboard():
    buttons = [
        [KeyboardButton("✉️ إرسال نص جماعي")],
        [KeyboardButton("🖼 إرسال صورة جماعية")],
        [KeyboardButton("🎵 إرسال صوت جماعي")],
        [KeyboardButton("🔙 رجوع للوحة الادمن")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== داخل القوائم (للمستخدمين) ======
def user_menu_keyboard(menu_buttons, is_admin=False):
    """
    menu_buttons = قائمة أسماء الأزرار من التخزين (DB أو JSON)
    """
    buttons = []

    for btn in menu_buttons:
        buttons.append([KeyboardButton(btn)])

    if is_admin:
        buttons.append([KeyboardButton("🔙 رجوع (ادمن)")])
    else:
        buttons.append([KeyboardButton("🔙 رجوع")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ====== زر رجوع عام ======
def back_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 رجوع")]], resize_keyboard=True)
