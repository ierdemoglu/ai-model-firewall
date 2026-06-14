#!/usr/bin/env python3
"""
Linux Build Script - Creates AppImage or simple executable
Usage: python build_linux.py
"""

import os
import subprocess
import sys

def build_linux():
    print("🐧 Building Linux executable...")

    # Simple onefile build (can be turned into AppImage later)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "AI_Model_Firewall",
        "main.py"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Linux build successful!")
        print("📁 Output: dist/AI_Model_Firewall")
        print("\nTip: For easier distribution, consider creating an AppImage.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_linux()