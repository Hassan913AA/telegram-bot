from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import get_token, get_admin_id, WAITING_TEXT
from handlers.start import start
from handlers.menu_handler import handle_menu
from handlers.broadcast import (
    broadcast_command,
    handle_photo,
    handle_audio,
    handle_text_broadcast
)
from services.user_service import load_users


async def route_text(update, context):
    # إذا كان المستخدم في وضع بث نص
    if context.user_data.get(WAITING_TEXT):
        await handle_text_broadcast(update, context)
        return

    # غير ذلك → تعامل مع القوائم والأزرار
    await handle_menu(update, context)


def main():
    TOKEN = get_token()
    ADMIN = get_admin_id()

    print("Token loaded:", TOKEN[:5], "...")

    app = Application.builder().token(TOKEN).build()

    # بيانات عامة للبوت
    app.bot_data["ADMIN"] = ADMIN
    app.bot_data["USERS"] = load_users()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # وسائط البث
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

    # معالج النص الموحد
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
