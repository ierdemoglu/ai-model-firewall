#!/usr/bin/env python3
"""
Windows Build Script with Logo Support
"""

import os
import subprocess
import sys

def build_windows():
    print("🪟 Building Windows executable with logo...")

    icon_path = "assets/logo.ico"
    icon_param = f"--icon={icon_path}" if os.path.exists(icon_path) else ""

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name", "AI_Model_Firewall",
    ]
    
    if icon_param:
        cmd.append(icon_param)
    
    cmd.append("main.py")

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Windows build successful!")
        print("📁 Output: dist/AI_Model_Firewall.exe")
        print("\n⚠️ SmartScreen Warning: Instruct users to click 'More info' → 'Run anyway'")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_windows()