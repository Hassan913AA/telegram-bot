from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger
import shutil, os

SECTIONS_FILE = "storage/sections.json"
BACKUP_FILE = "storage/sections_backup.json"

def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node

def backup_sections():
    if os.path.exists(SECTIONS_FILE):
        shutil.copy(SECTIONS_FILE, BACKUP_FILE)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("↩️ التراجع عن آخر تعديل")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

# ====================== إضافة زر / قائمة ======================
async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")

async def handle_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_json(SECTIONS_FILE) or {}
    path = context.user_data.get("path", [])
    node = get_node(data, path)
    new_name = update.message.text.strip()

    node[new_name] = {
        "file": None,
        "sub": {
            "🔙 رجوع": {"file": None, "sub": {}},
            "🏠 الرئيسية": {"file": None, "sub": {}}
        }
    }

    save_json(SECTIONS_FILE, data)
    context.user_data.clear()
    await update.message.reply_text(f"✅ تم إنشاء: {new_name} في {'/'.join(path) if path else 'الرئيسية'}")

# ====================== ربط ملف ======================
async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")

async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}
    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)
    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")

# ====================== التراجع عن آخر تعديل ======================
async def undo_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(BACKUP_FILE):
        shutil.copy(BACKUP_FILE, SECTIONS_FILE)
        await update.message.reply_text("↩️ تم التراجع عن آخر تعديل")
    else:
        await update.message.reply_text("❌ لا يوجد تعديل سابق للتراجع عنه")

# ====================== العودة للقائمة الرئيسية ======================
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
