import os
import hashlib
import requests
from typing import Optional, Dict, Any
from .base_module import BaseSecurityModule

class VirusTotalCheckModule(BaseSecurityModule):
    VT_API_URL = "https://www.virustotal.com/api/v3/files"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VIRUSTOTAL_API_KEY")
        self.enabled = bool(self.api_key)

    @property
    def name(self) -> str:
        return "VirusTotal Malware Scan"

    def _get_file_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def _query_virustotal(self, file_hash: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "API key not configured"}
        headers = {"x-apikey": self.api_key}
        url = f"{self.VT_API_URL}/{file_hash}"
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                return {
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                }
            elif response.status_code == 404:
                return {"not_found": True}
            else:
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def scan(self, file_path: str) -> dict:
        if not self.enabled:
            return {"success": True, "message": "VirusTotal API key not configured."}
        try:
            file_hash = self._get_file_hash(file_path)
            result = self._query_virustotal(file_hash)
            if "error" in result:
                return {"success": True, "message": f"VirusTotal error: {result['error']}"}
            if result.get("not_found"):
                return {"success": True, "message": "Not found in VirusTotal database."}
            malicious = result.get("malicious", 0)
            suspicious = result.get("suspicious", 0)
            if malicious > 0:
                return {"success": False, "message": f"VirusTotal: {malicious} engines flagged as malicious!"}
            elif suspicious > 2:
                return {"success": False, "message": f"VirusTotal: {suspicious} engines flagged as suspicious."}
            else:
                return {"success": True, "message": "VirusTotal: Clean."}
        except Exception as e:
            return {"success": True, "message": f"VirusTotal error: {e}"}
