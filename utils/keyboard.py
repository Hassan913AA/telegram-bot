from telegram import ReplyKeyboardMarkup, KeyboardButton

# ==========================
# القائمة الرئيسية
# ==========================
def main_menu_keyboard(is_admin=False):
    buttons = [[KeyboardButton("📂 القوائم")]]
    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة الأدمن")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# لوحة الأدمن الرئيسية
# ==========================
def admin_panel_keyboard():
    buttons = [
        [KeyboardButton("➕ إضافة زر / قائمة")],
        [KeyboardButton("✏️ تعديل زر / قائمة")],
        [KeyboardButton("🗑 حذف زر / قائمة")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 Back")]  # توحيد الاسم مع الحالة الهندسية
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# إضافة زر / قائمة
# ==========================
def add_menu_keyboard():
    buttons = [
        [KeyboardButton("📁 إنشاء قائمة جديدة")],
        [KeyboardButton("📎 إنشاء زر يرسل ملف")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# التعديل
# ==========================
def edit_menu_keyboard():
    buttons = [
        [KeyboardButton("✏️ تعديل اسم زر")],
        [KeyboardButton("📂 نقل زر إلى قائمة أخرى")],
        [KeyboardButton("📁 تعديل اسم قائمة")],
        [KeyboardButton("↩️ التراجع عن آخر تعديل")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# الحذف
# ==========================
def delete_menu_keyboard():
    buttons = [
        [KeyboardButton("🗑 حذف زر")],
        [KeyboardButton("🗑 حذف قائمة كاملة")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# الإرسال الجماعي
# ==========================
def broadcast_keyboard():
    buttons = [
        [KeyboardButton("✉️ نص")],
        [KeyboardButton("🖼 صورة")],
        [KeyboardButton("🎵 صوت")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# كيبورد داخل القوائم (للمستخدم)
# ==========================
def user_menu_keyboard(menu_buttons, is_admin=False):
    """
    🎯 ذكي: يضيف زر رجوع مختلف حسب الدور
    """
    buttons = [[KeyboardButton(btn)] for btn in menu_buttons]

    # 🧩 زر رجوع ذكي
    if is_admin:
        buttons.append([KeyboardButton("🔙 رجوع (أدمن)")])
    else:
        buttons.append([KeyboardButton("🔙 رجوع")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# ==========================
# زر رجوع عام
# ==========================
def back_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 رجوع")]], resize_keyboard=True)


# ==========================
# زر رجوع للقائمة الرئيسية دائمًا
# ==========================
def home_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("🏠 القائمة الرئيسية")]], resize_keyboard=True)
