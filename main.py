from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import get_token, get_admin_id, logger

from handlers.start import start
from handlers.menu_handler import show_current_menu
from handlers.broadcast import (
    broadcast_command,
    handle_broadcast_photo,
    handle_broadcast_audio,
    handle_broadcast_text
)
from handlers.admin_panel import open_admin_panel
from handlers.admin_add_menu import handle_admin_text, handle_admin_file

from services.menu_engine import get_tree, get_node_by_path
from services.user_service import load_users


# =========================
# 🧠 Router مركزي مضبوط
# =========================
async def route_text(update, context):
    state = context.user_data.get("state")
    text = update.message.text.strip()

    try:
        # 📢 بث جماعي
        if state == "BROADCAST_TEXT":
            await handle_broadcast_text(update, context)
            return

        # 🛠 حالات الأدمن (تحديد صريح)
        if state in {
            "ADMIN_PANEL",
            "ADMIN_ADD_MENU_WAIT_NAME",
            "ADMIN_ADD_MENU_WAIT_FILE",
            "ADMIN_ADD_MENU_WAIT_TYPE",
        }:
            await handle_admin_text(update, context)
            return

        # 👤 مستخدم عادي
        await handle_user_menu(update, context)

    except Exception as e:
        logger.error(f"[route_text] error={e}", exc_info=True)
        await update.message.reply_text("⚠️ حصل خطأ غير متوقع")


# =========================
# 👤 منطق المستخدم
# =========================
async def handle_user_menu(update, context):
    text = update.message.text.strip()
    tree = get_tree()
    path = context.user_data.get("path", [])

    node = get_node_by_path(tree, path)
    if not node:
        return

    item = node["children"].get(text)
    if not item:
        # إدخال غير مفهوم → نعيد عرض القائمة الحالية
        await show_current_menu(update, context)
        return

    # 📂 دخول قائمة
    if item["type"] == "menu":
        context.user_data.setdefault("path", []).append(text)
        await show_current_menu(update, context)
        return

    # 📎 زر ملف
    if item["type"] == "file":
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=item["file_id"],
            caption=item.get("file_name", "📄 ملف")
        )
        return


def main():
    TOKEN = get_token()
    ADMIN = get_admin_id()

    app = ApplicationBuilder().token(TOKEN).build()

    app.bot_data["ADMIN"] = ADMIN
    app.bot_data["USERS"] = load_users()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", open_admin_panel))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # 📎 ملفات الأدمن (مقيدة بالحالة)
    app.add_handler(
        MessageHandler(
            filters.Document.ALL | filters.VIDEO | filters.AUDIO,
            lambda update, context: (
                handle_admin_file(update, context)
                if context.user_data.get("state") == "ADMIN_ADD_MENU_WAIT_FILE"
                else None
            )
        )
    )

    # بث
    app.add_handler(MessageHandler(filters.PHOTO, handle_broadcast_photo))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_broadcast_audio))

    # Router النصوص
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))

    logger.info("Bot started successfully")
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
