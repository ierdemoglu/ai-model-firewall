"""
Auto-Discover Module - Cross-Platform with Ollama Support
Handles Ollama blobs (no extension), manifests, and regular model files.
"""

import os
import platform
from typing import List, Dict
from config import SUPPORTED_EXTENSIONS, MIN_OLLAMA_FILE_SIZE


def get_ollama_paths() -> List[str]:
    """Get all possible Ollama model paths."""
    user_home = os.path.expanduser("~")
    current_os = platform.system()
    paths = []
    
    if current_os == "Windows":
        paths.append(os.path.join(user_home, ".ollama", "models"))
    elif current_os == "Darwin":
        paths.append(os.path.join(user_home, ".ollama", "models"))
        paths.append("/usr/local/share/ollama/.ollama/models")
    else:
        paths.append(os.path.join(user_home, ".ollama", "models"))
        paths.append("/usr/share/ollama/.ollama/models")
        paths.append("/usr/local/share/ollama/.ollama/models")
    
    return paths


def get_default_paths() -> Dict[str, str]:
    """Return platform-specific default paths."""
    user_home = os.path.expanduser("~")
    current_os = platform.system()
    paths = {}

    if current_os == "Windows":
        paths["LM Studio"] = os.path.join(user_home, "AppData", "Local", "LM Studio", "models")
        paths["HuggingFace"] = os.path.join(user_home, ".cache", "huggingface", "hub")
    elif current_os == "Darwin":
        paths["LM Studio"] = os.path.join(user_home, ".cache", "lm-studio", "models")
        paths["HuggingFace"] = os.path.join(user_home, ".cache", "huggingface", "hub")
    else:
        paths["LM Studio"] = os.path.join(user_home, ".cache", "lm-studio", "models")
        paths["HuggingFace"] = os.path.join(user_home, ".cache", "huggingface", "hub")

    # Add Ollama paths
    for i, path in enumerate(get_ollama_paths()):
        paths[f"Ollama_{i}"] = path

    return paths


def is_valid_ollama_blob(file_path: str) -> bool:
    """
    Check if a file is a valid Ollama blob (model file without extension).
    Ollama stores model weights in blobs/ directory as sha256-xxx files.
    """
    if not os.path.isfile(file_path):
        return False
    
    # Must be in blobs directory
    if "blobs" not in file_path:
        return False
    
    # Must be larger than minimum size (ignore small manifest files)
    try:
        size = os.path.getsize(file_path)
        if size < MIN_OLLAMA_FILE_SIZE:
            return False
    except:
        return False
    
    # Filename should start with sha256- (Ollama naming convention)
    filename = os.path.basename(file_path)
    if not filename.startswith("sha256-"):
        return False
    
    return True


def is_supported_model_file(file_path: str) -> bool:
    """
    Check if file is a supported model file.
    Handles both extension-based files and Ollama blobs.
    """
    filename = os.path.basename(file_path).lower()
    
    # Check for standard extensions
    for ext in SUPPORTED_EXTENSIONS:
        if ext and filename.endswith(ext):
            return True
    
    # Check for Ollama blob (no extension, but valid blob)
    if is_valid_ollama_blob(file_path):
        return True
    
    return False


def discover_model_directories() -> List[str]:
    """Scan and return directories containing model files."""
    found_paths = []
    default_paths = get_default_paths()

    for name, path in default_paths.items():
        if os.path.isdir(path):
            has_models = False
            try:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if is_supported_model_file(full_path):
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
    """Find all supported model files in a directory."""
    model_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            if is_supported_model_file(full_path):
                model_files.append(full_path)
    return model_files


def scan_existing_models(directories: List[str]) -> List[str]:
    """Scan existing model files in directories."""
    all_models = []
    for directory in directories:
        if os.path.isdir(directory):
            models = get_all_model_files(directory)
            all_models.extend(models)
            if models:
                print(f"[Discover] Found {len(models)} existing models in {directory}")
    return all_models
