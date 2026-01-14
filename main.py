from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import get_token, get_admin_id
from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_photo,
    handle_audio,
    handle_text_broadcast
)

from services.user_service import load_users


def main():
    TOKEN = get_token()
    ADMIN = get_admin_id()

    print("Token loaded:", TOKEN[:5], "...")

    app = Application.builder().token(TOKEN).build()

    app.bot_data["ADMIN"] = ADMIN
    app.bot_data["USERS"] = load_users()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # Broadcast Handlers
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_broadcast))

    # Menu
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
