import json
import os
from utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")


def _get_path(filename: str) -> str:
    return os.path.join(STORAGE_DIR, filename)


def load_json(filename: str, default):
    path = _get_path(filename)

    if not os.path.exists(path):
        logger.warning(f"{filename} not found, creating new with default.")
        save_json(filename, default)
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"{filename} loaded successfully.")
            return data
    except Exception as e:
        logger.exception(f"Failed to load {filename}: {e}")
        return default


def save_json(filename: str, data):
    path = _get_path(filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"{filename} saved successfully.")
    except Exception as e:
        logger.exception(f"Failed to save {filename}: {e}")


def update_json(filename: str, update_func):
    """
    تحميل الملف → تعديل البيانات بدالة → حفظه من جديد
    """
    data = load_json(filename, default={})
    try:
        update_func(data)
        save_json(filename, data)
    except Exception as e:
        logger.exception(f"Failed to update {filename}: {e}")
