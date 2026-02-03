# admin_add_menu.py (Re-engineered & Smart)
import uuid
from telegram import Update
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json

SECTIONS_FILE = "storage/sections.json"
FILES_FILE = "storage/files.json"

# ======================
# 🟢 بدء إضافة قائمة أو زر ملف
# ======================
async def start_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تهيئة جلسة الأدمن
    context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_NAME"
    context.user_data["flow_data"] = {}
    await update.message.reply_text("📂 أرسل اسم القائمة أو الزر الجديد:")


# ======================
# 🟢 معالجة نص الأدمن
# ======================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip()

    # --- انتظار اسم القائمة / الزر ---
    if state == "ADMIN_ADD_MENU_WAIT_NAME":
        context.user_data["flow_data"]["menu_name"] = text
        context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف الذي سيرتبط بهذا الزر أو اكتب 'لا' للقائمة فقط.")
        return

    # --- بث رسالة جماعية ---
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
# 🟢 معالجة ملف الأدمن + التحديث الذكي للقوائم
# ======================
async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    if state != "ADMIN_ADD_MENU_WAIT_FILE":
        return

    file = update.message.document or update.message.audio or update.message.video

    menu_name = context.user_data["flow_data"]["menu_name"]

    sections = load_json(SECTIONS_FILE) or {}
    if "root" not in sections:
        sections["root"] = {"sub": {}, "buttons": {}}

    root = sections["root"]

    # ----------------------------
    # إذا المستخدم أرسل 'لا' → مجرد قائمة بدون ملف
    # ----------------------------
    if not file or update.message.text == "لا":
        # إضافة القائمة الجديدة داخل root sub
        root["sub"][menu_name] = {"sub": {}, "buttons": {}}
        save_json(SECTIONS_FILE, sections)
        await update.message.reply_text(f"✅ تم إنشاء القائمة الجديدة: {menu_name}")
        context.user_data.clear()
        return

    # ----------------------------
    # حفظ الملف في files.json
    # ----------------------------
    file_uuid = str(uuid.uuid4())
    file_name = getattr(file, "file_name", "ملف")
    files_data = load_json(FILES_FILE) or {"files": []}
    files_data["files"].append({
        "id": file_uuid,
        "telegram_file_id": file.file_id,
        "name": file_name
    })
    save_json(FILES_FILE, files_data)

    # ----------------------------
    # حفظ الزر في sections.json تلقائيًا
    # ----------------------------
    root["buttons"][menu_name] = {
        "file": {
            "file_id": file.file_id,
            "file_name": file_name
        }
    }
    save_json(SECTIONS_FILE, sections)

    await update.message.reply_text(f"✅ تم إنشاء زر وربطه بالملف: {file_name}")
    context.user_data.clear()


# ======================
# 🟢 زر المستخدم يرسل ملف
# ======================
async def handle_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    sections = load_json(SECTIONS_FILE) or {}
    root = sections.get("root", {}).get("sub", {})
    buttons = sections.get("root", {}).get("buttons", {})

    # تحقق أولاً في الأزرار المباشرة
    if text in buttons and buttons[text].get("file"):
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=buttons[text]["file"]["file_id"],
            caption=buttons[text]["file"]["file_name"]
        )
        return

    # تحقق في القوائم الفرعية (sub)
    for menu_name, menu_data in root.items():
        if text in menu_data.get("buttons", {}) and menu_data["buttons"][text].get("file"):
            file_info = menu_data["buttons"][text]
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file"]["file_id"],
                caption=file_info["file"]["file_name"]
            )
            return
