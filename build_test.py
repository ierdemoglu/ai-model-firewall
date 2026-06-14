#!/usr/bin/env python3
"""
Build Test Script - Tests all platform build scripts
"""
import sys
import subprocess
from pathlib import Path

def test_build_script(script_name, platform_name):
    print(f"\n{'='*60}")
    print(f"Testing {platform_name} Build Script")
    print(f"{'='*60}")
    
    script_path = Path(script_name)
    if not script_path.exists():
        print(f"❌ {script_name} not found!")
        return False
    
    try:
        # Run the build script
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Check if dist folder was created
        dist_path = Path("dist")
        if dist_path.exists():
            files = list(dist_path.glob("*"))
            print(f"\n📁 Files created in dist/:")
            for f in files:
                print(f"   • {f.name}")
            return True
        else:
            print("⚠️  No dist/ folder created")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 AI Model Firewall - Build System Test")
    print("="*60)
    
    results = {}
    
    # Test each platform
    results["Windows"] = test_build_script("build_windows.py", "Windows")
    results["macOS"] = test_build_script("build_macos.py", "macOS")
    results["Linux"] = test_build_script("build_linux.py", "Linux")
    
    # Summary
    print(f"\n{'='*60}")
    print("BUILD TEST SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for platform, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{platform:15} {status}")
        if not passed:
            all_passed = False
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL BUILD SCRIPTS WORKING!")
    else:
        print("⚠️  Some build scripts need attention")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
