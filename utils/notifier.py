"""
Desktop Notifications
"""
import os
import sys
from config import ENABLE_NOTIFICATIONS

def show_notification(title: str, message: str):
    if not ENABLE_NOTIFICATIONS:
        print(f"[NOTIF] {title}: {message}")
        return
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name="AI Model Firewall", timeout=8)
    except ImportError:
        print(f"\n{'='*50}\n🛡️ {title}\n{'='*50}\n{message}\n{'='*50}\n")

def notify_scan_started(filename): show_notification("Model Scan Started", f"Scanning {filename}...")
def notify_safe(filename): show_notification("Safe Model", f"{filename} passed all checks ✅")
def notify_blocked(filename, reason, module): show_notification("Model Blocked", f"{filename} - {module}: {reason}")
def notify_quarantined(filename): show_notification("Quarantined", f"{filename} moved to quarantine folder.")
