from telegram import ReplyKeyboardMarkup, KeyboardButton
from services.user_service import load_users, save_users
from config import get_admin_id, logger

USERS = load_users()
ADMIN_ID = get_admin_id()


def admin_start_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("▶️ تشغيل البوت")],
            [KeyboardButton("🛠 لوحة التحكم")]
        ],
        resize_keyboard=True
    )


async def start(update, context):
    user = update.effective_user
    uid = user.id

    # حفظ المستخدم
    if uid not in USERS:
        USERS.add(uid)
        save_users(USERS)
        logger.info(f"New user added: {uid}")

    # إذا كان أدمن
    if uid == ADMIN_ID:
        await update.message.reply_text(
            "👑 أهلاً أيها الأدمن!\nاختر ماذا تريد:",
            reply_markup=admin_start_keyboard()
        )
        return

    # مستخدم عادي
    await update.message.reply_text(
        "👋 مرحباً بك!\nلا توجد قوائم بعد… سيتم إضافتها قريبًا 📂",
        reply_markup=None
    )
