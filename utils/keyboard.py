from telegram import ReplyKeyboardMarkup, KeyboardButton

def build_menu(node, is_admin=False):
    buttons = []

    for name in node.get("children", {}).keys():
        buttons.append([KeyboardButton(name)])

    if node.get("path") != ["root"]:
        buttons.append([KeyboardButton("🔙 رجوع")])

    buttons.append([KeyboardButton("🏠 الرئيسية")])

    if is_admin:
        buttons.append([KeyboardButton("🛠 لوحة التحكم")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
