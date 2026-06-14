"""
File System Monitor (Watchdog)
"""
import time
import os
from typing import List, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import SUPPORTED_EXTENSIONS
from utils.logger import log_info, log_warning

class ModelFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.processed_files = set()

    def on_created(self, event):
        if not event.is_directory:
            self._handle_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._handle_file(event.dest_path)

    def _handle_file(self, file_path: str):
        if any(file_path.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            time.sleep(2)
            if os.path.exists(file_path) and file_path not in self.processed_files:
                self.processed_files.add(file_path)
                log_info(f"New model file detected: {file_path}")
                self.callback(file_path)

class DirectoryMonitor:
    def __init__(self, directories: List[str], callback: Callable[[str], None]):
        self.directories = directories
        self.callback = callback
        self.observers = []

    def start(self):
        handler = ModelFileHandler(self.callback)
        for directory in self.directories:
            if os.path.isdir(directory):
                observer = Observer()
                observer.schedule(handler, directory, recursive=True)
                observer.start()
                self.observers.append(observer)
                log_info(f"Monitoring started: {directory}")
            else:
                log_warning(f"Directory does not exist: {directory}")

    def stop(self):
        for observer in self.observers:
            observer.stop()
        for observer in self.observers:
            observer.join()
        log_info("All monitors stopped.")

    def run_forever(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()