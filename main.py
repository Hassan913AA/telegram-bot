from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from config import get_token, get_admin_id, logger

# handlers
from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_broadcast_photo,
    handle_broadcast_audio,
    handle_broadcast_text,
)
from handlers.admin_panel import open_admin_panel
from handlers.admin_add_menu import handle_admin_text, handle_admin_file

# services
from services.user_service import load_users


# =========================
# 🧠 Router مركزي واحد فقط
# =========================
async def route_text(update, context):
    state = context.user_data.get("state")

    try:
        # 📢 بث جماعي (نص)
        if state == "BROADCAST_TEXT":
            await handle_broadcast_text(update, context)
            return

        # 🛠 أي Flow إداري
        if state and state.startswith("ADMIN_"):
            await handle_admin_text(update, context)
            return

        # 👤 مستخدم عادي (القوائم)
        await handle_menu(update, context)

    except Exception as e:
        logger.error(f"[route_text] crash: {e}", exc_info=True)
        await update.message.reply_text("⚠️ حصل خطأ غير متوقع")


def main():
    TOKEN = get_token()
    ADMIN = get_admin_id()

    app = ApplicationBuilder().token(TOKEN).build()

    # بيانات عامة
    app.bot_data["ADMIN"] = ADMIN
    app.bot_data["USERS"] = load_users()

    # =================
    # أوامر
    # =================
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", open_admin_panel))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # =================
    # ملفات يرسلها الأدمن (ضمن Flow فقط)
    # =================
    app.add_handler(
        MessageHandler(
            filters.Document.ALL | filters.VIDEO | filters.AUDIO,
            handle_admin_file
        )
    )

    # =================
    # بث وسائط
    # =================
    app.add_handler(MessageHandler(filters.PHOTO, handle_broadcast_photo))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_broadcast_audio))

    # =================
    # Router النصوص الوحيد
    # =================
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, route_text)
    )

    logger.info("Bot started successfully")
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
