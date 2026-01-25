# admin_panel.py
import os
import shutil
from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboard import (
    main_menu_keyboard,
    admin_panel_keyboard,
    add_menu_keyboard,
    broadcast_keyboard,
)
from services.storage_service import load_json, save_json

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
SECTIONS_FILE = "storage/sections.json"
BACKUP_FILE = "storage/sections_backup.json"

def backup_sections():
    if os.path.exists(SECTIONS_FILE):
        shutil.copy(SECTIONS_FILE, BACKUP_FILE)

def get_node(data, path):
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node

def is_admin(user_id):
    return user_id == ADMIN_ID

async def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ لا تملك صلاحية الأدمن.")
        return
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=admin_panel_keyboard())

async def admin_add_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["state"] = "ADD_MENU"
    await update.message.reply_text("➕ إضافة زر / قائمة", reply_markup=add_menu_keyboard())

async def create_new_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "WAIT_PARENT_PATH"
    await update.message.reply_text("📁 أين توضع القائمة؟ اكتب المسار أو /root")

async def receive_parent_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "/root":
        context.user_data["path"] = []
    else:
        context.user_data["path"] = text.split("/")
    context.user_data["state"] = "WAIT_NEW_LIST_NAME"
    await update.message.reply_text("✏️ اكتب اسم القائمة الجديدة")

async def receive_new_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    data = load_json(SECTIONS_FILE) or {}
    node = get_node(data, context.user_data["path"])
    if name in node:
        await update.message.reply_text("⚠️ الاسم موجود مسبقًا، اختر اسمًا آخر")
        return
    backup_sections()
    node[name] = {
        "file": None,
        "sub": {
            "🔙 رجوع": {"file": None, "sub": {}},
            "🏠 رجوع للقائمة الرئيسية": {"file": None, "sub": {}},
        },
    }
    save_json(SECTIONS_FILE, data)
    context.user_data.clear()
    await update.message.reply_text(f"✅ تم إنشاء القائمة: {name}", reply_markup=admin_panel_keyboard())

async def broadcast_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["state"] = "BROADCAST"
    await update.message.reply_text("📢 إرسال رسالة جماعية", reply_markup=broadcast_keyboard())

async def broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "WAIT_BROADCAST_TEXT"
    await update.message.reply_text("✉️ أرسل نص الرسالة")

async def receive_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    users = load_json("storage/users.json") or []
    for uid in users:
        try:
            await context.bot.send_message(int(uid), text)
        except:
            pass
    context.user_data.clear()
    await update.message.reply_text("✅ تم الإرسال للجميع", reply_markup=admin_panel_keyboard())

async def undo_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(BACKUP_FILE):
        shutil.copy(BACKUP_FILE, SECTIONS_FILE)
        await update.message.reply_text("↩️ تم التراجع عن آخر تعديل", reply_markup=admin_panel_keyboard())
    else:
        await update.message.reply_text("❌ لا يوجد نسخة احتياطية", reply_markup=admin_panel_keyboard())

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user_is_admin = is_admin(update.effective_user.id)
    await update.message.reply_text("🏠 رجوع للقائمة الرئيسية", reply_markup=main_menu_keyboard(is_admin=user_is_admin))
