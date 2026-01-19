# handlers/menu_handler.py

from telegram import ReplyKeyboardMarkup
from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard
from handlers.broadcast import broadcast_command

SECTIONS_FILE = "storage/sections.json"


async def handle_menu(update, context):
    """
    التحكم بالقوائم والديناميكيات:
    - عرض القوائم والملفات للمستخدمين
    - دعم لوحة تحكم الأدمن
    - دعم البث الجماعي
    """
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text.strip()

    try:
        data = load_json(SECTIONS_FILE) or {}

        # =========================
        # لوحة تحكم الأدمن
        # =========================
        if is_admin and text == "🛠 لوحة التحكم":
            return await update.message.reply_text(
                "🛠 لوحة تحكم الأدمن:",
                reply_markup=admin_panel_keyboard()
            )

        # =========================
        # الرجوع للقائمة الرئيسية
        # =========================
        if text == "🔙 رجوع للقائمة الرئيسية":
            return await update.message.reply_text(
                "🏠 القائمة الرئيسية:",
                reply_markup=main_menu_keyboard(is_admin=is_admin)
            )

        # =========================
        # التعامل مع القوائم الديناميكية
        # =========================
        if text in data:
            section = data[text]

            # حالة القوائم الفرعية
            if section.get("sub_buttons"):
                buttons = [[name] for name in section["sub_buttons"].keys()]
                return await update.message.reply_text(
                    f"📂 {text}",
                    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                )

            # حالة إرسال ملف
            if section.get("file"):
                file_info = section["file"]
                try:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=file_info["file_id"],
                        caption=file_info.get("file_name", "📄 ملف")
                    )
                except Exception as e:
                    logger.error(f"File send error: {e}")
                    return await update.message.reply_text("❌ فشل إرسال الملف.")
                return

        # =========================
        # أوامر الأدمن أثناء استخدام القوائم
        # =========================
        if is_admin:
            # إضافة زر/قائمة جديدة
            if text == "➕ إضافة زر/قائمة":
                context.user_data["state"] = "ADDING_BUTTON"
                return await update.message.reply_text("📌 أرسل اسم الزر/القائمة الجديدة:")

            # رفع ملف وربطه بزر
            if text == "📂 رفع ملف وربطه بزر":
                context.user_data["state"] = "UPLOADING_FILE"
                return await update.message.reply_text("📎 أرسل اسم الزر ثم الملف:")

            # تعديل زر/قائمة
            if text == "✏️ تعديل زر/قائمة":
                context.user_data["state"] = "EDITING_BUTTON"
                return await update.message.reply_text("✏️ أرسل اسم الزر/القائمة للتعديل:")

            # حذف زر/قائمة
            if text == "🗑 حذف زر/قائمة":
                context.user_data["state"] = "DELETING_BUTTON"
                return await update.message.reply_text("🗑 أرسل اسم الزر/القائمة للحذف:")

            # بث رسالة جماعية
            if text == "📢 إرسال رسالة جماعية":
                context.user_data["state"] = "BROADCAST"
                return await update.message.reply_text("📢 أرسل نص أو صورة أو صوت للبث:")

        # =========================
        # أي أمر غير معروف
        # =========================
        return await update.message.reply_text(
            "⚠️ اختر من القائمة فقط.",
            reply_markup=main_menu_keyboard(is_admin=is_admin)
        )

    except Exception as e:
        logger.error(f"handle_menu crash: {e}")
        return await update.message.reply_text("❌ حصل خطأ داخلي.")
