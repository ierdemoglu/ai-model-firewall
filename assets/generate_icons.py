#!/usr/bin/env python3
"""
Icon Generator - Creates platform-specific icons from a single PNG/SVG
Run this script when you have a new logo.png to generate all required icons.
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Run: pip install Pillow")
    exit(1)


def generate_icons(source_png: str = "logo.png"):
    """
    Generate Windows .ico and prepare for macOS .icns from a single PNG.
    """
    if not os.path.exists(source_png):
        print(f"❌ Source file not found: {source_png}")
        print("Please place your high-resolution logo (at least 512x512) as 'logo.png' in this folder.")
        return

    img = Image.open(source_png)
    assets_dir = Path(__file__).parent

    # === Windows .ico (multi-size) ===
    ico_path = assets_dir / "logo.ico"
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    img.save(ico_path, format="ICO", sizes=sizes)
    print(f"✅ Windows icon created: {ico_path}")

    # === macOS preparation ===
    print("\n📌 For macOS icon (.icns):")
    print("   1. Use an online converter or 'iconutil' on macOS")
    print("   2. Recommended sizes: 16, 32, 128, 256, 512, 1024 px")
    print("   3. Save the result as 'assets/logo.icns'")

    # Optional: Create a simple 512px PNG for reference
    png_512 = assets_dir / "logo_512.png"
    img.resize((512, 512), Image.LANCZOS).save(png_512)
    print(f"\n✅ Reference PNG created: {png_512}")


if __name__ == "__main__":
    generate_icons()