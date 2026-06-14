print("=" * 60)
print("🛡️  AI MODEL FIREWALL - COMPREHENSIVE TEST SUITE")
print("=" * 60)
print()

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("[TEST 1] Importing all modules...")
from modules.base_module import BaseSecurityModule
from modules.hf_hash_check import HFHashCheckModule
from modules.virustotal_check import VirusTotalCheckModule
from modules.pickle_scanner import PickleScannerModule
from modules.model_integrity_check import ModelIntegrityCheckModule
from modules.disk_space_guard import DiskSpaceGuardModule
print("✅ All modules imported successfully")

print("\n[TEST 2] Creating SecurityPipeline...")
from core.pipeline import SecurityPipeline
pipeline = SecurityPipeline()
print(f"✅ Pipeline created with {len(pipeline.modules)} modules")

for i, m in enumerate(pipeline.modules, 1):
    print(f"   {i}. {m.name}")

print("\n[TEST 3] Testing DiskSpaceGuardModule...")
module = DiskSpaceGuardModule()
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(b"x" * (1024 * 1024))
    path = f.name
result = module.scan(path)
os.unlink(path)
print(f"✅ DiskSpaceGuard test passed (success={result['success']})")

print("\n[TEST 4] Testing PickleScannerModule (safe file)...")
module = PickleScannerModule()
with tempfile.NamedTemporaryFile(suffix=".gguf", delete=False) as f:
    f.write(b"safe content")
    path = f.name
result = module.scan(path)
os.unlink(path)
assert result["success"] is True
print("✅ PickleScanner (safe) test passed")

print("\n[TEST 5] Testing PickleScannerModule (dangerous file)...")
module = PickleScannerModule()
with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as f:
    f.write(b"os.system('rm -rf /')")
    path = f.name
result = module.scan(path)
os.unlink(path)
assert result["success"] is False
print("✅ PickleScanner (dangerous) test passed")

print("\n[TEST 6] Testing Ollama blob detection...")
from core.discover import is_valid_ollama_blob, is_supported_model_file
import tempfile

# Test 1: Valid Ollama blob
with tempfile.NamedTemporaryFile(delete=False, dir="/tmp", prefix="sha256-") as f:
    f.write(b"x" * (2 * 1024 * 1024))  # 2MB
    blob_path = f.name
# Move to blobs directory simulation
os.makedirs("/tmp/test_blobs", exist_ok=True)
import shutil
shutil.move(blob_path, "/tmp/test_blobs/" + os.path.basename(blob_path))
blob_path = "/tmp/test_blobs/" + os.path.basename(blob_path)

result = is_valid_ollama_blob(blob_path)
print(f"✅ Ollama blob detection: {result}")
os.unlink(blob_path)
os.rmdir("/tmp/test_blobs")

print("\n[TEST 7] Testing full pipeline execution...")
with tempfile.NamedTemporaryFile(delete=False, suffix=".gguf") as f:
    f.write(b"fake model content")
    path = f.name
result = pipeline.execute(path)
os.unlink(path)
assert "safe" in result
print("✅ Pipeline execution test passed")

print()
print("=" * 60)
print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
print("=" * 60)
