from telegram import ReplyKeyboardMarkup, KeyboardButton

# ==========================
# القائمة الرئيسية
# ==========================
def main_menu_keyboard(is_admin=False):
    """
    القائمة الرئيسية للمستخدم أو الأدمن
    """
    buttons = [
        [KeyboardButton("📂 القوائم")],  # للمستخدم العادي
    ]

    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة الأدمن")])  # يظهر فقط للأدمن

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# لوحة الأدمن الرئيسية
# ==========================
def admin_panel_keyboard():
    """
    الكيبورد الرئيسي للأدمن
    """
    buttons = [
        [KeyboardButton("➕ إضافة زر / قائمة")],
        [KeyboardButton("✏️ تعديل زر / قائمة")],
        [KeyboardButton("🗑 حذف زر / قائمة")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# إضافة زر / قائمة
# =========================
