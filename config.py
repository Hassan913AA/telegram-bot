import os
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_token():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("⚠️ TELEGRAM_BOT_TOKEN غير موجود في المتغيرات البيئية!")
    return token

def get_admin_id():
    admin = os.environ.get("ADMIN_ID")
    if not admin:
        raise ValueError("⚠️ ADMIN_ID غير موجود!")
    return int(admin)

WAITING_TEXT = "waiting_text"
WAITING_PHOTO = "waiting_photo"
WAITING_AUDIO = "waiting_audio"
