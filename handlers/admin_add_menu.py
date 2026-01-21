from services.storage_service import load_json, save_json
from telegram import ReplyKeyboardMarkup, KeyboardButton

SECTIONS_FILE = "storage/sections.json"


def get_section_by_path(data, path):
    current = data
    for p in path:
        current = current.setdefault(p, {}).setdefault("sub_buttons", {})
    return current


async def handle_add_menu(update, context):
    text = update.message.text.strip()
    data = load_json(SECTIONS_FILE) or {}

    # المرحلة 1: اختيار الموقع
    if context.user_data.get("admin_step") == "ask_menu_location":
        context.user_data["new_menu_path"] = text.split("/")
        context.user_data["admin_step"] = "ask_menu_name"
        return await update.message.reply_text("✍️ أرسل اسم القائمة الجديدة:")

    # المرحلة 2: اسم القائمة
    if context.user_data.get("admin_step") == "ask_menu_name":
        path = context.user_data.get("new_menu_path", [])
        section = get_section_by_path(data, path)

        section[text] = {
            "sub_buttons": {}
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()

        return await update.message.reply_text("✅ تم إنشاء القائمة بنجاح مع أزرار الرجوع تلقائيًا.")
