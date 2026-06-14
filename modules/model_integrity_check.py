import os
from .base_module import BaseSecurityModule

class ModelIntegrityCheckModule(BaseSecurityModule):
    @property
    def name(self) -> str:
        return "Model Integrity & Safety Check"

    def scan(self, file_path: str) -> dict:
        filename = os.path.basename(file_path).lower()
        file_size = os.path.getsize(file_path)
        warnings = []
        errors = []

        if filename.endswith((".bin", ".pt", ".pth")):
            warnings.append("Legacy format detected - safetensors recommended.")
        if file_size < 1024 * 1024:
            errors.append(f"File too small ({file_size/1024:.1f} KB).")
        if file_size > 50 * 1024 * 1024 * 1024:
            warnings.append("File extremely large.")
        suspicious = ["malware", "trojan", "virus", "hacked", "backdoor"]
        for pattern in suspicious:
            if pattern in filename:
                errors.append(f"Suspicious filename: {pattern}")
        if filename.endswith(".gguf"):
            try:
                with open(file_path, "rb") as f:
                    if f.read(4) != b"GGUF":
                        errors.append("Invalid GGUF header!")
            except Exception as e:
                errors.append(f"Read error: {e}")

        if errors:
            return {"success": False, "message": " | ".join(errors)}
        elif warnings:
            return {"success": True, "message": "Warnings: " + " | ".join(warnings)}
        else:
            return {"success": True, "message": "Integrity checks passed."}
