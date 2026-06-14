"""
Auto-Discover Module - Cross-Platform
Automatically finds common AI model directories on Windows, macOS, and Linux.
"""

import os
import platform
from typing import List, Dict
from config import SUPPORTED_EXTENSIONS


def get_default_paths() -> Dict[str, str]:
    """
    Return platform-specific default paths for AI model directories.
    """
    user_home = os.path.expanduser("~")
    current_os = platform.system()
    paths = {}

    if current_os == "Windows":
        paths["LM Studio"] = os.path.join(user_home, "AppData", "Local", "LM Studio", "models")
        paths["Ollama"] = os.path.join(user_home, ".ollama", "models")
        paths["HuggingFace"] = os.path.join(user_home, ".cache", "huggingface", "hub")
        paths["Downloads"] = os.path.join(user_home, "Downloads")

    elif current_os == "Darwin":  # macOS
        paths["LM Studio"] = os.path.join(user_home, ".cache", "lm-studio", "models")
        paths["Ollama"] = os.path.join(user_home, ".ollama", "models")
        paths["HuggingFace"] = os.path.join(user_home, ".cache", "huggingface", "hub")
        paths["Downloads"] = os.path.join(user_home, "Downloads")

    elif current_os == "Linux":
        paths["LM Studio"] = os.path.join(user_home, ".cache", "lm-studio", "models")
        paths["Ollama"] = "/usr/share/ollama/.ollama/models"
        paths["HuggingFace"] = os.path.join(user_home, ".cache", "huggingface", "hub")
        paths["Downloads"] = os.path.join(user_home, "Downloads")

    return paths


def discover_model_directories() -> List[str]:
    """
    Scan common locations and return existing directories that contain model files.
    """
    found_paths = []
    default_paths = get_default_paths()

    for name, path in default_paths.items():
        if os.path.isdir(path):
            # Check if it contains any supported model files
            has_models = False
            try:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                            has_models = True
                            break
                    if has_models:
                        break
            except (PermissionError, OSError):
                continue

            if has_models:
                found_paths.append(path)
                print(f"[Discover] Found model directory ({name}): {path}")

    return found_paths


def get_all_model_files(directory: str) -> List[str]:
    """Recursively find all supported model files in a directory."""
    model_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                model_files.append(os.path.join(root, file))
    return model_files