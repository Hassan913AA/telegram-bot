# admin_add_menu.py

from enum import Enum, auto

# =========================
# الحالات (State Machine)
# =========================

class AdminState(Enum):
    NONE = auto()
    ADD_MENU = auto()
    ADD_FILE_BUTTON = auto()
    EDIT_BUTTON = auto()
    MOVE_BUTTON = auto()
    DELETE_BUTTON = auto()
    DELETE_MENU = auto()
    UNDO = auto()
    BROADCAST = auto()


# =========================
# ذاكرة الجلسة (مؤقتة)
# =========================

admin_sessions = {}
"""
admin_sessions = {
    admin_id: {
        "state": AdminState.ADD_MENU,
        "data": {}
    }
}
"""


# =========================
# فتح لوحة الأدمن
# =========================

def open_admin_panel(update, context):
    admin_id = update.effective_user.id

    admin_sessions[admin_id] = {
        "state": AdminState.NONE,
        "data": {}
    }

    update.message.reply_text(
        "🛠 لوحة التحكم\n"
        "اختر ما تريد:\n"
        "- إضافة قائمة\n"
        "- تعديل زر\n"
        "- حذف\n"
        "- بث رسالة"
    )


# =========================
# التعامل مع النصوص
# =========================

def handle_admin_text(update, context):
    admin_id = update.effective_user.id
    text = update.message.text

    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]

    # -------- ADD MENU --------
    if state == AdminState.ADD_MENU:
        menu_name = text.strip()
        session["data"]["menu_name"] = menu_name

        # لاحقًا: إنشاء القائمة فعليًا
        session["state"] = AdminState.ADD_FILE_BUTTON

        update.message.reply_text(
            f"✅ تم إنشاء القائمة: {menu_name}\n"
            "أرسل اسم أول زر."
        )

    # -------- EDIT BUTTON --------
    elif state == AdminState.EDIT_BUTTON:
        # placeholder
        update.message.reply_text("✏️ تعديل الزر (قيد البناء)")

    # -------- DELETE MENU --------
    elif state == AdminState.DELETE_MENU:
        # placeholder
        update.message.reply_text("🗑 حذف القائمة (قيد البناء)")

    # -------- BROADCAST --------
    elif state == AdminState.BROADCAST:
        message = text
        # لاحقًا: إرسال للجميع
        update.message.reply_text("📣 تم إرسال البث (نظريًا 😄)")

    else:
        update.message.reply_text("❓ أمر غير معروف في هذه الحالة.")


# =========================
# التعامل مع الملفات
# =========================

def handle_admin_file(update, context):
    admin_id = update.effective_user.id

    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]

    if state == AdminState.ADD_FILE_BUTTON:
        file = update.message.document or update.message.audio or update.message.video

        if not file:
            update.message.reply_text("❌ أرسل ملفًا صالحًا.")
            return

        # لاحقًا: حفظ الملف وربطه بالزر
        update.message.reply_text("📎 تم استلام الملف وربطه بالزر.")


# =========================
# أوامر مساعدة لتغيير الحالة
# =========================

def start_add_menu(update, context):
    admin_id = update.effective_user.id

    admin_sessions[admin_id] = {
        "state": AdminState.ADD_MENU,
        "data": {}
    }

    update.message.reply_text("📂 أرسل اسم القائمة الجديدة.")


def start_broadcast(update, context):
    admin_id = update.effective_user.id

    admin_sessions[admin_id]["state"] = AdminState.BROADCAST
    update.message.reply_text("📣 أرسل رسالة البث.")
