"""
AI Model Firewall - Comprehensive Test Suite
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import SecurityPipeline


def test_1_pipeline_initialization():
    """Test 1: Pipeline loads all 5 modules"""
    pipeline = SecurityPipeline()
    assert len(pipeline.modules) == 5, f"Expected 5 modules, got {len(pipeline.modules)}"
    
    names = [m.name for m in pipeline.modules]
    expected = ["Disk Alanı", "Hugging Face", "VirusTotal", "Pickle", "Model Bütünlük"]
    
    for exp in expected:
        assert any(exp in name for name in names), f"Module containing '{exp}' not found"
    
    print("✅ TEST 1 PASSED: Pipeline initialization - 5 modules loaded correctly")


def test_2_pipeline_execution():
    """Test 2: Pipeline runs without crashing on valid file"""
    pipeline = SecurityPipeline()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gguf") as f:
        f.write(b"fake model content for testing")
        temp_path = f.name
    
    result = pipeline.execute(temp_path)
    os.unlink(temp_path)
    
    assert "safe" in result
    print("✅ TEST 2 PASSED: Pipeline execution works without crashing")


def test_3_disk_space_guard():
    """Test 3: Disk Space Guard module"""
    from modules.disk_space_guard import DiskSpaceGuardModule
    module = DiskSpaceGuardModule()
    
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    
    result = module.scan(path)
    os.unlink(path)
    
    assert result["success"] is True
    print("✅ TEST 3 PASSED: DiskSpaceGuard works correctly")


def test_4_pickle_scanner_safe():
    """Test 4: Pickle Scanner - safe file"""
    from modules.pickle_scanner import PickleScannerModule
    module = PickleScannerModule()
    
    with tempfile.NamedTemporaryFile(suffix=".gguf", delete=False) as f:
        f.write(b"safe content")
        path = f.name
    
    result = module.scan(path)
    os.unlink(path)
    
    assert result["success"] is True
    print("✅ TEST 4 PASSED: PickleScanner correctly identifies safe files")


def test_5_pickle_scanner_dangerous():
    """Test 5: Pickle Scanner - dangerous file"""
    from modules.pickle_scanner import PickleScannerModule
    module = PickleScannerModule()
    
    with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as f:
        f.write(b"os.system('rm -rf /')")
        path = f.name
    
    result = module.scan(path)
    os.unlink(path)
    
    assert result["success"] is False
    print("✅ TEST 5 PASSED: PickleScanner correctly detects dangerous files")


def test_6_all_modules_have_scan_method():
    """Test 6: All modules have required scan method"""
    pipeline = SecurityPipeline()
    
    for module in pipeline.modules:
        assert hasattr(module, 'scan'), f"{module.name} missing scan method"
        assert hasattr(module, 'name'), f"{module.name} missing name property"
    
    print("✅ TEST 6 PASSED: All modules have required interface")


if __name__ == "__main__":
    print("=" * 60)
    print("🛡️  AI MODEL FIREWALL - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()
    
    test_1_pipeline_initialization()
    test_2_pipeline_execution()
    test_3_disk_space_guard()
    test_4_pickle_scanner_safe()
    test_5_pickle_scanner_dangerous()
    test_6_all_modules_have_scan_method()
    
    print()
    print("=" * 60)
    print("🎉 ALL 6 TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)