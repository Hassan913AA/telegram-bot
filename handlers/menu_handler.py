from utils.keyboard import (
    get_main_menu,
    get_admin_menu,
    get_section_keyboard,
)
from services.storage_service import load_sections
from services.file_service import send_file_by_key
from utils.logger import get_logger

logger = get_logger(__name__)


async def handle_menu(update, context):
    text = update.message.text
    user_id = update.effective_user.id
    admin_id = context.bot_data.get("ADMIN")

    sections = load_sections()

    # === الرجوع للقائمة الرئيسية ===
    if text in ["🏠 Main Menu", "🔙 Back"]:
        if user_id == admin_id:
            return await update.message.reply_text(
                "🏠 القائمة الرئيسية (Admin)",
                reply_markup=get_admin_menu()
            )
        else:
            return await update.message.reply_text(
                "🏠 القائمة الرئيسية",
                reply_markup=get_main_menu()
            )

    # === فتح قسم ===
    if text in sections:
        return await update.message.reply_text(
            f"📂 اختر من قسم: {text}",
            reply_markup=get_section_keyboard(text)
        )

    # === الضغط على زر ملف ===
    for section_name, buttons in sections.items():
        for btn in buttons:
            if btn["title"] == text:
                return await send_file_by_key(update, context, btn["file_key"])

    # === أي شيء غير معروف ===
    await update.message.reply_text("❓ لم أفهم الأمر، عد للقائمة الرئيسية 🔙")
