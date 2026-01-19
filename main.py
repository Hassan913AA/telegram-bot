from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import get_token, get_admin_id, WAITING_TEXT, logger

from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_photo,
    handle_audio,
    handle_text_broadcast
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
    try:
        # وضع البث الجماعي
        if context.user_data.get(WAITING_TEXT):
            await handle_text_broadcast(update, context)
            return

        # حالات الإدمن
        if context.user_data.get("state"):
            await handle_admin_text(update, context)
            return

        # الوضع العادي
        await handle_menu(update, context)

    except Exception as e:
        logger.error(f"route_text error: {e}")


def main():
    try:
        TOKEN = get_token()
        ADMIN = get_admin_id()

        print("Token loaded:", TOKEN[:5], "...")

        app = Application.builder().token(TOKEN).build()

        app.bot_data["ADMIN"] = ADMIN
        app.bot_data["USERS"] = load_users()

        # Commands
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("broadcast", broadcast_command))
        app.add_handler(CommandHandler("admin", admin_panel))

        # Admin panel buttons (ReplyKeyboard)
        app.add_handler(MessageHandler(filters.Regex("^➕ إضافة زر جديد$"), add_button))
        app.add_handler(MessageHandler(filters.Regex("^📂 رفع ملف وربطه بزر$"), upload_file))
        app.add_handler(MessageHandler(filters.Regex("^🔙 رجوع للقائمة الرئيسية$"), back_to_main))

        # Media (admin upload file + broadcast)
        app.add_handler(MessageHandler(filters.Document.ALL, handle_admin_file))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

        # Text
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

        print("Bot running...")
        app.run_polling()

    except Exception as e:
        logger.critical(f"Main crash: {e}")


if __name__ == "__main__":
    main()
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import get_token, get_admin_id, WAITING_TEXT, logger

from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_photo,
    handle_audio,
    handle_text_broadcast
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
    try:
        # وضع البث الجماعي
        if context.user_data.get(WAITING_TEXT):
            await handle_text_broadcast(update, context)
            return

        # حالات الإدمن
        if context.user_data.get("state"):
            await handle_admin_text(update, context)
            return

        # الوضع العادي
        await handle_menu(update, context)

    except Exception as e:
        logger.error(f"route_text error: {e}")


def main():
    try:
        TOKEN = get_token()
        ADMIN = get_admin_id()

        print("Token loaded:", TOKEN[:5], "...")

        app = Application.builder().token(TOKEN).build()

        app.bot_data["ADMIN"] = ADMIN
        app.bot_data["USERS"] = load_users()

        # Commands
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("broadcast", broadcast_command))
        app.add_handler(CommandHandler("admin", admin_panel))

        # Admin panel buttons (ReplyKeyboard)
        app.add_handler(MessageHandler(filters.Regex("^➕ إضافة زر جديد$"), add_button))
        app.add_handler(MessageHandler(filters.Regex("^📂 رفع ملف وربطه بزر$"), upload_file))
        app.add_handler(MessageHandler(filters.Regex("^🔙 رجوع للقائمة الرئيسية$"), back_to_main))

        # Media (admin upload file + broadcast)
        app.add_handler(MessageHandler(filters.Document.ALL, handle_admin_file))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

        # Text
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

        print("Bot running...")
        app.run_polling()

    except Exception as e:
        logger.critical(f"Main crash: {e}")


if __name__ == "__main__":
    main()
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import get_token, get_admin_id, WAITING_TEXT, logger

from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_photo,
    handle_audio,
    handle_text_broadcast
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
    try:
        # وضع البث الجماعي
        if context.user_data.get(WAITING_TEXT):
            await handle_text_broadcast(update, context)
            return

        # حالات الإدمن
        if context.user_data.get("state"):
            await handle_admin_text(update, context)
            return

        # الوضع العادي
        await handle_menu(update, context)

    except Exception as e:
        logger.error(f"route_text error: {e}")


def main():
    try:
        TOKEN = get_token()
        ADMIN = get_admin_id()

        print("Token loaded:", TOKEN[:5], "...")

        app = Application.builder().token(TOKEN).build()

        app.bot_data["ADMIN"] = ADMIN
        app.bot_data["USERS"] = load_users()

        # Commands
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("broadcast", broadcast_command))
        app.add_handler(CommandHandler("admin", admin_panel))

        # Admin panel buttons (ReplyKeyboard)
        app.add_handler(MessageHandler(filters.Regex("^➕ إضافة زر جديد$"), add_button))
        app.add_handler(MessageHandler(filters.Regex("^📂 رفع ملف وربطه بزر$"), upload_file))
        app.add_handler(MessageHandler(filters.Regex("^🔙 رجوع للقائمة الرئيسية$"), back_to_main))

        # Media (admin upload file + broadcast)
        app.add_handler(MessageHandler(filters.Document.ALL, handle_admin_file))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

        # Text
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

        print("Bot running...")
        app.run_polling()

    except Exception as e:
        logger.critical(f"Main crash: {e}")


if __name__ == "__main__":
    main()
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import get_token, get_admin_id, WAITING_TEXT, logger

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
    try:
        # وضع البث الجماعي
        if context.user_data.get(WAITING_TEXT):
            await handle_text_broadcast(update, context)
            return

        # حالات الإدمن
        if context.user_data.get("state"):
            await handle_admin_text(update, context)
            return

        # الوضع العادي
        await handle_menu(update, context)

    except Exception as e:
        logger.error(f"route_text error: {e}")


def main():
    try:
        TOKEN = get_token()
        ADMIN = get_admin_id()

        print("Token loaded:", TOKEN[:5], "...")

        app = Application.builder().token(TOKEN).build()

        app.bot_data["ADMIN"] = ADMIN
        app.bot_data["USERS"] = load_users()

        # Commands
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("broadcast", broadcast_command))
        app.add_handler(CommandHandler("admin", admin_panel))

        # Admin panel buttons (ReplyKeyboard)
        app.add_handler(MessageHandler(filters.Regex("^➕ إضافة زر جديد$"), add_button))
        app.add_handler(MessageHandler(filters.Regex("^📂 رفع ملف وربطه بزر$"), upload_file))
        app.add_handler(MessageHandler(filters.Regex("^🔙 رجوع للقائمة الرئيسية$"), back_to_main))

        # Media (admin upload file + broadcast)
        app.add_handler(MessageHandler(filters.Document.ALL, handle_admin_file))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

        # Text
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

        print("Bot running...")
        app.run_polling()

    except Exception as e:
        logger.critical(f"Main crash: {e}")


if __name__ == "__main__":
    main()
