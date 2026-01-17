import os
import logging

# إعداد نظام التسجيل (Logging)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("BOT")

# ===== قراءة المتغيرات البيئية =====

def get_token():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("❌ TELEGRAM_BOT_TOKEN غير موجود في Environment Variables")
    return token


def get_admin_id():
    admin = os.environ.get("ADMIN_ID")
    if not admin:
        raise RuntimeError("❌ ADMIN_ID غير موجود في Environment Variables")
    try:
        return int(admin)
    except ValueError:
        raise RuntimeError("❌ ADMIN_ID يجب أن يكون رقمًا صحيحًا")


# ===== ثوابت حالات البث =====
WAITING_TEXT = "waiting_text"
WAITING_PHOTO = "waiting_photo"
WAITING_AUDIO = "waiting_audio"
