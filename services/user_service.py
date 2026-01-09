import json
import os
from config import logger

USERS_PATH = "storage/users.json"

def load_users():
    if os.path.exists(USERS_PATH):
        try:
            with open(USERS_PATH, "r") as f:
                return set(json.load(f))
        except Exception as e:
            logger.error(f"Failed to load users: {e}")
            return set()
    return set()

def save_users(users):
    try:
        with open(USERS_PATH, "w") as f:
            json.dump(list(users), f)
    except Exception as e:
        logger.error(f"Failed to save users: {e}")
