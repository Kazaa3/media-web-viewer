#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Parser Pipeline Test
# Eingabewerte: Media files, Parser chain configuration
# Ausgabewerte: Metadata extraction results, Parser timing
# Testdateien: media/* (various formats)
# Kommentar: Testet vollständige Parser-Pipeline (Filename → Mutagen → FFmpeg → Container).
"""
Test suite for release pipeline validation.
Tests the build_system.py pipeline implementation.
"""

import sys
import subprocess
from pathlib import Path

# Project root handled by PYTHONPATH=.

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=capture_output,
        text=True,
        check=False
    )
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(f"   stdout: {result.stdout}")
        print(f"   stderr: {result.stderr}")
        return False
    return result.returncode == 0

def test_pipeline_script_exists():
    """Test that build_system.py exists and has pipeline functionality."""
    print("\n🧪 Test 1: Pipeline Script Exists")
    
    script_path = Path(__file__).parents[4] / "infra.build_system.py"
    
    if not script_path.exists():
        print("❌ build_system.py not found")
        return False
    
    # Check for pipeline functionality
    with open(script_path, 'r') as f:
        content = f.read()
        if 'def run_pipeline' not in content:
            print("❌ build_system.py does not contain run_pipeline function")
            return False
        if '--pipeline' not in content:
            print("❌ build_system.py does not support --pipeline flag")
            return False
    
    print("✅ build_system.py exists with pipeline functionality")
    return True

def test_pipeline_help():
    """Test that pipeline help is available."""
    print("\n🧪 Test 2: Pipeline Help Available")
    
    result = run_command(
        "python build_system.py --help | grep -i pipeline",
        check=False
    )
    
    if not result:
        print("❌ Pipeline help not found in build_system.py --help")
        return False
    
    print("✅ Pipeline help is available")
    return True

def test_version_sync_test_exists():
    """Test that version sync test exists (required by pipeline)."""
    print("\n🧪 Test 3: Version Sync Test Exists")
    
    test_path = Path(__file__).parents[4] / "test_version_sync.py"
    
    if not test_path.exists():
        print(f"❌ test_version_sync.py not found")
        return False
    
    print("✅ test_version_sync.py exists")
    return True

def test_reinstall_test_exists():
    """Test that reinstall test exists (required by pipeline)."""
    print("\n🧪 Test 4: Reinstall Test Exists")
    
    test_path = Path(__file__).parents[4] / "test_reinstall_deb.py"
    
    if not test_path.exists():
        print(f"❌ test_reinstall_deb.py not found")
        return False
    
    print("✅ test_reinstall_deb.py exists")
    return True

def test_build_script_exists():
    """Test that build script exists (required by pipeline)."""
    print("\n🧪 Test 5: Build Script Exists")
    
    script_path = Path(__file__).parents[4] / "build_deb.sh"
    
    if not script_path.exists():
        print("❌ build_deb.sh not found")
        return False
    
    print("✅ build_deb.sh exists")
    return True

def test_reinstall_script_exists():
    """Test that reinstall script exists (used by destructive pipeline)."""
    print("\n🧪 Test 6: Reinstall Script Exists")
    
    script_path = Path(__file__).parents[4] / "reinstall_deb.sh"
    
    if not script_path.exists():
        print("❌ reinstall_deb.sh not found")
        return False
    
    print("✅ reinstall_deb.sh exists")
    return True

def test_version_sync_config_exists():
    """Test that VERSION_SYNC.json exists (required by pipeline)."""
    print("\n🧪 Test 7: Version Sync Config Exists")
    
    config_path = Path(__file__).parents[4] / "VERSION_SYNC.json"
    
    if not config_path.exists():
        print("❌ VERSION_SYNC.json not found")
        return False
    
    print("✅ VERSION_SYNC.json exists")
    return True

def test_pipeline_info_command():
    """Test that build_system.py --info works (sanity check)."""
    print("\n🧪 Test 8: Build System Info Command")
    
    result = run_command("python build_system.py --info", check=False)
    
    if not result:
        print("❌ build_system.py --info failed")
        return False
    
    print("✅ build_system.py --info works")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Media Web Viewer - Pipeline Test Suite")
    print("=" * 60)
    
    tests = [
        test_pipeline_script_exists,
        test_pipeline_help,
        test_version_sync_test_exists,
        test_reinstall_test_exists,
        test_build_script_exists,
        test_reinstall_script_exists,
        test_version_sync_config_exists,
        test_pipeline_info_command,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✅ All pipeline infrastructure tests passed!")
        print("\nTo run the actual pipeline:")
        print("  python build_system.py --pipeline")
        print("  python build_system.py --pipeline --destructive")
        sys.exit(0)

if __name__ == "__main__":
    main()
