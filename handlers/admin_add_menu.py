# admin_add_menu.py
import uuid
from enum import Enum, auto
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json

# ملفات التخزين
SECTIONS_FILE = "storage/sections.json"
FILES_FILE = "storage/files.json"

# =========================
# حالات الأدمن (State Machine)
# =========================
class AdminState(Enum):
    NONE = auto()
    ADD_MENU = auto()
    ADD_FILE_BUTTON = auto()
    BROADCAST = auto()
    # يمكن إضافة الحالات الأخرى لاحقًا: EDIT_BUTTON, DELETE_BUTTON, MOVE_BUTTON

# =========================
# جلسات الأدمن المؤقتة
# =========================
admin_sessions = {}
"""
admin_sessions = {
    admin_id: {
        "state": AdminState.ADD_MENU,
        "data": {
            "menu_name": str,
            "new_button_name": str
        }
    }
}
"""

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
# بدء إضافة قائمة جديدة
# =========================
def start_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        update.message.reply_text(
            f"✅ تم إنشاء القائمة: {menu_name}\n"
            "✍️ أرسل اسم الزر الأول أو أرسل ملفاً لربطه بالزر."
        )

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
        session["data"] = {}

    # -------- حالة غير معرفة --------
    else:
        update.message.reply_text("❓ أمر غير معروف في هذه الحالة.")

# =========================
# التعامل مع الملفات وربطها بالزر
# =========================
def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]
    # =========================
# إضافة: التعامل مع ضغط المستخدمين العاديين على الزر
# =========================
async def handle_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    هذه الدالة تتعامل مع الضغط على أي زر من المستخدم العادي.
    إذا كان الزر مرتبطًا بملف، يقوم البوت بإرسال الملف مباشرة.
    """

    text = update.message.text.strip()

    # تحميل الأقسام والملفات
    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    files_data = load_json(FILES_FILE) or {"files": []}

    # البحث في الزر ضمن القائمة الرئيسية فقط في هذه النسخة
    button_data = sections.get("main", {}).get("buttons", {}).get(text)
    if not button_data:
        # زر غير موجود، يمكن إضافة رسائل أخرى لاحقًا
        return await update.message.reply_text("⚠️ هذا الزر غير موجود.")

    if button_data.get("type") == "file":
        file_id = button_data.get("file_id")
        # البحث عن الملف في files.json
        file_entry = next((f for f in files_data.get("files", []) if f.get("id") == file_id), None)
        if not file_entry:
            return await update.message.reply_text("❌ الملف المرتبط بالزر غير موجود.")

        # إرسال الملف مباشرة
        try:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_entry.get("telegram_file_id"),
                caption=file_entry.get("name", "📄 ملف")
            )
        except Exception as e:
            return await update.message.reply_text(f"❌ فشل إرسال الملف: {e}")

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
        "name": getattr(file, "file_name", "غير معروف")
    })
    save_json(FILES_FILE, files_data)

    # ربط الزر بالقائمة في sections.json
    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    menu_name = session["data"].get("menu_name", "main")
    button_name = getattr(file, "file_name", "زر جديد")  # اسم الزر من اسم الملف
    sections.setdefault("main", {}).setdefault("buttons", {})[button_name] = {
        "type": "file",
        "file_id": file_uuid
    }
    save_json(SECTIONS_FILE, sections)

    update.message.reply_text(f"✅ تم ربط الزر بالملف: {button_name}")
    session["state"] = AdminState.NONE
    session["data"] = {}
