from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard

SECTIONS_FILE = "storage/sections.json"


def get_section_by_path(data, path):
    current = data
    for p in path:
        current = current.get(p, {}).get("sub_buttons", {})
    return current


async def show_current_menu(update, context, data, path, is_admin):
    section = get_section_by_path(data, path)
    buttons = []

    for name in section.keys():
        buttons.append([KeyboardButton(name)])

    # أزرار التنقل
    if path:
        buttons.append([KeyboardButton("🔙 رجوع")])
    buttons.append([KeyboardButton("🏠 القائمة الرئيسية")])

    return await update.message.reply_text(
        "📂 اختر:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


async def handle_menu(update, context):
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text.strip()

    try:
        data = load_json(SECTIONS_FILE) or {}
        path = context.user_data.get("path", [])

        # ===== رجوع =====
        if text == "🔙 رجوع":
            if path:
                path.pop()
                context.user_data["path"] = path
            return await show_current_menu(update, context, data, path, is_admin)

        # ===== رجوع للقائمة الرئيسية =====
        if text == "🏠 القائمة الرئيسية":
            context.user_data["path"] = []
            return await update.message.reply_text(
                "🏠 القائمة الرئيسية:",
                reply_markup=main_menu_keyboard(is_admin=is_admin)
            )

        # ===== دخول عنصر =====
        section = get_section_by_path(data, path)

        if text in section:
            item = section[text]

            # لو فيه قائمة فرعية
            if item.get("sub_buttons"):
                path.append(text)
                context.user_data["path"] = path
                return await show_current_menu(update, context, data, path, is_admin)

            # لو فيه ملف
            if item.get("file"):
                try:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=item["file"]["file_id"],
                        caption=item["file"].get("file_name", "📄 ملف")
                    )
                except Exception as e:
                    logger.error(f"File send error: {e}")
                    return await update.message.reply_text("❌ فشل إرسال الملف.")
                return

        # ===== أوامر الأدمن =====
        if is_admin:
            if text == "🛠 لوحة التحكم":
                from utils.keyboard import admin_panel_keyboard
                return await update.message.reply_text(
                    "🛠 لوحة تحكم الأدمن:",
                    reply_markup=admin_panel_keyboard()
                )

        return await update.message.reply_text(
            "⚠️ اختر من القائمة فقط.",
            reply_markup=main_menu_keyboard(is_admin=is_admin)
        )

    except Exception as e:
        logger.error(f"handle_menu crash: {e}")
        return await update.message.reply_text("❌ حصل خطأ داخلي.")
