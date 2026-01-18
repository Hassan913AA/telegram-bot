# bot/handlers/admin_panel.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard

SECTIONS_FILE = "storage/sections.json"

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    عرض لوحة تحكم الإدمن.
    """
    user_id = update.effective_user.id
    if user_id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ أنت لست الإدمن.")
        return

    sections = load_json(SECTIONS_FILE) or {}

    buttons = [
        [KeyboardButton("➕ إضافة زر جديد")],
        [KeyboardButton("✏️ تعديل زر")],
        [KeyboardButton("🗑 حذف زر")],
        [KeyboardButton("📂 رفع ملف جديد")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]

    await update.message.reply_text(
        "🛠 لوحة التحكم الخاصة بالإدمن",
        reply_markup=ReplyKeyboardMarkup(
            buttons, resize_keyboard=True, one_time_keyboard=False
        )
    )

async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هنا ستضع منطق إضافة زر جديد وربطه بقسم أو ملف
    await update.message.reply_text("📌 أرسل اسم الزر الجديد:")

async def edit_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # منطق تعديل زر موجود
    await update.message.reply_text("✏️ أرسل اسم الزر الذي تريد تعديله:")

async def delete_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # منطق حذف زر موجود
    await update.message.reply_text("🗑 أرسل اسم الزر الذي تريد حذفه:")

async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # منطق رفع ملف جديد وربطه بزر
    await update.message.reply_text("📂 أرسل الملف الذي تريد رفعه:")

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إرجاع الإدمن للقائمة الرئيسية
    await update.message.reply_text(
        "🏠 تم الرجوع للقائمة الرئيسية",
        reply_markup=main_menu_keyboard(is_admin=True)
    )
