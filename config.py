"""
AI Model Firewall - Configuration
"""
import os
from pathlib import Path

# Supported model file extensions (including Ollama blobs without extension)
SUPPORTED_EXTENSIONS = [
    ".gguf", ".safetensors", ".bin", ".pt", ".pth",
    ""  # Empty extension for Ollama blobs
]

DEFAULT_MONITOR_PATHS = [
    os.path.expanduser("~/LM Studio/models"),
    os.path.expanduser("~/AppData/Local/LM Studio/models"),
    os.path.expanduser("~/.ollama/models"),
    os.path.expanduser("~/.cache/huggingface/hub"),
    os.path.expanduser("~/ai-models"),
    os.path.expanduser("~/models"),
]

LOG_FILE = os.path.join(os.path.dirname(__file__), "firewall.log")
ENABLE_NOTIFICATIONS = True
QUARANTINE_DIR = os.path.join(os.path.dirname(__file__), "quarantine")
Path(QUARANTINE_DIR).mkdir(parents=True, exist_ok=True)

# Ollama specific settings
OLLAMA_BLOBS_DIR = "blobs"
OLLAMA_MANIFESTS_DIR = "manifests"
MIN_OLLAMA_FILE_SIZE = 1024 * 1024  # 1MB - ignore small manifest files
