# handlers/menu_handler.py

from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard

SECTIONS_FILE = "storage/sections.json"


async def handle_menu(update, context):
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text

    try:
        data = load_json(SECTIONS_FILE) or {}

        # =========================
        # زر لوحة التحكم (للأدمن)
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

            # إذا كان هذا القسم يحتوي أزرار فرعية
            if section.get("type") == "menu":
                buttons = []
                for name in section.get("items", {}).keys():
                    buttons.append([name])

                from telegram import ReplyKeyboardMarkup
                return await update.message.reply_text(
                    f"📂 {text}",
                    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                )

            # إذا كان هذا القسم يرسل ملف
            if section.get("type") == "file":
                file_path = section.get("path")
                caption = section.get("caption", "📄 ملف")

                try:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=open(file_path, "rb"),
                        caption=caption
                    )
                except Exception as e:
                    logger.error(f"File send error: {e}")
                    return await update.message.reply_text("❌ فشل إرسال الملف.")

        # =========================
        # أوامر لوحة تحكم الأدمن
        # =========================
        if is_admin:
            if text == "➕ إضافة زر جديد":
                context.user_data["admin_mode"] = "add_button"
                return await update.message.reply_text("✍️ أرسل اسم الزر الجديد:")

            if text == "📂 رفع ملف وربطه بزر":
                context.user_data["admin_mode"] = "upload_file"
                return await update.message.reply_text("📎 أرسل الملف الآن:")

            if text == "📢 بث رسالة":
                from handlers.broadcast import broadcast_command
                return await broadcast_command(update, context)

        # =========================
        # أي شيء غير معروف
        # =========================
        return await update.message.reply_text(
            "⚠️ اختر من القائمة فقط.",
            reply_markup=main_menu_keyboard(is_admin=is_admin)
        )

    except Exception as e:
        logger.error(f"handle_menu crash: {e}")
        return await update.message.reply_text("❌ حصل خطأ داخلي.")
# handlers/menu_handler.py

from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard

SECTIONS_FILE = "storage/sections.json"


async def handle_menu(update, context):
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text

    try:
        data = load_json(SECTIONS_FILE) or {}

        # =========================
        # زر لوحة التحكم (للأدمن)
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

            # إذا كان هذا القسم يحتوي أزرار فرعية
            if section.get("type") == "menu":
                buttons = []
                for name in section.get("items", {}).keys():
                    buttons.append([name])

                from telegram import ReplyKeyboardMarkup
                return await update.message.reply_text(
                    f"📂 {text}",
                    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                )

            # إذا كان هذا القسم يرسل ملف
            if section.get("type") == "file":
                file_path = section.get("path")
                caption = section.get("caption", "📄 ملف")

                try:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=open(file_path, "rb"),
                        caption=caption
                    )
                except Exception as e:
                    logger.error(f"File send error: {e}")
                    return await update.message.reply_text("❌ فشل إرسال الملف.")

        # =========================
        # أوامر لوحة تحكم الأدمن
        # =========================
        if is_admin:
            if text == "➕ إضافة زر جديد":
                context.user_data["admin_mode"] = "add_button"
                return await update.message.reply_text("✍️ أرسل اسم الزر الجديد:")

            if text == "📂 رفع ملف وربطه بزر":
                context.user_data["admin_mode"] = "upload_file"
                return await update.message.reply_text("📎 أرسل الملف الآن:")

            if text == "📢 بث رسالة":
                from handlers.broadcast import broadcast_command
                return await broadcast_command(update, context)

        # =========================
        # أي شيء غير معروف
        # =========================
        return await update.message.reply_text(
            "⚠️ اختر من القائمة فقط.",
            reply_markup=main_menu_keyboard(is_admin=is_admin)
        )

    except Exception as e:
        logger.error(f"handle_menu crash: {e}")
        return await update.message.reply_text("❌ حصل خطأ داخلي.")
