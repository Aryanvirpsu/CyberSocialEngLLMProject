    # bootstrap.py
"""
Universal installer for the CYBER 221 LLM Safety Project.
- Ensures venv exists
- Ensures pip exists
- Installs missing pip if needed
- Installs all dependencies inside the venv

Works on Windows, macOS, Linux.
"""

import os
import sys
import subprocess
import ensurepip
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / "venv"


def run(cmd, env=None):
    """Run a shell command and print errors cleanly."""
    print(f"🔧 Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, env=env)


def ensure_venv():
    """Create virtual environment if missing."""
    if not VENV_DIR.exists():
        print("📦 Creating virtual environment...")
        run([sys.executable, "-m", "venv", "venv"])
    else:
        print("✔ Virtual environment already exists.")


def get_venv_python():
    """Return the Python executable inside venv."""
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_pip(python_exe):
    """Ensure pip exists inside the virtual environment."""
    try:
        run([str(python_exe), "-m", "pip", "--version"])
        print("✔ pip is installed.")
    except Exception:
        print("⚠️ pip not found — installing pip via ensurepip...")
        run([str(python_exe), "-m", "ensurepip", "--upgrade"])

    # Upgrade pip safely
    print("⬆️ Upgrading pip...")
    run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])


def install_requirements(python_exe):
    """Install dependencies into the virtual environment."""
    req = PROJECT_ROOT / "requirements.txt"

    if not req.exists():
        print("❌ requirements.txt missing!")
        return

    print("📦 Installing dependencies from requirements.txt...")
    run([str(python_exe), "-m", "pip", "install", "-r", str(req)])


def main():
    print("=====================================================")
    print("   CYBER 221 Project Bootstrap — Auto Installer")
    print("=====================================================")

    ensure_venv()
    venv_python = get_venv_python()

    ensure_pip(venv_python)
    install_requirements(venv_python)

    print("\n🎉 Installation Complete!")
    print("To run the project:")
    if os.name == "nt":
        print("  .\\venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")

    print("\nThen run:")
    print("  python main.py")
    print("\n=====================================================")


if __name__ == "__main__":
    main()
