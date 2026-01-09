from menus import MAIN_MENU
from services.user_service import save_users
from config import logger

USERS = set()

async def start(update, context):
    uid = update.effective_user.id
    USERS.add(uid)
    save_users(USERS)
    logger.info(f"New user: {uid}")

    await update.message.reply_text(
        "Welcome 👋 اختر خياراً:",
        reply_markup=MAIN_MENU
    )
