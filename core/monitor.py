"""
File System Monitor using Watchdog.
Watches directories for new model files including Ollama blobs.
"""

import time
import os
from typing import List, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent

from config import SUPPORTED_EXTENSIONS, MIN_OLLAMA_FILE_SIZE
from utils.logger import log_info, log_warning
from core.discover import is_supported_model_file, is_valid_ollama_blob


class ModelFileHandler(FileSystemEventHandler):
    """
    Custom event handler that filters for model files and calls the callback.
    """

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
        """Check if file is a supported model and not already processed."""
        
        # Wait for file to finish writing (important for large Ollama blobs)
        time.sleep(3)
        
        if not os.path.exists(file_path):
            return
            
        if file_path in self.processed_files:
            return
        
        # Check if it's a supported model file (including Ollama blobs)
        if is_supported_model_file(file_path):
            self.processed_files.add(file_path)
            log_info(f"New model file detected: {file_path}")
            self.callback(file_path)
        else:
            # Log why it was skipped (for debugging)
            filename = os.path.basename(file_path)
            if "blobs" in file_path and not filename.startswith("sha256-"):
                log_info(f"Skipped non-Ollama blob file: {filename}")


class DirectoryMonitor:
    """
    Manages watchdog observers for multiple directories.
    """

    def __init__(self, directories: List[str], callback: Callable[[str], None]):
        self.directories = directories
        self.callback = callback
        self.observers = []

    def start(self):
        """Start monitoring all directories."""
        handler = ModelFileHandler(self.callback)
        
        for directory in self.directories:
            if os.path.isdir(directory):
                observer = Observer()
                observer.schedule(handler, directory, recursive=True)
                observer.start()
                self.observers.append(observer)
                log_info(f"Monitoring started: {directory}")
            else:
                log_warning(f"Directory does not exist, skipping: {directory}")

        if not self.observers:
            log_warning("No valid directories to monitor!")

    def stop(self):
        """Stop all observers."""
        for observer in self.observers:
            observer.stop()
        for observer in self.observers:
            observer.join()
        log_info("All monitors stopped.")

    def run_forever(self):
        """Block and keep the monitor running."""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
