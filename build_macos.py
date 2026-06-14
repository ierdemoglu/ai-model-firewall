#!/usr/bin/env python3
"""
macOS Build Script - Creates .app bundle
Run this on macOS to create a distributable application.

For users without Apple Developer Account ($99/year):
After building, users will need to run:
    xattr -cr /Applications/AI_Model_Firewall.app

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
        print(f"   Current platform: {sys.platform}")
        print("   Please run this script on a Mac computer.")
        return False
    
    # Clean previous builds
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Cleaned {folder}/")
    
    icon_path = "assets/logo.icns"
    
    # Build command optimized for macOS
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onedir",
        "--windowed",
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
        print("\n🔨 Running PyInstaller (this may take 2-5 minutes)...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        app_path = Path("dist/AI_Model_Firewall.app")
        
        if app_path.exists():
            print("\n" + "=" * 60)
            print("✅ SUCCESS! macOS Application Created")
            print("=" * 60)
            print(f"📁 App Location: {app_path.absolute()}")
            print("\n📋 For Users (No Apple Developer Account Needed):")
            print("   1. Copy AI_Model_Firewall.app to /Applications")
            print("   2. Open Terminal and run:")
            print("      xattr -cr /Applications/AI_Model_Firewall.app")
            print("   3. Double-click the app to launch")
            print("\n💡 The xattr command removes macOS quarantine flag")
            print("=" * 60)
            return True
        else:
            print("❌ .app bundle was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed!")
        return False

if __name__ == "__main__":
    success = build_macos()
    sys.exit(0 if success else 1)
