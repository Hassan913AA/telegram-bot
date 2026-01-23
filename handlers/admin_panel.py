from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.storage_service import load_json, save_json
from utils.keyboard import main_menu_keyboard
from config import logger

SECTIONS_FILE = "storage/sections.json"


def get_node(data, path):
    """يصل إلى قائمة داخل قوائم: path = ['القائمة1','القائمة2']"""
    node = data
    for p in path:
        node = node.get(p, {}).get("sub", {})
    return node


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    kb = [
        [KeyboardButton("➕ إضافة زر/قائمة")],
        [KeyboardButton("✏️ تعديل زر/قائمة")],
        [KeyboardButton("🗑 حذف زر/قائمة")],
        [KeyboardButton("📎 زر يرسل ملف")],
        [KeyboardButton("📢 إرسال رسالة جماعية")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ]
    await update.message.reply_text("🛠 لوحة الأدمن", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "ADD_PATH"
    await update.message.reply_text("📍 أرسل موقع القائمة (مثال: رئيسية/برمجة/بايثون) أو /root")


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data["ADMIN"]:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state")
    data = load_json(SECTIONS_FILE) or {}

    # ===== إضافة =====
    if state == "ADD_PATH":
        context.user_data["path"] = [] if text == "/root" else text.split("/")
        context.user_data["state"] = "ADD_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر أو القائمة الجديدة:")
        return

    if state == "ADD_NAME":
        path = context.user_data["path"]
        node = get_node(data, path)

        node[text] = {
            "file": None,
            "sub": {
                "🔙 رجوع": {"file": None, "sub": {}},
                "🏠 الرئيسية": {"file": None, "sub": {}}
            }
        }

        save_json(SECTIONS_FILE, data)
        context.user_data.clear()
        await update.message.reply_text(f"✅ تم إنشاء: {text} في {'/'.join(path) if path else 'الرئيسية'}")
        return

    # ===== ربط ملف =====
    if state == "FILE_PATH":
        context.user_data["file_path"] = text.split("/")
        context.user_data["state"] = "FILE_NAME"
        await update.message.reply_text("✏️ أرسل اسم الزر الذي سيرسل الملف:")
        return

    if state == "FILE_NAME":
        context.user_data["file_button"] = text
        context.user_data["state"] = "WAIT_FILE"
        await update.message.reply_text("📎 الآن أرسل الملف:")
        return


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "FILE_PATH"
    await update.message.reply_text("📍 أرسل موقع الزر (مثال: رئيسية/برمجة):")


async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "WAIT_FILE":
        return

    doc = update.message.document
    data = load_json(SECTIONS_FILE) or {}

    path = context.user_data["file_path"]
    btn = context.user_data["file_button"]

    node = get_node(data, path)
    if btn not in node:
        await update.message.reply_text("❌ الزر غير موجود.")
        return

    node[btn]["file"] = {"file_id": doc.file_id, "file_name": doc.file_name}
    save_json(SECTIONS_FILE, data)

    context.user_data.clear()
    await update.message.reply_text(f"✅ تم ربط الملف بالزر: {btn}")


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏠 تم الرجوع", reply_markup=main_menu_keyboard(is_admin=True))
