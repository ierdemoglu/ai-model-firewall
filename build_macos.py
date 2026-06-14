#!/usr/bin/env python3
"""
macOS Build Script - Creates proper .app bundle
This MUST be run on macOS to create a working application.

Usage: python build_macos.py
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def build_macos():
    print("🍎 Building macOS Application Bundle...")
    print("=" * 60)
    
    if sys.platform != "darwin":
        print("❌ ERROR: This script must be run on macOS!")
        print("   Current platform:", sys.platform)
        print("   Please run this on a Mac computer.")
        return False
    
    # Clean previous builds
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Cleaned {folder}/")
    
    icon_path = "assets/logo.icns"
    
    # Build command with correct parameters for macOS
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onedir",                    # Creates proper .app structure
        "--windowed",                  # No console window
        "--name", "AI_Model_Firewall",
        "--osx-bundle-identifier", "com.aimodelfirewall.app",
        "--hidden-import=tkinter",
        "--hidden-import=plyer",
    ]
    
    if os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
        print(f"✅ Using icon: {icon_path}")
    
    cmd.append("main.py")
    
    try:
        print("\n🔨 Running PyInstaller (this may take a few minutes)...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        app_path = Path("dist/AI_Model_Firewall.app")
        
        if app_path.exists():
            print("\n" + "=" * 60)
            print("✅ SUCCESS! macOS Application Bundle Created")
            print("=" * 60)
            print(f"📁 App Location: {app_path.absolute()}")
            print("\n📋 Installation Instructions:")
            print("   1. Copy 'AI_Model_Firewall.app' to /Applications folder")
            print("   2. Double-click to launch")
            print("   3. If macOS blocks it:")
            print("      - Right-click → Open (first time only)")
            print("      - Or: System Settings → Privacy & Security → Open Anyway")
            print("\n💡 The app will appear in your Applications folder")
            print("=" * 60)
            return True
        else:
            print("❌ .app bundle was not created!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed!")
        if e.stdout:
            print("STDOUT:", e.stdout[-2000:] if len(e.stdout) > 2000 else e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr[-2000:] if len(e.stderr) > 2000 else e.stderr)
        return False

if __name__ == "__main__":
    success = build_macos()
    sys.exit(0 if success else 1)
