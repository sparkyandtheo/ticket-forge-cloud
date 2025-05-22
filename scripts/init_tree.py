import os
from utils.file_tree import create_project_structure, generate_tree_output

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__ + "/.."))

file_tree = {
    "src": ["__init__.py", "main.py"],
    "tests": ["__init__.py", "test_main.py"],
    "docs": [],
    "data": ["raw/", "processed/"],
    "configs": ["settings.yaml"],
    "scripts": [],
    "notebooks": [],
    "assets": [],
    "logs": [],
    ".github": ["workflows/ci.yml"],
    "": ["README.md", ".gitignore", "requirements.txt", "setup.py"]
}

if __name__ == "__main__":
    create_project_structure(PROJECT_ROOT, file_tree)
    tree_output = generate_tree_output(PROJECT_ROOT)
    logs_dir = os.path.join(PROJECT_ROOT, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    with open(os.path.join(logs_dir, "tree.txt"), "w") as f:
        f.write(tree_output)
    print("✅ Structure created and logged to logs/tree.txt")
