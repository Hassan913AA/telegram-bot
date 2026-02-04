from services.storage_service import load_json, save_json

SECTIONS_FILE = "storage/sections.json"

def get_tree():
    return load_json(SECTIONS_FILE) or {
        "root": {"title": "الرئيسية", "children": {}}
    }

def save_tree(tree):
    save_json(SECTIONS_FILE, tree)

def get_node_by_path(tree, path):
    node = tree["root"]
    for step in path:
        node = node["children"].get(step)
        if not node:
            return None
    return node

def add_menu(path, menu_name):
    tree = get_tree()
    node = get_node_by_path(tree, path)
    if node is None:
        return False
    node["children"][menu_name] = {
        "type": "menu",
        "children": {}
    }
    save_tree(tree)
    return True

def add_file(path, name, file_id):
    tree = get_tree()
    node = get_node_by_path(tree, path)
    if node is None:
        return False
    node["children"][name] = {
        "type": "file",
        "file_id": file_id,
        "file_name": name
    }
    save_tree(tree)
    return True
