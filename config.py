"""
AI Model Firewall - Configuration
"""
import os
from pathlib import Path

DEFAULT_MONITOR_PATHS = [
    os.path.expanduser("~/LM Studio/models"),
    os.path.expanduser("~/AppData/Local/LM Studio/models"),
    os.path.expanduser("~/.ollama/models"),
    os.path.expanduser("~/.cache/huggingface/hub"),
    os.path.expanduser("~/ai-models"),
    os.path.expanduser("~/models"),
]

SUPPORTED_EXTENSIONS = [".gguf", ".safetensors", ".bin", ".pt", ".pth"]
LOG_FILE = os.path.join(os.path.dirname(__file__), "firewall.log")
ENABLE_NOTIFICATIONS = True
QUARANTINE_DIR = os.path.join(os.path.dirname(__file__), "quarantine")
Path(QUARANTINE_DIR).mkdir(parents=True, exist_ok=True)