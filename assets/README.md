# Assets - Logo and Icons

## Logo

The official logo of **AI Model Firewall** is located in `logo.svg`.

### How to Generate Platform Icons

#### For Windows (.ico)
1. Open `logo.svg` in a vector editor (Inkscape, Figma, or online converter)
2. Export as PNG (512x512 recommended)
3. Use an online converter (e.g. https://icoconvert.com) to create `logo.ico`

#### For macOS (.icns)
1. Export `logo.svg` as PNG (1024x1024)
2. Use `iconutil` on macOS:
   ```bash
   mkdir icon.iconset
   # Create multiple sizes: 16, 32, 128, 256, 512, 1024
   iconutil -c icns icon.iconset -o logo.icns
   ```

#### For Linux
- Use the SVG directly or convert to PNG (256x256 or 512x512)

## Usage in Build Scripts

The build scripts (`build_windows.py`, `build_macos.py`) are already configured to use:
- `assets/logo.ico` for Windows
- `assets/logo.icns` for macOS

Place the generated icon files in this `assets/` folder.