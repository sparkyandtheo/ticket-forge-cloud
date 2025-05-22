# init.ps1 — Run this in your project root

Write-Host "🚀 Setting up project..."

# Create folders
mkdir -Force scripts, utils

# Move main file if it exists
if (Test-Path .\init_tree.py) {
    Move-Item .\init_tree.py .\scripts\init_tree.py -Force
}

# Create helper module
@"
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
"@ | Out-File -Encoding UTF8 .\utils\file_tree.py

# Create updated init_tree script
@"
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
"@ | Out-File -Encoding UTF8 .\scripts\init_tree.py

# Create pyproject.toml for black
@"
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.mypy_cache
  | \.venv
  | build
  | dist
)/
'''
"@ | Out-File -Encoding UTF8 .\pyproject.toml

# Create flake8 config
@"
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,build,dist
"@ | Out-File -Encoding UTF8 .\.flake8

# Install and freeze tools
pip install black flake8
pip freeze | Out-File -Encoding ASCII .\requirements.txt

Write-Host "✅ Project initialized and linting tools ready."
