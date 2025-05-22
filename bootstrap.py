import os
import sys
import subprocess
import platform

def venv_path():
    return os.path.join(os.getcwd(), "venv")

def pip_path():
    if platform.system() == "Windows":
        return os.path.join(venv_path(), "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path(), "bin", "pip")

def python_path():
    if platform.system() == "Windows":
        return os.path.join(venv_path(), "Scripts", "python.exe")
    else:
        return os.path.join(venv_path(), "bin", "python")

def venv_exists():
    return os.path.exists(pip_path())

def create_venv():
    print("📦 Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", "venv"])

def install_requirements():
    pip = pip_path()
    req = "requirements.txt"
    if not os.path.isfile(req):
        print("⚠️  requirements.txt not found. Creating one from current packages...")
        subprocess.check_call([pip, "freeze"], stdout=open(req, "w"))
    print("📄 Installing dependencies from requirements.txt...")
    subprocess.check_call([pip, "install", "-r", req])
    print("✅ Dependencies installed.")

def main():
    if not venv_exists():
        create_venv()

    install_requirements()

    print("\n✅ Setup complete!")
    print("👉 To activate your virtual environment:")

    if platform.system() == "Windows":
        print(r"   .\venv\Scripts\activate")
    else:
        print("   source ./venv/bin/activate")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Command failed: {e}")
        sys.exit(1)
