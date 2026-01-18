from services.storage_service import load_json, save_json
from utils.logger import get_logger

logger = get_logger(__name__)

USERS_FILE = "users.json"


def load_users() -> set:
    try:
        data = load_json(USERS_FILE, default=[])
        return set(data)
    except Exception as e:
        logger.exception(f"Failed to load users: {e}")
        return set()


def save_users(users: set):
    try:
        save_json(USERS_FILE, list(users))
    except Exception as e:
        logger.exception(f"Failed to save users: {e}")


def add_user(user_id: int, users: set):
    if user_id not in users:
        users.add(user_id)
        save_users(users)
        logger.info(f"New user added: {user_id}")


def remove_user(user_id: int, users: set):
    if user_id in users:
        users.remove(user_id)
        save_users(users)
        logger.info(f"User removed: {user_id}")
