"""
Pipeline and Module Tests
"""
import os
import sys
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import SecurityPipeline


def test_pipeline_initialization():
    pipeline = SecurityPipeline()
    assert len(pipeline.modules) >= 5
    names = [m.name for m in pipeline.modules]
    assert any("Hugging Face" in n for n in names)
    assert any("VirusTotal" in n for n in names)
    assert any("Pickle" in n for n in names)
    print("✅ Pipeline initialization test passed")


def test_pipeline_runs_without_crashing():
    pipeline = SecurityPipeline()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gguf") as f:
        f.write(b"fake model content for testing")
        temp_path = f.name
    
    result = pipeline.execute(temp_path)
    os.unlink(temp_path)
    assert "safe" in result
    print("✅ Pipeline execution test passed")


def test_disk_space_module():
    from modules.disk_space_guard import DiskSpaceGuardModule
    module = DiskSpaceGuardModule()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    result = module.scan(path)
    os.unlink(path)
    assert result["success"] is True
    print("✅ Disk Space Guard test passed")


def test_pickle_scanner_safe():
    from modules.pickle_scanner import PickleScannerModule
    module = PickleScannerModule()
    with tempfile.NamedTemporaryFile(suffix=".gguf", delete=False) as f:
        f.write(b"safe content")
        path = f.name
    result = module.scan(path)
    os.unlink(path)
    assert result["success"] is True
    print("✅ Pickle Scanner (safe) test passed")


def test_pickle_scanner_dangerous():
    from modules.pickle_scanner import PickleScannerModule
    module = PickleScannerModule()
    with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as f:
        f.write(b"os.system('rm -rf /')")
        path = f.name
    result = module.scan(path)
    os.unlink(path)
    assert result["success"] is False
    print("✅ Pickle Scanner (dangerous) test passed")


if __name__ == "__main__":
    test_pipeline_initialization()
    test_pipeline_runs_without_crashing()
    test_disk_space_module()
    test_pickle_scanner_safe()
    test_pickle_scanner_dangerous()
    print("\n🎉 All tests passed!")