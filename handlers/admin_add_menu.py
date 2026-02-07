# admin_add_menu.py (Merged & Stable Version – Patched)

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
    """
    بدء Flow الأدمن لإضافة قائمة أو زر ملف
    """
    context.user_data["flow"] = "ADMIN_ADD_MENU"
    context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_NAME"
    context.user_data["flow_data"] = {}
    context.user_data.setdefault("path", [])

    await update.message.reply_text("📂 أرسل اسم القائمة أو الزر الجديد:")


# ======================
# 🟢 معالجة نص الأدمن
# ======================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالجة نص الأدمن حسب الحالة الحالية في flow
    """
    state = context.user_data.get("state")
    text = update.message.text.strip()

    # --- 1️⃣ انتظار اسم القائمة / الزر ---
    if state == "ADMIN_ADD_MENU_WAIT_NAME":
        context.user_data["flow_data"]["menu_name"] = text
        context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_TYPE"
        await update.message.reply_text("✳ هل تريد ربط ملف؟ أرسل (نعم) أو (لا)")
        return

    # --- 2️⃣ تحديد هل هناك ملف ---
    if state == "ADMIN_ADD_MENU_WAIT_TYPE":
        if text == "نعم":
            context.user_data["state"] = "ADMIN_ADD_MENU_WAIT_FILE"
            await update.message.reply_text("📎 أرسل الملف الآن")
            return

        if text == "لا":
            menu_name = context.user_data["flow_data"]["menu_name"]
            _add_menu_only(menu_name)
            await update.message.reply_text(f"✅ تم إنشاء القائمة: {menu_name}")
            _clear_flow(context)
            return

        await update.message.reply_text("❗ الرجاء إرسال (نعم) أو (لا)")
        return

    # --- 3️⃣ بث جماعي ---
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
    """
    استقبال الملف وربطه بالزر الجديد في sections.json وfiles.json
    """
    if context.user_data.get("state") != "ADMIN_ADD_MENU_WAIT_FILE":
        return

    file = update.message.document or update.message.audio or update.message.video
    if not file:
        await update.message.reply_text("❗ لم يتم استلام ملف صالح")
        return

    menu_name = context.user_data["flow_data"]["menu_name"]
    _add_button_with_file(menu_name, file)

    await update.message.reply_text(f"✅ تم إنشاء زر وربطه بالملف: {file.file_name}")
    _clear_flow(context)


# ======================
# 🔧 وظائف مساعدة (داخلية)
# ======================
def _add_menu_only(menu_name: str):
    """
    إضافة قائمة بدون ملف
    """
    sections = load_json(SECTIONS_FILE) or {}
    sections.setdefault("root", {"sub": {}, "buttons": {}})

    sections["root"]["sub"][menu_name] = {
        "sub": {},
        "buttons": {}
    }

    save_json(SECTIONS_FILE, sections)


def _add_button_with_file(menu_name: str, file):
    """
    إضافة زر مرتبط بملف وحفظه في files.json
    """
    sections = load_json(SECTIONS_FILE) or {}
    sections.setdefault("root", {"sub": {}, "buttons": {}})

    # حفظ الملف في files.json
    file_uuid = str(uuid.uuid4())
    files_data = load_json(FILES_FILE) or {"files": []}
    files_data["files"].append({
        "id": file_uuid,
        "telegram_file_id": file.file_id,
        "name": file.file_name
    })
    save_json(FILES_FILE, files_data)

    # إضافة الزر في sections.json
    sections["root"]["buttons"][menu_name] = {
        "file": {"file_id": file.file_id, "file_name": file.file_name}
    }
    save_json(SECTIONS_FILE, sections)


def _clear_flow(context):
    """
    إنهاء flow الأدمن الحالي دون مسح path أو بيانات مستخدم أخرى
    """
    context.user_data.pop("state", None)
    context.user_data.pop("flow", None)
    context.user_data.pop("flow_data", None)


# ======================
# 🟢 زر المستخدم يرسل ملف (مباشر من sections.json)
# ======================
async def handle_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    إرسال الملفات مباشرة حسب زر المستخدم في sections.json
    """
    text = update.message.text.strip()
    sections = load_json(SECTIONS_FILE) or {}
    root = sections.get("root", {}).get("sub", {})
    buttons = sections.get("root", {}).get("buttons", {})

    # تحقق من الأزرار المباشرة
    if text in buttons and buttons[text].get("file"):
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=buttons[text]["file"]["file_id"],
            caption=buttons[text]["file"]["file_name"]
        )
        return

    # تحقق في القوائم الفرعية
    for menu_name, menu_data in root.items():
        if text in menu_data.get("buttons", {}) and menu_data["buttons"][text].get("file"):
            file_info = menu_data["buttons"][text]
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file"]["file_id"],
                caption=file_info["file"]["file_name"]
            )
            return
