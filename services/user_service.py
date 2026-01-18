import json
import os
from services.storage_service import load_json, save_json
from utils.logger import logger

USERS_PATH = "storage/users.json"

def load_users():
    try:
        return set(load_json(USERS_PATH))
    except Exception as e:
        logger.error(f"Failed to load users: {e}")
        return set()

def save_users(users):
    try:
        save_json(USERS_PATH, list(users))
    except Exception as e:
        logger.error(f"Failed to save users: {e}")
