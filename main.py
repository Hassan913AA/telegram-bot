from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard

SECTIONS_FILE = "storage/sections.json"


# ================= أدوات الشجرة =================
def get_section_by_path(data: dict, path: list) -> dict:
    """
    إرجاع العقدة الحالية من الشجرة حسب path
    آمن 100% ولا يرمي Exceptions
    """
    current = data or {}
    for p in path:
        node = current.get(p)
        if not isinstance(node, dict):
            return {}
        current = node.get("sub", {})
        if not isinstance(current, dict):
            return {}
    return current


# ================= عرض القائمة الحالية =================
async def show_current_menu(update, context):
    try:
        user_id = update.effective_user.id
        is_admin = user_id == context.bot_data.get("ADMIN")

        data = load_json(SECTIONS_FILE) or {}
        path = list(context.user_data.get("path", []))

        section = get_section_by_path(data, path)
        buttons = []

        # عناصر الشجرة
        for name in section.keys():
            buttons.append([KeyboardButton(name)])

        # 🔙 رجوع خطوة واحدة
        if path:
            buttons.append([KeyboardButton("🔙 رجوع")])

        # 🔙 رجوع للأدمن
        if is_admin:
            buttons.append([KeyboardButton("🔙 رجوع للأدمن")])

        # 🏠 الرئيسية
        buttons.append([KeyboardButton("🏠 القائمة الرئيسية")])

        if not buttons:
            buttons = [[KeyboardButton("🏠 القائمة الرئيسية")]]

        return await update.message.reply_text(
            "📂 اختر:",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        )

    except Exception as e:
        logger.error(f"show_current_menu crash: {e}", exc_info=True)
        return await update.message.reply_text("❌ خطأ في عرض القائمة.")


# ================= المعالج الرئيسي للقوائم =================
async def handle_menu(update, context):
    # احترام Router: لا نتدخل أثناء أي Flow إداري أو بث
    if context.user_data.get("state"):
        return

    try:
        user_id = update.effective_user.id
        is_admin = user_id == context.bot_data.get("ADMIN")
        text = update.message.text.strip()

        data = load_json(SECTIONS_FILE) or {}
        path = list(context.user_data.get("path", []))

        # 🏠 القائمة الرئيسية
        if text == "🏠 القائمة الرئيسية":
            context.user_data["path"] = []
            return await update.message.reply_text(
                "🏠 القائمة الرئيسية:",
                reply_markup=main_menu_keyboard(is_admin=is_admin)
            )

        # 🔙 رجوع خطوة
        if text == "🔙 رجوع":
            if path:
                path.pop()
                context.user_data["path"] = path
            return await show_current_menu(update, context)

        # 🔙 رجوع للأدمن
        if text == "🔙 رجوع للأدمن" and is_admin:
            context.user_data["path"] = []
            return await update.message.reply_text(
                "🛠 لوحة الأدمن:",
                reply_markup=admin_panel_keyboard()
            )

        # 📂 دخول القوائم
        if text == "📂 القوائم":
            context.user_data["path"] = []
            return await show_current_menu(update, context)

        section = get_section_by_path(data, path)

        # عنصر داخل الشجرة
        if text in section:
            item = section.get(text, {})

            # قائمة فرعية
            if isinstance(item.get("sub"), dict):
                path.append(text)
                context.user_data["path"] = path
                return await show_current_menu(update, context)

            # زر ملف
            file_data = item.get("file")
            if isinstance(file_data, dict) and file_data.get("file_id"):
                try:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=file_data["file_id"],
                        caption=file_data.get("file_name", "📄 ملف")
                    )
                except Exception as e:
                    logger.error(f"File send error: {e}", exc_info=True)
                    return await update.message.reply_text("❌ فشل إرسال الملف.")
                return

        # 🛠 دخول لوحة الأدمن من الرئيسية
        if is_admin and text == "🛠 لوحة الأدمن":
            return await update.message.reply_text(
                "🛠 لوحة تحكم الأدمن:",
                reply_markup=admin_panel_keyboard()
            )

        # إدخال غير مفهوم → نعيد نفس القائمة الحالية
        return await show_current_menu(update, context)

    except Exception as e:
        logger.error(f"handle_menu crash: {e}", exc_info=True)
        return await update.message.reply_text("❌ حصل خطأ داخلي.")
