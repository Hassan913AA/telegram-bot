from services.storage_service import load_json
from utils.keyboard import build_menu
from config import logger

SECTIONS_FILE = "storage/sections.json"

def get_node(tree, path):
    node = tree["root"]
    for p in path[1:]:
        node = node["children"][p]
    return node

async def handle_menu(update, context):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    is_admin = user_id == context.bot_data.get("ADMIN")

    tree = load_json(SECTIONS_FILE)
    path = context.user_data.get("path", ["root"])

    try:
        if text == "🏠 الرئيسية":
            context.user_data["path"] = ["root"]
            node = get_node(tree, ["root"])
            return await update.message.reply_text("🏠 الرئيسية", reply_markup=build_menu({"children": node["children"], "path": ["root"]}, is_admin))

        if text == "🔙 رجوع":
            if len(path) > 1:
                path.pop()
            context.user_data["path"] = path
            node = get_node(tree, path)
            return await update.message.reply_text("🔙 رجوع", reply_markup=build_menu({"children": node["children"], "path": path}, is_admin))

        node = get_node(tree, path)

        if text in node["children"]:
            target = node["children"][text]

            if target["type"] == "menu":
                path.append(text)
                context.user_data["path"] = path
                return await update.message.reply_text(f"📂 {text}", reply_markup=build_menu({"children": target["children"], "path": path}, is_admin))

            if target["type"] == "file":
                await context.bot.send_document(update.effective_chat.id, target["file_id"], caption=target.get("file_name", "📄 ملف"))
                return

        return await update.message.reply_text("اختر من القائمة فقط")

    except Exception as e:
        logger.error(e)
        await update.message.reply_text("❌ خطأ داخلي")
