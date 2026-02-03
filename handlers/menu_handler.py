from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import logger
from services.storage_service import load_json
from utils.keyboard import main_menu_keyboard, admin_panel_keyboard

SECTIONS_FILE = "storage/sections.json"


# ================= أدوات الشجرة =================
def get_section_by_path(data, path):
    current = data
    for p in path:
        current = current.get(p, {}).get("sub", {})
    return current


async def show_current_menu(update, context, data, path, is_admin):
    section = get_section_by_path(data, path)
    buttons = []

    # عرض عناصر الشجرة
    for name in section.keys():
        buttons.append([KeyboardButton(name)])

    # 🔙 رجوع خطوة واحدة (للجميع)
    if path:
        buttons.append([KeyboardButton("🔙 رجوع")])

    # 🔙 رجوع للأدمن فقط
    if is_admin:
        buttons.append([KeyboardButton("🔙 رجوع للأدمن")])

    # 🏠 رجوع للرئيسية
    buttons.append([KeyboardButton("🏠 القائمة الرئيسية")])

    return await update.message.reply_text(
        "📂 اختر:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


# ================= المعالج الرئيسي =================
async def handle_menu(update, context):
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text.strip()

    # 🧠 احترام الـ Router: لا نتدخل لو هناك حالة فعالة
    # 🧩 إضافة هندسية: لا نكسر أي Flow إداري أو بث أو إضافة
    if context.user_data.get("state"):
        return

    try:
        data = load_json(SECTIONS_FILE) or {}
        path = list(context.user_data.get("path", []))  # نسخة آمنة

        # 🏠 رجوع للرئيسية
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
            return await show_current_menu(update, context, data, path, is_admin)

        # 🔙 رجوع للأدمن
        if text == "🔙 رجوع للأدمن" and is_admin:
            context.user_data["path"] = []
            return await update.message.reply_text(
                "🛠 لوحة الأدمن:",
                reply_markup=admin_panel_keyboard()
            )

        # 📂 دخول من القائمة الرئيسية إلى الشجرة
        if text == "📂 القوائم":
            context.user_data["path"] = []
            return await show_current_menu(update, context, data, [], is_admin)

        section = get_section_by_path(data, path)

        # 📂 دخول عنصر من الشجرة
        if text in section:
            item = section[text]

            # قائمة فرعية
            if item.get("sub"):
                path.append(text)
                context.user_data["path"] = path
                return await show_current_menu(update, context, data, path, is_admin)

            # زر يرسل ملف
            if item.get("file"):
                try:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=item["file"]["file_id"],
                        caption=item["file"].get("file_name", "📄 ملف")
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

        # ❗ إدخال غير مفهوم → نعيد نفس القائمة الحالية
        # 🧩 إضافة هندسية: لا نرمي المستخدم للرئيسية بلا سبب
        return await show_current_menu(update, context, data, path, is_admin)

    except Exception as e:
        logger.error(f"handle_menu crash: {e}", exc_info=True)
        return await update.message.reply_text("❌ حصل خطأ داخلي.")
