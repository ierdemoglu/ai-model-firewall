# 🛡️ AI Model Firewall

**Cross-Platform • Modular • Event-Driven AI Model Security**

AI Model Firewall is a plug-and-play security tool that automatically scans, verifies hashes, and checks for malware when downloading large language models (LLMs) locally.

---

## ✨ Features

- **Cross-Platform**: Windows, macOS, and Linux support
- **Auto Discovery**: Automatically finds LM Studio, Ollama, Hugging Face Cache directories
- **Real-time Monitoring**: Detects new model files instantly with Watchdog
- **6-Layer Security**:
  1. Disk Space Guard
  2. Hugging Face Hash Verification (with caching)
  3. VirusTotal Malware Scanning
  4. Pickle Injection Scanner (RCE protection)
  5. Model Integrity Checks
- **Quarantine System**
- **Modern GUI + CLI**
- **Docker Support** (for enterprise/server use)

---

## 🚀 Installation

### Run with CLI / GUI (All Platforms)

```bash
git clone https://github.com/yourusername/ai-model-firewall.git
cd ai-model-firewall
pip install -r requirements.txt

# GUI
python gui.py

# CLI
python main.py
```

### VirusTotal Support (Optional)

```bash
export VIRUSTOTAL_API_KEY="your_api_key"
```

---

## 📦 macOS Installation

### Method 1: Run from Source (Recommended)

```bash
git clone https://github.com/yourusername/ai-model-firewall.git
cd ai-model-firewall
pip install -r requirements.txt
python gui.py
```

### Method 2: Using Pre-built .app (No Apple Developer Account)

If you downloaded `AI_Model_Firewall.app`:

1. **Copy to Applications folder:**
   ```bash
   cp -r AI_Model_Firewall.app /Applications/
   ```

2. **Remove quarantine flag (IMPORTANT):**
   ```bash
   xattr -cr /Applications/AI_Model_Firewall.app
   ```

3. **Launch the application:**
   - Double-click `AI_Model_Firewall.app`
   - If macOS blocks it: Right-click → Open

> **Why this step?** macOS adds a quarantine flag to apps downloaded from the internet. The `xattr -cr` command removes this flag, allowing the app to run without an Apple Developer certificate.

---

## 📦 Distribution (Build)

### Windows
```bash
python build_windows.py
```

### macOS
```bash
python build_macos.py
```

### Linux
```bash
python build_linux.py
```

Or with Docker:
```bash
docker build -t ai-model-firewall .
docker run -v ~/models:/models ai-model-firewall
```

---

## ⚠️ Windows SmartScreen Warning

When running the `.exe` for the first time on Windows, SmartScreen may show:

> **"Windows protected your PC – Unknown Publisher"**

**Solution:**
1. Click **"More info"** at the bottom of the warning.
2. Select **"Run anyway"**.

This is normal behavior. The warning will be removed once a code signing certificate is obtained.

---

## ⚖️ License & Transparency Statement

This project is licensed under the **Business Source License (BSL 1.1)**.

- **Individual / Educational Use**: Free
- **Commercial / Enterprise Use**: Requires a paid license

AI tools were used during development. All code has been manually reviewed and tested.

See `LICENSE.md` and `README.md` for details.

---

## 🏗️ Architecture

The system is fully modular and extensible. Add new security modules by simply placing new files in the `modules/` directory.

---

*Cross-Platform AI Model Security — Everywhere, for everyone.*
