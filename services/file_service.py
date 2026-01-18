import os
from telegram.constants import ChatAction
from utils.logger import get_logger

logger = get_logger(__name__)

async def safe_send_file(bot, chat_id: int, file_path: str, caption: str = None) -> bool:
    """
    إرسال أي ملف (PDF / صورة / صوت / ... ) بأمان مع معالجة الأخطاء.
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_DOCUMENT)

        with open(file_path, "rb") as f:
            await bot.send_document(
                chat_id=chat_id,
                document=f,
                caption=caption
            )

        logger.info(f"File sent successfully to {chat_id}: {file_path}")
        return True

    except Exception as e:
        logger.exception(f"Failed to send file to {chat_id}: {e}")
        return False
