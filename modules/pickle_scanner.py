import os
from .base_module import BaseSecurityModule

class PickleScannerModule(BaseSecurityModule):
    SUSPICIOUS_PATTERNS = [
        b"os.system", b"subprocess", b"__import__", 
        b"eval(", b"exec(", b"pickle.loads", b"__reduce__"
    ]

    @property
    def name(self) -> str:
        return "Pickle Injection Scanner"

    def scan(self, file_path: str) -> dict:
        filename = os.path.basename(file_path).lower()
        if not filename.endswith((".bin", ".pth", ".pt")):
            return {"success": True, "message": "Safe format."}
        try:
            with open(file_path, "rb") as f:
                content = f.read(10 * 1024 * 1024)
            found = [p.decode(errors="ignore") for p in self.SUSPICIOUS_PATTERNS if p in content]
            if found:
                return {"success": False, "message": f"Suspicious commands detected: {', '.join(found)}"}
            return {"success": True, "message": "Pickle scan clean."}
        except Exception as e:
            return {"success": True, "message": f"Scan error: {e}"}
