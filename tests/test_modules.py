"""
Additional module-specific tests
"""

import tempfile
import os
import pytest
from modules.pickle_scanner import PickleScannerModule
from modules.disk_space_guard import DiskSpaceGuardModule


def test_pickle_scanner_safe_file():
    module = PickleScannerModule()
    with tempfile.NamedTemporaryFile(suffix=".gguf", delete=False) as f:
        f.write(b"safe content")
        path = f.name
    
    result = module.scan(path)
    os.unlink(path)
    assert result["success"] is True


def test_pickle_scanner_dangerous_file():
    module = PickleScannerModule()
    with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as f:
        f.write(b"os.system('rm -rf /')")
        path = f.name
    
    result = module.scan(path)
    os.unlink(path)
    assert result["success"] is False


def test_disk_space_guard():
    module = DiskSpaceGuardModule()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    
    result = module.scan(path)
    os.unlink(path)
    assert "success" in result
