from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import get_token, get_admin_id, logger

from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_broadcast_photo,
    handle_broadcast_audio,
    handle_broadcast_text
)
from handlers.admin_panel import (
    admin_panel,
    add_button,
    upload_file,
    back_to_main,
    handle_admin_text,
    handle_admin_file
)

from services.user_service import load_users


async def route_text(update, context):
    user_id = update.effective_user.id
    state = context.user_data.get("state")

    try:
        # ===== وضع البث الجماعي =====
        if state == "BROADCAST_TEXT":
            await handle_broadcast_text(update, context)
            return

        # ===== حالات الأدمن الأخرى =====
        if state and state.startswith("ADMIN_"):
            await handle_admin_text(update, context)
            return

        # ===== الوضع العادي (المستخدمين) =====
        await handle_menu(update, context)

    except Exception as e:
        logger.error(f"[route_text] user={user_id} state={state} error={e}", exc_info=True)
        await update.message.reply_text("⚠️ حصل خطأ غير متوقع، حاول مرة أخرى.")


def main():
    try:
        TOKEN = get_token()
        ADMIN = get_admin_id()

        app = Application.builder().token(TOKEN).build()

        # تخزين بيانات عامة للبوت
        app.bot_data["ADMIN"] = ADMIN
        app.bot_data["USERS"] = load_users()

        # ===== أوامر =====
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("admin", admin_panel))
        app.add_handler(CommandHandler("broadcast", broadcast_command))

        # ===== أزرار لوحة الأدمن =====
        app.add_handler(MessageHandler(filters.Regex("^➕ إضافة زر/قائمة$"), add_button))
        app.add_handler(MessageHandler(filters.Regex("^📂 رفع ملف وربطه بزر$"), upload_file))
        app.add_handler(MessageHandler(filters.Regex("^🔙 رجوع للقائمة الرئيسية$"), back_to_main))

        # ===== ملفات وصور وصوت =====
        app.add_handler(MessageHandler(filters.Document.ALL, handle_admin_file))
        app.add_handler(MessageHandler(filters.PHOTO, handle_broadcast_photo))
        app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_broadcast_audio))

        # ===== نصوص عامة =====
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

        logger.info("Bot started successfully")
        print("🤖 Bot is running...")

        app.run_polling()

    except Exception as e:
        logger.critical(f"[MAIN CRASH] {e}", exc_info=True)


if __name__ == "__main__":
    main()
