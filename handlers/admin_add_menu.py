# admin_add_menu.py (Re-engineered)

import uuid
from telegram import Update
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json

SECTIONS_FILE = "storage/sections.json"
FILES_FILE = "storage/files.json"


# ======================
# 🟢 بدء إضافة قائمة
# ======================
async def start_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_NAME"
    context.user_data["flow_data"] = {}
    await update.message.reply_text("📂 أرسل اسم القائمة الجديدة:")


# ======================
# 🟢 معالجة نص الأدمن
# ======================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip()

    # --- انتظار اسم القائمة ---
    if state == "ADMIN_ADD_MENU_WAIT_NAME":
        context.user_data["flow_data"]["menu_name"] = text
        context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف الذي سيرتبط بهذا الزر.")
        return

    # --- بث رسالة ---
    if state == "ADMIN_BROADCAST_TEXT":
        users = load_json("storage/users.json") or []
        for uid in users:
            try:
                await context.bot.send_message(uid, text)
            except:
                pass
        await update.message.reply_text("📣 تم إرسال الرسالة الجماعية بنجاح.")
        context.user_data.clear()
        return


# ======================
# 🟢 معالجة ملف الأدمن
# ======================
async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    if state != "ADMIN_ADD_MENU_WAIT_FILE":
        return

    file = update.message.document or update.message.audio or update.message.video
    if not file:
        return

    file_uuid = str(uuid.uuid4())
    file_name = getattr(file, "file_name", "ملف")

    # حفظ الملف في files.json
    files_data = load_json(FILES_FILE) or {"files": []}
    files_data["files"].append({
        "id": file_uuid,
        "telegram_file_id": file.file_id,
        "name": file_name
    })
    save_json(FILES_FILE, files_data)

    # حفظ الزر في sections.json
    sections = load_json(SECTIONS_FILE) or {}
    sections.setdefault("root", {}).setdefault("sub", {})[file_name] = {
        "file": {
            "file_id": file.file_id,
            "file_name": file_name
        }
    }
    save_json(SECTIONS_FILE, sections)

    await update.message.reply_text(f"✅ تم إنشاء زر وربطه بالملف: {file_name}")

    # إنهاء الجلسة
    context.user_data.clear()


# ======================
# 🟢 زر المستخدم يرسل ملف
# ======================
async def handle_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    sections = load_json(SECTIONS_FILE) or {}

    root = sections.get("root", {}).get("sub", {})
    item = root.get(text)

    if not item:
        return

    if item.get("file"):
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=item["file"]["file_id"],
            caption=item["file"]["file_name"]
        )
