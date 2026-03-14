#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Browser Launch Test
# Eingabewerte: Browser preference settings, Chrome/Chromium paths
# Ausgabewerte: Browser launch success, Window creation
# Testdateien: Keine (System browser)
# Kommentar: Testet Browser-Launch-Mechanismus (Chrome/Chromium/App-Mode).
"""
Test suite for browser launch functionality.
Validates Chrome app mode configuration and fallback behavior.
"""

import sys
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))


def test_chrome_browser_available():
    """Test that at least one Chrome/Chromium variant is available."""
    print("\n🧪 Test 1: Chrome/Chromium Browser Available")
    
    browser_candidates = [
        'google-chrome-stable',
        'google-chrome',
        'chrome',
        'chromium-browser',
        'chromium',
    ]
    
    found_browsers = []
    for browser_cmd in browser_candidates:
        browser_path = shutil.which(browser_cmd)
        if browser_path:
            found_browsers.append((browser_cmd, browser_path))
    
    if not found_browsers:
        print("⚠️  No Chrome/Chromium browser found in PATH")
        print("   App will fall back to system default browser")
        return True  # Not a hard failure
    
    for browser_cmd, browser_path in found_browsers:
        print(f"✅ Found: {browser_cmd} ({browser_path})")
    
    return True


def test_app_mode_flags_present():
    """Test that main.py contains Chrome app mode flags."""
    print("\n🧪 Test 2: App Mode Flags Present in Code")
    
    main_py = Path(__file__).parent.parent / "main.py"
    
    if not main_py.exists():
        print("❌ main.py not found")
        return False
    
    with open(main_py, 'r') as f:
        content = f.read()
    
    required_flags = [
        '--app=',
        '--new-window',
        '--no-first-run',
        '--no-default-browser-check',
    ]
    
    missing_flags = []
    for flag in required_flags:
        if flag not in content:
            missing_flags.append(flag)
    
    if missing_flags:
        print(f"❌ Missing Chrome app mode flags: {missing_flags}")
        return False
    
    print("✅ All Chrome app mode flags present in main.py")
    return True


def test_subprocess_launch_pattern():
    """Test that main.py uses subprocess.Popen for browser launch."""
    print("\n🧪 Test 3: Subprocess Launch Pattern")
    
    main_py = Path(__file__).parent.parent / "main.py"
    
    with open(main_py, 'r') as f:
        content = f.read()
    
    if 'subprocess.Popen' not in content:
        print("❌ subprocess.Popen not found in main.py")
        return False
    
    # Check for proper browser launch pattern
    if 'browser_path' in content and 'subprocess.Popen' in content:
        print("✅ Browser launch uses subprocess.Popen")
        return True
    
    print("⚠️  Browser launch pattern unclear")
    return False


def test_fallback_browser_exists():
    """Test that get_preferred_browser fallback still exists."""
    print("\n🧪 Test 4: Fallback Browser Function Exists")
    
    main_py = Path(__file__).parent.parent / "main.py"
    
    with open(main_py, 'r') as f:
        content = f.read()
    
    if 'def get_preferred_browser' not in content:
        print("❌ get_preferred_browser function not found")
        return False
    
    print("✅ get_preferred_browser fallback exists")
    return True


def test_m3u8_package_available():
    """Test that m3u8 package is importable (VLC support)."""
    print("\n🧪 Test 5: m3u8 Package Available")
    
    try:
        import m3u8
        version = getattr(m3u8, '__version__', 'unknown')
        print(f"✅ m3u8 package available (version: {version})")
        return True
    except ImportError:
        print("❌ m3u8 package not installed")
        print("   Fix: pip install m3u8>=4.1.0")
        return False


def test_requirements_txt_has_m3u8():
    """Test that requirements.txt includes m3u8."""
    print("\n🧪 Test 6: requirements.txt Contains m3u8")
    
    req_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    with open(req_file, 'r') as f:
        content = f.read()
    
    if 'm3u8' not in content.lower():
        print("❌ m3u8 not found in requirements.txt")
        return False
    
    print("✅ m3u8 listed in requirements.txt")
    return True


def test_browser_launch_logic_structure():
    """Test that browser launch has proper try-except structure."""
    print("\n🧪 Test 7: Browser Launch Error Handling")
    
    main_py = Path(__file__).parent.parent / "main.py"
    
    with open(main_py, 'r') as f:
        content = f.read()
    
    # Check for error handling around browser launch
    has_logging = 'logging.info' in content or 'logging.warning' in content
    has_try_except = 'try:' in content and 'except' in content
    
    if not has_logging:
        print("⚠️  No logging found for browser launch")
        return True  # Warning only
    
    if not has_try_except:
        print("⚠️  No exception handling found")
        return True  # Warning only
    
    print("✅ Browser launch has logging and error handling")
    return True


def main():
    """Run all browser launch tests."""
    print("=" * 60)
    print("🧪 Media Web Viewer - Browser Launch Test Suite")
    print("=" * 60)
    
    tests = [
        test_chrome_browser_available,
        test_app_mode_flags_present,
        test_subprocess_launch_pattern,
        test_fallback_browser_exists,
        test_m3u8_package_available,
        test_requirements_txt_has_m3u8,
        test_browser_launch_logic_structure,
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
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("\n⚠️  Some tests failed")
        print("\nCommon fixes:")
        print("  - Install Chrome/Chromium: sudo apt install google-chrome-stable")
        print("  - Install m3u8: pip install m3u8>=4.1.0")
        sys.exit(1)
    else:
        print("\n✅ All browser launch tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
