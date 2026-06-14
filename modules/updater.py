"""
Simple Auto-Updater Module (GitHub Releases based)
Checks for newer versions on GitHub and notifies the user.
This is a lightweight implementation suitable for v1.1.0+.
"""

import os
import json
import requests
from packaging import version
from utils.logger import log_info


class SimpleUpdater:
    """
    Lightweight auto-updater using GitHub Releases API.
    """

    GITHUB_REPO = "kullanici/ai-model-firewall"  # ← Change this to your actual repo
    CURRENT_VERSION = "1.0.0"

    def check_for_update(self) -> dict:
        """
        Check GitHub for the latest release.
        Returns dict with update info or None.
        """
        try:
            url = f"https://api.github.com/repos/{self.GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=8)
            
            if response.status_code != 200:
                return None

            data = response.json()
            latest_version = data.get("tag_name", "").lstrip("v")
            current = self.CURRENT_VERSION.lstrip("v")

            if version.parse(latest_version) > version.parse(current):
                return {
                    "update_available": True,
                    "latest_version": latest_version,
                    "current_version": self.CURRENT_VERSION,
                    "download_url": data.get("html_url"),
                    "release_notes": data.get("body", "")[:300] + "..."
                }
            return {"update_available": False}

        except Exception as e:
            log_info(f"Updater check failed: {e}")
            return None

    def notify_update(self, update_info: dict):
        """Simple console/GUI notification."""
        if update_info and update_info.get("update_available"):
            print("\n" + "="*60)
            print("🆕 YENİ GÜNCELLEME MEVCUT!")
            print(f"   Mevcut sürüm : {update_info['current_version']}")
            print(f"   Yeni sürüm   : {update_info['latest_version']}")
            print(f"   İndir        : {update_info['download_url']}")
            print("="*60 + "\n")
            return True
        return False