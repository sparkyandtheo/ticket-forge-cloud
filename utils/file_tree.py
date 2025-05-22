import os

def create_project_structure(base_path, file_tree):
    created_paths = []
    for folder, items in file_tree.items():
        base_folder = os.path.join(base_path, folder)
        os.makedirs(base_folder, exist_ok=True)
        if folder:
            created_paths.append(base_folder)
        for item in items:
            item_path = os.path.join(base_folder, item)
            if item.endswith("/"):
                os.makedirs(item_path, exist_ok=True)
                created_paths.append(item_path)
            else:
                os.makedirs(os.path.dirname(item_path), exist_ok=True)
                with open(item_path, "w") as f:
                    f.write("")
                created_paths.append(item_path)
    return created_paths

def generate_tree_output(base_path):
    tree_lines = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d != "venv"]
        rel_root = os.path.relpath(root, base_path)
        indent_level = rel_root.count(os.sep) if rel_root != "." else 0
        indent = "    " * indent_level
        tree_lines.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = "    " * (indent_level + 1)
        for f in files:
            tree_lines.append(f"{sub_indent}{f}")
    return "\n".join(tree_lines)
