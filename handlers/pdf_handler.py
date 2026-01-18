from services.file_service import safe_send_pdf

UPLOAD_PATH = "data/uploads"

async def send_grammar(update, context):
    waiting = await update.message.reply_text("⏳ تجهيز Grammar…")
    ok = await safe_send_pdf(
        context.bot,
        update.effective_chat.id,
        f"{UPLOAD_PATH}/grammar.pdf",
        "📘 Grammar PDF"
    )
    await waiting.edit_text("📘 تم الإرسال" if ok else "❌ الملف غير موجود")


async def send_vocab(update, context):
    waiting = await update.message.reply_text("⏳ تجهيز Vocabulary…")
    ok = await safe_send_pdf(
        context.bot,
        update.effective_chat.id,
        f"{UPLOAD_PATH}/vocabulary.pdf",
        "📗 Vocabulary PDF"
    )
    await waiting.edit_text("📗 تم الإرسال" if ok else "❌ الملف غير موجود")


async def send_reading(update, context):
    waiting = await update.message.reply_text("⏳ تجهيز Reading…")
    ok = await safe_send_pdf(
        context.bot,
        update.effective_chat.id,
        f"{UPLOAD_PATH}/reading.pdf",
        "📕 Reading PDF"
    )
    await waiting.edit_text("📕 تم الإرسال" if ok else "❌ الملف غير موجود")
