# admin_add_menu.py
import uuid
from enum import Enum, auto
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json

# =========================
# ملفات التخزين
# =========================
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

# =========================
# جلسات الأدمن المؤقتة
# =========================
admin_sessions = {}

# =========================
# فتح لوحة الأدمن
# =========================
async def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    admin_sessions[admin_id] = {"state": AdminState.NONE, "data": {}}

    buttons = [
        [KeyboardButton("➕ إضافة زر / قائمة")],
        [KeyboardButton("✏️ تعديل زر / قائمة")],
        [KeyboardButton("🗑 حذف زر / قائمة")],
        [KeyboardButton("📢 بث رسالة")],
        [KeyboardButton("🔙 رجوع")]
    ]
    await update.message.reply_text(
        "🛠 لوحة التحكم\nاختر ما تريد:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

# =========================
# بدء إضافة قائمة جديدة
# =========================
async def start_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    admin_sessions[admin_id] = {"state": AdminState.ADD_MENU, "data": {}}
    await update.message.reply_text("📂 أرسل اسم القائمة الجديدة:")

# =========================
# التعامل مع نصوص الأدمن
# =========================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(
            f"✅ تم إنشاء القائمة: {menu_name}\n"
            "✍️ أرسل اسم الزر الأول أو أرسل ملفاً لربطه بالزر."
        )

    # -------- BROADCAST --------
    elif state == AdminState.BROADCAST:
        message = text
        users = load_json("storage/users.json") or []
        for uid in users:
            try:
                await context.bot.send_message(uid, message)
            except:
                pass
        await update.message.reply_text("📣 تم إرسال البث للجميع")
        session["state"] = AdminState.NONE
        session["data"] = {}

    # -------- حالة غير معرفة --------
    else:
        await update.message.reply_text("❓ أمر غير معروف في هذه الحالة.")

# =========================
# التعامل مع الملفات وربطها بالزر
# =========================
async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]

    if state != AdminState.ADD_FILE_BUTTON:
        await update.message.reply_text("❌ لا يوجد زر في انتظار ملف")
        return

    file = update.message.document or update.message.audio or update.message.video
    if not file:
        await update.message.reply_text("❌ أرسل ملفًا صالحًا")
        return

    # إنشاء معرف فريد للملف
    file_uuid = str(uuid.uuid4())
    file_name = getattr(file, "file_name", getattr(file, "title", "غير معروف"))

    # حفظ الملف في files.json
    files_data = load_json(FILES_FILE) or {"version":1, "files":[], "meta":{}}
    files_data["files"].append({
        "id": file_uuid,
        "telegram_file_id": file.file_id,
        "name": file_name
    })
    save_json(FILES_FILE, files_data)

    # ربط الزر بالقائمة في sections.json
    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    button_name = file_name
    sections.setdefault("main", {}).setdefault("buttons", {})[button_name] = {
        "type": "file",
        "file_id": file_uuid
    }
    save_json(SECTIONS_FILE, sections)

    await update.message.reply_text(f"✅ تم ربط الزر بالملف: {button_name}")
    session["state"] = AdminState.NONE
    session["data"] = {}

# =========================
# التعامل مع ضغط المستخدمين العاديين على الزر
# =========================
async def handle_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    files_data = load_json(FILES_FILE) or {"files": []}

    button_data = sections.get("main", {}).get("buttons", {}).get(text)
    if not button_data:
        return await update.message.reply_text("⚠️ هذا الزر غير موجود.")

    if button_data.get("type") == "file":
        file_id = button_data.get("file_id")
        file_entry = next((f for f in files_data.get("files", []) if f.get("id") == file_id), None)
        if not file_entry:
            return await update.message.reply_text("❌ الملف المرتبط بالزر غير موجود.")

        try:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_entry.get("telegram_file_id"),
                caption=file_entry.get("name", "📄 ملف")
            )
        except Exception as e:
            await update.message.reply_text(f"❌ فشل إرسال الملف: {e}")
