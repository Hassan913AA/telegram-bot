# admin_add_menu.py
import uuid
from enum import Enum, auto
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json

SECTIONS_FILE = "storage/sections.json"
FILES_FILE = "storage/files.json"

class AdminState(Enum):
    NONE = auto()
    ADD_MENU = auto()
    ADD_FILE_BUTTON = auto()
    BROADCAST = auto()

admin_sessions = {}

async def start_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    admin_sessions[admin_id] = {"state": AdminState.ADD_MENU, "data": {}}
    await update.message.reply_text("📂 أرسل اسم القائمة الجديدة:")

async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    text = update.message.text.strip()

    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    state = session["state"]

    if state == AdminState.ADD_MENU:
        session["data"]["menu_name"] = text
        session["state"] = AdminState.ADD_FILE_BUTTON
        await update.message.reply_text("✍️ أرسل ملفاً لربطه بزر.")

    elif state == AdminState.BROADCAST:
        users = load_json("storage/users.json") or []
        for uid in users:
            try:
                await context.bot.send_message(uid, text)
            except:
                pass
        await update.message.reply_text("📣 تم إرسال البث")
        session["state"] = AdminState.NONE
        session["data"] = {}

async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    if admin_id not in admin_sessions:
        return

    session = admin_sessions[admin_id]
    if session["state"] != AdminState.ADD_FILE_BUTTON:
        return

    file = update.message.document or update.message.audio or update.message.video
    if not file:
        return

    file_uuid = str(uuid.uuid4())
    file_name = getattr(file, "file_name", "ملف")

    files_data = load_json(FILES_FILE) or {"files": []}
    files_data["files"].append({
        "id": file_uuid,
        "telegram_file_id": file.file_id,
        "name": file_name
    })
    save_json(FILES_FILE, files_data)

    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    sections.setdefault("main", {}).setdefault("buttons", {})[file_name] = {
        "type": "file",
        "file_id": file_uuid
    }
    save_json(SECTIONS_FILE, sections)

    await update.message.reply_text(f"✅ تم ربط الزر بالملف: {file_name}")
    session["state"] = AdminState.NONE
    session["data"] = {}

async def handle_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    sections = load_json(SECTIONS_FILE) or {"main": {"buttons": {}}}
    files_data = load_json(FILES_FILE) or {"files": []}

    button = sections.get("main", {}).get("buttons", {}).get(text)
    if not button:
        return

    if button.get("type") == "file":
        file_id = button.get("file_id")
        file_entry = next((f for f in files_data["files"] if f["id"] == file_id), None)
        if not file_entry:
            return

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file_entry["telegram_file_id"],
            caption=file_entry["name"]
        )
