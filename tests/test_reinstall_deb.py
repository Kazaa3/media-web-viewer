#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for .deb package reinstallation workflow
Tests the build_deb.sh + reinstall_deb.sh pipeline
"""

import subprocess
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))


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
        sys.exit(1)
    return result


def test_version_consistency():
    """Test that VERSION file matches the version in control file."""
    print("\n🧪 Test 1: Version Consistency")
    
    # Read VERSION file
    version_path = Path(__file__).parent.parent / "VERSION"
    with open(version_path, 'r') as f:
        version = f.read().strip()
    
    # Read control file
    control_path = Path(__file__).parent.parent / "packaging" / "DEBIAN" / "control"
    with open(control_path, 'r') as f:
        control_content = f.read()
    
    # Extract version from control
    for line in control_content.split('\n'):
        if line.startswith('Version:'):
            control_version = line.split(':', 1)[1].strip()
            break
    else:
        print("❌ Version not found in control file")
        return False
    
    if version == control_version:
        print(f"✅ Version consistency OK: {version}")
        return True
    else:
        print(f"❌ Version mismatch: VERSION={version}, control={control_version}")
        return False


def test_deb_build_script_exists():
    """Test that build_deb.sh exists and is executable."""
    print("\n🧪 Test 2: Build Script Exists")
    
    script_path = Path(__file__).parent.parent / "build_deb.sh"
    
    if not script_path.exists():
        print("❌ build_deb.sh not found")
        return False
    
    if not os.access(script_path, os.X_OK):
        print("❌ build_deb.sh is not executable")
        return False
    
    print("✅ build_deb.sh exists and is executable")
    return True


def test_reinstall_script_exists():
    """Test that reinstall_deb.sh exists and is executable."""
    print("\n🧪 Test 3: Reinstall Script Exists")
    
    script_path = Path(__file__).parent.parent / "reinstall_deb.sh"
    
    if not script_path.exists():
        print("❌ reinstall_deb.sh not found")
        return False
    
    if not os.access(script_path, os.X_OK):
        print("❌ reinstall_deb.sh is not executable")
        return False
    
    print("✅ reinstall_deb.sh exists and is executable")
    return True


def test_deb_package_structure():
    """Test that the .deb package has correct structure after build."""
    print("\n🧪 Test 4: Package Structure")
    
    # Read version
    version_path = Path(__file__).parent.parent / "VERSION"
    with open(version_path, 'r') as f:
        version = f.read().strip()
    
    # Check if .deb file exists
    deb_path = Path(__file__).parent.parent / f"media-web-viewer_{version}_amd64.deb"
    
    if not deb_path.exists():
        print(f"ℹ️  .deb package not found: {deb_path.name}")
        print("   Run ./build_deb.sh to create the package first")
        return True  # Not a failure, just not built yet
    
    # Check package contents
    result = run_command(f"dpkg-deb -c {deb_path}", check=False)
    
    if result.returncode != 0:
        print("❌ Failed to inspect .deb package")
        return False
    
    # Check for essential files (DEBIAN/control not shown in dpkg-deb -c output)
    essential_files = [
        './opt/media-web-viewer/main.py',
        './opt/media-web-viewer/requirements.txt',
        './usr/bin/media-web-viewer',
    ]
    
    content = result.stdout
    missing_files = []
    
    for file in essential_files:
        if file not in content:
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files in package: {missing_files}")
        return False
    
    print(f"✅ Package structure OK: {deb_path.name}")
    return True


def test_package_installation_status():
    """Test if package is currently installed."""
    print("\n🧪 Test 5: Package Installation Status")
    
    result = run_command("dpkg -l | grep media-web-viewer", check=False)
    
    if result.returncode == 0 and "media-web-viewer" in result.stdout:
        # Extract version from dpkg output
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'media-web-viewer' in line:
                parts = line.split()
                status = parts[0]
                installed_version = parts[2] if len(parts) > 2 else "unknown"
                print(f"ℹ️  Package is installed (status: {status}, version: {installed_version})")
                return True
    
    print("ℹ️  Package is not currently installed")
    return True


def test_reinstall_script_dry_run():
    """Test reinstall script without actually running it (check syntax)."""
    print("\n🧪 Test 6: Reinstall Script Syntax")
    
    script_path = Path(__file__).parent.parent / "reinstall_deb.sh"
    
    # Use bash -n to check syntax without execution
    result = run_command(f"bash -n {script_path}", check=False)
    
    if result.returncode != 0:
        print("❌ Syntax error in reinstall_deb.sh")
        print(result.stderr)
        return False
    
    print("✅ reinstall_deb.sh syntax is valid")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Media Web Viewer - Reinstall .deb Test Suite")
    print("=" * 60)
    
    tests = [
        test_version_consistency,
        test_deb_build_script_exists,
        test_reinstall_script_exists,
        test_deb_package_structure,
        test_package_installation_status,
        test_reinstall_script_dry_run,
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
        print("\n✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
