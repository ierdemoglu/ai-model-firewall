#!/usr/bin/env python3
"""
AI Model Firewall - Main Entry Point
Scans existing models on startup + monitors for new files
"""
import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DEFAULT_MONITOR_PATHS, QUARANTINE_DIR
from core.discover import discover_model_directories, scan_existing_models, get_all_model_files
from core.monitor import DirectoryMonitor
from core.pipeline import SecurityPipeline
from utils.notifier import notify_scan_started, notify_safe, notify_blocked, notify_quarantined
from utils.logger import log_info, log_error
from modules.updater import SimpleUpdater
from utils.updater_gui import check_and_show_update


def handle_new_model(file_path: str):
    """Callback for new model files detected by watchdog."""
    filename = os.path.basename(file_path)
    log_info(f"Processing new model: {filename}")
    notify_scan_started(filename)

    pipeline = SecurityPipeline()
    result = pipeline.execute(file_path)

    if result["safe"]:
        notify_safe(filename)
        log_info(f"✅ Model approved: {filename}")
    else:
        reason = result.get("reason", "Unknown reason")
        module = result.get("module", "Unknown Module")
        notify_blocked(filename, reason, module)
        log_info(f"❌ Model BLOCKED: {filename} | Module: {module} | Reason: {reason}")

        try:
            quarantine_path = os.path.join(QUARANTINE_DIR, filename)
            if os.path.exists(quarantine_path):
                base, ext = os.path.splitext(filename)
                quarantine_path = os.path.join(QUARANTINE_DIR, f"{base}_{int(time.time())}{ext}")
            os.rename(file_path, quarantine_path)
            notify_quarantined(filename)
            log_info(f"File moved to quarantine: {quarantine_path}")
        except Exception as e:
            log_error(f"Failed to quarantine file: {e}")


def scan_existing_models_on_startup(directories: list):
    """
    Scan ALL existing model files when the firewall starts.
    This catches models that were downloaded before the firewall was running.
    """
    log_info("=" * 50)
    log_info("SCANNING EXISTING MODELS ON STARTUP")
    log_info("=" * 50)
    
    total_scanned = 0
    total_blocked = 0
    
    for directory in directories:
        if not os.path.isdir(directory):
            continue
            
        log_info(f"Scanning directory: {directory}")
        models = get_all_model_files(directory)
        
        if not models:
            log_info(f"  No models found in {directory}")
            continue
            
        log_info(f"  Found {len(models)} model(s) in {directory}")
        
        pipeline = SecurityPipeline()
        
        for model_path in models:
            filename = os.path.basename(model_path)
            total_scanned += 1
            
            log_info(f"  → Scanning: {filename}")
            result = pipeline.execute(model_path)
            
            if result["safe"]:
                log_info(f"    ✅ SAFE: {filename}")
            else:
                total_blocked += 1
                reason = result.get("reason", "Unknown")
                module = result.get("module", "Unknown")
                log_info(f"    ❌ BLOCKED: {filename} | {module}: {reason}")
                
                try:
                    quarantine_path = os.path.join(QUARANTINE_DIR, filename)
                    if os.path.exists(quarantine_path):
                        base, ext = os.path.splitext(filename)
                        quarantine_path = os.path.join(QUARANTINE_DIR, f"{base}_{int(time.time())}{ext}")
                    os.rename(model_path, quarantine_path)
                    log_info(f"    📦 Moved to quarantine: {quarantine_path}")
                except Exception as e:
                    log_error(f"    Failed to quarantine: {e}")
    
    log_info("=" * 50)
    log_info(f"STARTUP SCAN COMPLETE")
    log_info(f"Total models scanned: {total_scanned}")
    log_info(f"Total models blocked: {total_blocked}")
    log_info("=" * 50)


def main():
    print("=" * 70)
    print("🛡️  AI MODEL FIREWALL - Model Security Firewall")
    print("=" * 70)
    print("Modular, Event-Driven and extensible security system starting...\n")

    # Step 1: Check for updates
    print("[1/5] Checking for updates...")
    updater = SimpleUpdater()
    check_and_show_update(updater)

    # Step 2: Discover model directories
    print("\n[2/5] Discovering model directories...")
    discovered = discover_model_directories()
    monitor_paths = list(set(discovered + [p for p in DEFAULT_MONITOR_PATHS if os.path.isdir(os.path.expanduser(p))]))

    if not monitor_paths:
        print("⚠️  No model directories found. Using default paths.")
        monitor_paths = [os.path.expanduser(p) for p in DEFAULT_MONITOR_PATHS if os.path.isdir(os.path.expanduser(p))]

    print(f"Monitoring {len(monitor_paths)} directories:")
    for path in monitor_paths:
        print(f"  • {path}")

    # Step 3: Scan existing models (IMPORTANT - this was missing before)
    print("\n[3/5] 🔍 SCANNING EXISTING MODELS (Ollama, LM Studio, HuggingFace)...")
    print("This may take a moment for large model collections...")
    scan_existing_models_on_startup(monitor_paths)

    # Step 4: Initialize pipeline
    print("\n[4/5] Loading security modules...")
    pipeline = SecurityPipeline()

    # Step 5: Start file system monitor for NEW files
    print("\n[5/5] Starting file system monitor for new downloads...")
    monitor = DirectoryMonitor(monitor_paths, handle_new_model)
    monitor.start()

    print("\n" + "=" * 70)
    print("✅ AI Model Firewall is ACTIVE")
    print("   ✓ Existing models scanned on startup")
    print("   ✓ New downloads will be monitored in real-time")
    print("   Press Ctrl+C to exit.")
    print("=" * 70 + "\n")

    try:
        monitor.run_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user. Shutting down...")
        monitor.stop()
        print("Goodbye! 👋")


if __name__ == "__main__":
    main()
