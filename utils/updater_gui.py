"""
GUI Updater - Simple Tkinter-based update notification
"""
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import webbrowser


def show_update_dialog(latest_version: str, download_url: str, on_update_callback=None):
    """
    Shows a professional update notification dialog.
    """
    root = tk.Tk()
    root.withdraw()

    message = (
        f"A new security update is available for AI Model Firewall.\n\n"
        f"New Version: {latest_version}\n\n"
        f"Would you like to download it now?"
    )

    answer = messagebox.askyesno(
        "🛡️ AI Model Firewall - Security Update",
        message,
        icon="info"
    )

    if answer:
        progress_window = tk.Toplevel(root)
        progress_window.title("Downloading Update...")
        progress_window.geometry("320x100")
        progress_window.resizable(False, False)

        label = tk.Label(progress_window, text="Downloading... Please wait.", font=("Segoe UI", 10))
        label.pack(pady=10)

        progress = ttk.Progressbar(progress_window, length=280, mode='indeterminate')
        progress.pack(pady=5, padx=20)
        progress.start(10)

        def start_download():
            webbrowser.open(download_url)
            progress_window.destroy()
            root.destroy()
            
            if on_update_callback:
                on_update_callback()

        threading.Thread(target=start_download, daemon=True).start()

    else:
        root.destroy()


def check_and_show_update(updater_instance):
    """Check for updates and show GUI if available."""
    update_info = updater_instance.check_for_update()
    
    if update_info and update_info.get("update_available"):
        show_update_dialog(
            latest_version=update_info["latest_version"],
            download_url=update_info["download_url"]
        )
        return True
    return False
