#!/usr/bin/env python3
"""
AI Model Firewall - Main Entry Point (Test Version)
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DEFAULT_MONITOR_PATHS
from core.pipeline import SecurityPipeline
from utils.logger import log_info

def main():
    print("=" * 60)
    print("🛡️  AI MODEL FIREWALL - Test Mode")
    print("=" * 60)
    
    print("\n[1] Pipeline başlatılıyor...")
    pipeline = SecurityPipeline()
    print(f"✅ {len(pipeline.modules)} modül yüklendi")
    
    print("\n[2] Modüller:")
    for m in pipeline.modules:
        print(f"   • {m.name}")
    
    print("\n[3] Test tamamlandı!")
    print("=" * 60)

if __name__ == "__main__":
    main()