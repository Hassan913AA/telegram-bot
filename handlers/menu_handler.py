# handlers/menu_handler.py

from config import logger
from utils.keyboard import (
    get_main_menu,
    get_books_menu,
    get_admin_broadcast_menu,
    get_admin_menu
)

async def handle_menu(update, context):
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")
    text = update.message.text

    # قائمة الكتب
    if text in ["📘 Grammar PDF", "📗 Vocabulary PDF", "📕 Reading PDF"]:
        from .pdf_handler import send_grammar, send_vocab, send_reading
        if text == "📘 Grammar PDF":
            return await send_grammar(update, context)
        if text == "📗 Vocabulary PDF":
            return await send_vocab(update, context)
        if text == "📕 Reading PDF":
            return await send_reading(update, context)

    # العودة للقائمة الرئيسية
    if text in ["🔙 Back", "🏠 Main Menu", "🔙 رجوع"]:
        # إذا كان أدمن → لوحة الإدارة، وإلا القائمة العادية
        menu = get_admin_menu() if is_admin else get_main_menu(is_admin=False)
        return await update.message.reply_text("القائمة الرئيسية:", reply_markup=menu)

    # قسم المعلومات
    if text == "ℹ️ معلومات":
        return await update.message.reply_text("🤖 بوت تعليمي يعمل على تنظيم الكتب والبث", 
                                               reply_markup=get_main_menu(is_admin))

    # قسم تصفح الكتب
    if text == "📚 تصفح الكتب":
        return await update.message.reply_text("اختر الكتاب:", reply_markup=get_books_menu())

    # قسم البحث (يمكن إضافة وظيفة البحث لاحقًا)
    if text == "🔍 بحث":
        return await update.message.reply_text("🔍 اكتب كلمة للبحث في الكتب (ميزة قيد التطوير).")

    # لوحة البث للإدمن
    if is_admin and text == "📢 بث رسالة":
        from .broadcast import broadcast_command
        return await broadcast_command(update, context)

    # رفع كتاب (يمكن ربطه لاحقًا مع file_service)
    if is_admin and text == "📤 رفع كتاب":
        return await update.message.reply_text("📤 أرسل الملف الآن ليتم رفعه وربطه بالأزرار.")

    # إدارة البوت (لوحة الإدمن)
    if is_admin and text == "🛠 إدارة البوت":
        return await update.message.reply_text("🛠 لوحة إدارة البوت:", reply_markup=get_admin_menu())

    # أي نص آخر
    return await update.message.reply_text("⚠️ لم أفهم هذا الأمر، الرجاء اختيار خيار من القائمة.",
                                           reply_markup=get_main_menu(is_admin))
