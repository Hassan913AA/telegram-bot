from telegram.constants import ChatAction
from utils.logger import logger

async def safe_send_pdf(bot, chat_id, path, caption):
    try:
        await bot.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
        with open(path, "rb") as f:
            await bot.send_document(chat_id, f, caption=caption)
        return True
    except Exception as e:
        logger.error(f"PDF send failed: {e}")
        return False
