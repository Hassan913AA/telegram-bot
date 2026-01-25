import uuid
from enum import Enum, auto
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json

SECTIONS_FILE = "storage/sections.json"
FILES_FILE = "storage/files.json"

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
# ذاكرة الجلسة المؤقتة
# =========================
admin_sessions = {}

# =========================
# فتح لوحة الأدمن
# =========================
def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    admin_sessions[admin_id] = {"state": AdminState.NONE, "data": {}}
    buttons = [
        [KeyboardButton("➕ إضافة زر / قائمة")],
        [KeyboardButton("✏️ تعديل زر / قائمة")],
        [KeyboardButton("🗑 حذف زر / قائمة")],
        [KeyboardButton("📢 بث رسالة")],
        [KeyboardButton("🔙 رجوع")]
    ]
    update.message.reply_text(
        "🛠 لوحة التحكم\nاختر ما تريد:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

# =========================
# البدء بإضافة قائمة
# =========================
def start_add_menu(update: Update, context):
    admin_id = update.effective_user.id
    admin_sessions[admin_id] = {"state": AdminState.ADD_MENU, "data": {}}
    update.message.reply_text("📂 أرسل اسم القائمة الجديدة:")

# =========================
# التعامل مع نصوص الأدمن
# =========================
def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    text = update.message.text.strip()

    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]

    # -------- ADD_MENU --------
    if state == AdminState.ADD_MENU:
        menu_name = text
        session["data"]["menu_name"] = menu_name
        session["state"] = AdminState.ADD_FILE_BUTTON
        update.message.reply_text(f"✅ تم إنشاء القائمة: {menu_name}\n✍️ أرسل اسم الزر الأول أو أرسل ملفاً لربطه بالزر.")

    # -------- BROADCAST --------
    elif state == AdminState.BROADCAST:
        message = text
        users = load_json("storage/users.json") or []
        for uid in users:
            try:
                context.bot.send_message(uid, message)
            except:
                pass
        update.message.reply_text("📣 تم إرسال البث للجميع")
        session["state"] = AdminState.NONE

    # -------- أوامر أخرى placeholder --------
    else:
        update.message.reply_text("❓ أمر غير معروف في هذه الحالة.")

# =========================
# التعامل مع الملفات
# =========================
def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]

    if state != AdminState.ADD_FILE_BUTTON:
        update.message.reply_text("❌ لا يوجد زر في انتظار ملف")
        return

    file = update.message.document or update.message.audio or update.message.video
    if not file:
        update.message.reply_text("❌ أرسل ملفًا صالحًا")
        return

    # إنشاء معرف فريد للملف
    file_uuid = str(uuid.uuid4())

    # حفظ الملف في files.json
    files_data = load_json(FILES_FILE) or {"version":1, "files":[], "meta":{}}
    files_data["files"].append({
        "id": file_uuid,
        "telegram_file_id": file.file_id,
        "name": file.file_name
    })
    save_json(FILES_FILE, files_data)

    # ربط الزر بالقائمة في sections.json
    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    menu_name = session["data"].get("menu_name", "main")
    button_name = session["data"].get("new_button_name", file.file_name)

    sections.setdefault("main", {}).setdefault("buttons", {})[button_name] = {
        "type": "file",
        "file_id": file_uuid
    }
    save_json(SECTIONS_FILE, sections)

    update.message.reply_text(f"✅ تم ربط الزر بالملف: {button_name}")
    session["state"] = AdminState.NONE
    session["data"] = {}
