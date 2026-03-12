#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: DEB Reinstall Test
# Eingabewerte: .deb package
# Ausgabewerte: Installation results
# Testdateien: build/*.deb
# Kommentar: Testet DEB-Package-Reinstallation.
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

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=capture_output,
        text=True,
        check=False
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
    version_path = Path(__file__).parents[3] / "VERSION"
    with open(version_path, 'r') as f:
        version = f.read().strip()
    
    # Read control file
    control_path = Path(__file__).parents[3] / "packaging" / "DEBIAN" / "control"
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
    
    script_path = Path(__file__).parents[3] / "build_deb.sh"
    
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
    
    script_path = Path(__file__).parents[3] / "reinstall_deb.sh"
    
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
    version_path = Path(__file__).parents[3] / "VERSION"
    with open(version_path, 'r') as f:
        version = f.read().strip()
    
    # Check if .deb file exists
    deb_path = Path(__file__).parents[3] / f"media-web-viewer_{version}_amd64.deb"
    
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

def test_installed_version_matches_current_build():
    """Test that installed package version matches VERSION file exactly."""
    print("\n🧪 Test 6: Installed Version Matches Current Build")

    version_path = Path(__file__).parents[3] / "VERSION"
    with open(version_path, 'r') as f:
        expected_version = f.read().strip()

    result = run_command(
        "dpkg-query -W -f='${Status} ${Version}\\n' media-web-viewer",
        check=False

    strict_mode = os.getenv("STRICT_PACKAGE_VERSION", "0") == "1"

    if result.returncode != 0:
        print("ℹ️  Package media-web-viewer is not installed")
        print("   Run ./reinstall_deb.sh to purge old package and install current build")
        return not strict_mode

    output = result.stdout.strip()
    parts = output.split()

    if len(parts) < 4:
        print(f"❌ Unexpected dpkg-query output: {output}")
        return False

    installed_state = " ".join(parts[:3])
    installed_version = parts[3]

    if installed_state != "install ok installed":
        print(f"❌ Package state is not fully installed: {installed_state}")
        return False

    if installed_version != expected_version:
        print(
            f"⚠️  Installed version mismatch: installed={installed_version}, "
            f"expected={expected_version}"
        print("   Run ./reinstall_deb.sh to purge old package and install current build")
        return not strict_mode

    print(f"✅ Installed version matches current build: {installed_version}")
    return True

def test_destructive_reinstall_e2e_optional():
    """Optionally run full purge+install flow when explicitly enabled."""
    print("\n🧪 Test 7: Destructive Reinstall E2E (optional)")

    if os.getenv("RUN_DESTRUCTIVE_TESTS", "0") != "1":
        print("ℹ️  Skipped (set RUN_DESTRUCTIVE_TESTS=1 to enable)")
        return True

    project_root = Path(__file__).parents[3]
    reinstall_script = project_root / "reinstall_deb.sh"

    if not reinstall_script.exists():
        print("❌ reinstall_deb.sh not found")
        return False

    print("⚠️  Running destructive reinstall via reinstall_deb.sh...")
    result = run_command(f"{reinstall_script}", check=False)

    if result.returncode != 0:
        print("❌ reinstall_deb.sh failed")
        print("   stdout:")
        print(result.stdout)
        print("   stderr:")
        print(result.stderr)
        return False

    version_path = project_root / "VERSION"
    with open(version_path, 'r') as f:
        expected_version = f.read().strip()

    verify_result = run_command(
        "dpkg-query -W -f='${Status} ${Version}\\n' media-web-viewer",
        check=False

    if verify_result.returncode != 0:
        print("❌ Package media-web-viewer not installed after reinstall")
        return False

    output = verify_result.stdout.strip().split()
    if len(output) < 4:
        print(f"❌ Unexpected dpkg-query output after reinstall: {verify_result.stdout.strip()}")
        return False

    installed_state = " ".join(output[:3])
    installed_version = output[3]

    if installed_state != "install ok installed" or installed_version != expected_version:
        print(
            f"❌ Reinstall verification failed: state={installed_state}, "
            f"version={installed_version}, expected={expected_version}"
        return False

    print(f"✅ Destructive reinstall successful: {installed_version}")
    return True

def test_reinstall_script_dry_run():
    """Test reinstall script without actually running it (check syntax)."""
    print("\n🧪 Test 8: Reinstall Script Syntax")
    
    script_path = Path(__file__).parents[3] / "reinstall_deb.sh"
    
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
        test_installed_version_matches_current_build,
        test_destructive_reinstall_e2e_optional,
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
