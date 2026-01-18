from menus import MAIN_MENU
from services.user_service import load_users, save_users
from config import logger

# تحميل المستخدمين الحاليين عند التشغيل
USERS = load_users()

async def start(update, context):
    uid = update.effective_user.id

    # إضافة المستخدم الجديد إذا لم يكن موجوداً
    if uid not in USERS:
        USERS.add(uid)
        save_users(USERS)
        logger.info(f"New user added: {uid}")

    await update.message.reply_text(
        "Welcome 👋 اختر خياراً:",
        reply_markup=MAIN_MENU
    )
