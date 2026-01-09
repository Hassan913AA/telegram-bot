from menus import BOOKS_MENU, SUB_MENU, MAIN_MENU
from .pdf_handler import send_grammar, send_vocab, send_reading

async def handle_menu(update, context):
    text = update.message.text

    if text == "📘 Grammar PDF":
        return await send_grammar(update, context)

    if text == "📗 Vocabulary PDF":
        return await send_vocab(update, context)

    if text == "📕 Reading PDF":
        return await send_reading(update, context)

    if text in ["🎓 بكالوريا علمي", "📚 بكالوريا أدبي"]:
        return await update.message.reply_text("📚 اختر الكتاب:", reply_markup=BOOKS_MENU)

    if text == "ℹ️ Info":
        return await update.message.reply_text("بوت تعليمي", reply_markup=SUB_MENU)

    if text in ["🔙 Back", "🏠 Main Menu"]:
        return await update.message.reply_text("Main menu", reply_markup=MAIN_MENU)
