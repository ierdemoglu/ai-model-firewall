#!/usr/bin/env python3
"""
AI Model Firewall - Tkinter GUI
"""
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DEFAULT_MONITOR_PATHS, QUARANTINE_DIR
from core.discover import discover_model_directories
from core.monitor import DirectoryMonitor
from core.pipeline import SecurityPipeline
from utils.logger import log_info, log_error
from utils.notifier import show_notification

class AIModelFirewallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ AI Model Firewall")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)

        self.monitor = None
        self.is_running = False
        self.pipeline = SecurityPipeline()
        self.scanned_count = 0
        self.blocked_count = 0

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header, text="🛡️ AI Model Firewall", font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        self.status_label = ttk.Label(header, text="● Stopped", font=("Segoe UI", 11), foreground="red")
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Control Panel
        control = ttk.LabelFrame(main_frame, text="Control Panel", padding=10)
        control.pack(fill=tk.X, pady=5)

        btns = ttk.Frame(control)
        btns.pack(fill=tk.X)

        self.start_btn = ttk.Button(btns, text="▶ Start Monitoring", command=self.start_monitoring, width=20)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btns, text="⏹ Stop Monitoring", command=self.stop_monitoring, width=20, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(btns, text="🔄 Rescan Directories", command=self._discover_directories, width=22).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="📁 Quarantine Folder", command=self.open_quarantine, width=20).pack(side=tk.LEFT, padx=5)

        # Directories
        dir_frame = ttk.LabelFrame(main_frame, text="Monitored Directories", padding=8)
        dir_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        self.dir_listbox = tk.Listbox(dir_frame, height=5, font=("Consolas", 9))
        self.dir_listbox.pack(fill=tk.BOTH, expand=True)

        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Event Log", padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=("Consolas", 9), state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.tag_config("success", foreground="#2e7d32")
        self.log_text.tag_config("error", foreground="#c62828")
        self.log_text.tag_config("warning", foreground="#f57c00")
        self.log_text.tag_config("info", foreground="#1565c0")

        # Status bar
        status_bar = ttk.Frame(main_frame)
        status_bar.pack(fill=tk.X, pady=(5, 0))
        self.stats_label = ttk.Label(status_bar, text="Scanned: 0  |  Blocked: 0  |  Modules: 5", font=("Segoe UI", 9))
        self.stats_label.pack(side=tk.LEFT)
        ttk.Label(status_bar, text="v2.0  |  Modular Security Firewall", font=("Segoe UI", 8), foreground="gray").pack(side=tk.RIGHT)

        self._discover_directories()

    def _log(self, message, level="info"):
        self.log_text.config(state=tk.NORMAL)
        ts = time.strftime("%H:%M:%S")
        prefix = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(level, "•")
        self.log_text.insert(tk.END, f"[{ts}] {prefix} {message}\n", level)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _discover_directories(self):
        self.dir_listbox.delete(0, tk.END)
        discovered = discover_model_directories()
        all_paths = list(set(discovered + [os.path.expanduser(p) for p in DEFAULT_MONITOR_PATHS]))
        valid = [p for p in all_paths if os.path.isdir(p)]
        for p in valid:
            self.dir_listbox.insert(tk.END, f"📁 {p}")
        self._log(f"{len(valid)} directories discovered", "info")
        return valid

    def start_monitoring(self):
        if self.is_running:
            return
        paths = self._discover_directories()
        if not paths:
            messagebox.showwarning("Warning", "No directories found to monitor!")
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="● Active - Monitoring", foreground="#2e7d32")
        self._log("Starting file system monitor...", "info")

        def run():
            try:
                self.monitor = DirectoryMonitor(paths, self._handle_new_model)
                self.monitor.start()
                self.monitor.run_forever()
            except Exception as e:
                self._log(f"Monitor error: {e}", "error")

        threading.Thread(target=run, daemon=True).start()
        self._log("Monitoring active.", "success")

    def stop_monitoring(self):
        if not self.is_running:
            return
        self.is_running = False
        if self.monitor:
            self.monitor.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="● Stopped", foreground="red")
        self._log("Monitoring stopped.", "warning")

    def _handle_new_model(self, file_path):
        filename = os.path.basename(file_path)
        self.root.after(0, lambda: self._log(f"New file detected: {filename}", "info"))

        result = self.pipeline.execute(file_path)

        if result["safe"]:
            self.scanned_count += 1
            self.root.after(0, lambda: self._log(f"✅ SAFE: {filename}", "success"))
            self.root.after(0, lambda: show_notification("Safe Model", f"{filename} passed all checks."))
        else:
            self.blocked_count += 1
            reason = result.get("reason", "Unknown")
            module = result.get("module", "Unknown")
            self.root.after(0, lambda: self._log(f"❌ BLOCKED: {filename} ({module})", "error"))
            self.root.after(0, lambda: self._log(f"   Reason: {reason}", "error"))

            try:
                qpath = os.path.join(QUARANTINE_DIR, filename)
                if os.path.exists(qpath):
                    base, ext = os.path.splitext(filename)
                    qpath = os.path.join(QUARANTINE_DIR, f"{base}_{int(time.time())}{ext}")
                os.rename(file_path, qpath)
                self.root.after(0, lambda: self._log(f"Moved to quarantine.", "warning"))
            except Exception as e:
                self.root.after(0, lambda: self._log(f"Quarantine error: {e}", "error"))

        self.root.after(0, self._update_stats)

    def _update_stats(self):
        self.stats_label.config(text=f"Scanned: {self.scanned_count}  |  Blocked: {self.blocked_count}  |  Modules: {len(self.pipeline.modules)}")

    def open_quarantine(self):
        if not os.path.exists(QUARANTINE_DIR):
            os.makedirs(QUARANTINE_DIR, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(QUARANTINE_DIR)
        elif sys.platform == "darwin":
            os.system(f"open {QUARANTINE_DIR}")
        else:
            os.system(f"xdg-open {QUARANTINE_DIR}")

    def on_closing(self):
        if self.is_running and self.monitor:
            self.monitor.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AIModelFirewallGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
