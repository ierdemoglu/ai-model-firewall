import os
import time
import hashlib
import requests
from typing import Optional, Dict
from .base_module import BaseSecurityModule

class HFHashCheckModule(BaseSecurityModule):
    _cache: Dict[str, tuple] = {}
    CACHE_TTL = 6 * 3600

    @property
    def name(self) -> str:
        return "Hugging Face Hash Verification"

    def _extract_repo_from_path(self, file_path: str) -> Optional[str]:
        path_parts = file_path.replace("\\", "/").split("/")
        for part in path_parts:
            if part.startswith("models--"):
                return part.replace("models--", "").replace("--", "/")
        return None

    def _get_original_hash(self, file_path: str) -> Optional[str]:
        repo_id = self._extract_repo_from_path(file_path)
        if not repo_id:
            return None
        if repo_id in self._cache:
            cached_hash, timestamp = self._cache[repo_id]
            if time.time() - timestamp < self.CACHE_TTL:
                return cached_hash
        filename = os.path.basename(file_path)
        try:
            api_url = f"https://huggingface.co/api/models/{repo_id}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for sibling in data.get("siblings", []):
                    if sibling.get("rfilename") == filename and "sha" in sibling:
                        original_hash = sibling["sha"]
                        self._cache[repo_id] = (original_hash, time.time())
                        return original_hash
        except Exception:
            pass
        return None

    def scan(self, file_path: str) -> dict:
        original_hash = self._get_original_hash(file_path)
        if not original_hash:
            return {"success": True, "message": "Model not found on Hugging Face."}
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(1024 * 1024):
                    sha256_hash.update(chunk)
            local_hash = sha256_hash.hexdigest()
        except Exception as e:
            return {"success": False, "message": f"File read error: {e}"}
        if local_hash.lower() == original_hash.lower():
            return {"success": True, "message": "File integrity verified."}
        else:
            return {"success": False, "message": "Hash mismatch!"}
