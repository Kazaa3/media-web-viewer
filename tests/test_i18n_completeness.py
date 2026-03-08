#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for i18n (internationalization) completeness and correctness.
Validates that all UI strings are properly translated and no hardcoded text exists.
"""

import sys
import json
import re
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))


def test_i18n_json_structure():
    """Test that i18n.json has valid structure with de/en keys."""
    print("\n🧪 Test 1: i18n.json Structure")
    
    i18n_file = Path(__file__).parent.parent / "web" / "i18n.json"
    
    if not i18n_file.exists():
        print("❌ i18n.json not found")
        return False
    
    with open(i18n_file, 'r', encoding='utf-8') as f:
        try:
            i18n_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False
    
    if 'de' not in i18n_data or 'en' not in i18n_data:
        print("❌ Missing 'de' or 'en' keys in i18n.json")
        return False
    
    print(f"✅ Valid structure with {len(i18n_data['de'])} German and {len(i18n_data['en'])} English keys")
    return True


def test_i18n_key_parity():
    """Test that German and English have the same keys."""
    print("\n🧪 Test 2: German/English Key Parity")
    
    i18n_file = Path(__file__).parent.parent / "web" / "i18n.json"
    
    with open(i18n_file, 'r', encoding='utf-8') as f:
        i18n_data = json.load(f)
    
    de_keys = set(i18n_data['de'].keys())
    en_keys = set(i18n_data['en'].keys())
    
    missing_in_en = de_keys - en_keys
    missing_in_de = en_keys - de_keys
    
    if missing_in_en:
        print(f"❌ Missing in English: {missing_in_en}")
        return False
    
    if missing_in_de:
        print(f"❌ Missing in German: {missing_in_de}")
        return False
    
    print(f"✅ All {len(de_keys)} keys present in both languages")
    return True


def test_required_i18n_keys_present():
    """Test that all required i18n keys are present."""
    print("\n🧪 Test 3: Required i18n Keys Present")
    
    i18n_file = Path(__file__).parent.parent / "web" / "i18n.json"
    
    with open(i18n_file, 'r', encoding='utf-8') as f:
        i18n_data = json.load(f)
    
    required_keys = [
        'test_loading',
        'parser_no_options',
        'lib_no_media_desc',
        'logbook_saved',
        'logbook_deleted',
        'logbook_error',
        'parser_filename',
        'parser_container',
        'parser_mutagen',
        'parser_pymediainfo',
        'parser_ffmpeg',
    ]
    
    missing_keys = []
    for key in required_keys:
        if key not in i18n_data['de'] or key not in i18n_data['en']:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing required keys: {missing_keys}")
        return False
    
    print(f"✅ All {len(required_keys)} required keys present")
    return True


def test_no_hardcoded_german_strings():
    """Test that app.html doesn't contain hardcoded German strings."""
    print("\n🧪 Test 4: No Hardcoded German Strings")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patterns that should NOT appear (hardcoded German without i18n)
    forbidden_patterns = [
        (r'innerHTML\s*=\s*[\'"].*Lade Tests\.\.\.', 'Lade Tests...'),
        (r'innerHTML\s*=\s*[\'"].*Keine Medien in der Bibliothek\.', 'Keine Medien in der Bibliothek'),
        (r'Keine spezifischen Optionen für.*verfügbar', 'Keine spezifischen Optionen'),
    ]
    
    found_issues = []
    for pattern, description in forbidden_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Check if it's actually using i18n
            for match in matches:
                if 'data-i18n' not in match and 't(' not in match and '${t(' not in match:
                    found_issues.append(f"{description}: {match[:100]}")
    
    if found_issues:
        print("❌ Found hardcoded German strings:")
        for issue in found_issues:
            print(f"   - {issue}")
        return False
    
    print("✅ No hardcoded German strings found")
    return True


def test_no_i18n_function_calls():
    """Test that app.html uses t() instead of i18n()."""
    print("\n🧪 Test 5: No i18n() Function Calls")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find i18n( function calls (should be t() instead)
    i18n_calls = re.findall(r'\bi18n\s*\(', content)
    
    if i18n_calls:
        print(f"❌ Found {len(i18n_calls)} i18n() function calls (should be t())")
        # Find line numbers
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(r'\bi18n\s*\(', line):
                print(f"   Line {i}: {line.strip()[:80]}")
        return False
    
    print("✅ No i18n() function calls found (all use t())")
    return True


def test_eel_expose_on_scan_media():
    """Test that scan_media function has @eel.expose decorator."""
    print("\n🧪 Test 6: scan_media @eel.expose Decorator")
    
    main_py = Path(__file__).parent.parent / "main.py"
    
    with open(main_py, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find scan_media function definition
    scan_media_match = re.search(r'def scan_media\s*\(', content)
    if not scan_media_match:
        print("❌ scan_media function not found")
        return False
    
    # Check if @eel.expose appears before it
    pos = scan_media_match.start()
    lines_before = content[:pos].split('\n')[-20:]  # Last 20 lines before function
    
    has_expose = any('@eel.expose' in line for line in lines_before)
    
    if not has_expose:
        print("❌ scan_media function missing @eel.expose decorator")
        return False
    
    print("✅ scan_media has @eel.expose decorator")
    return True


def test_data_i18n_attributes():
    """Test that data-i18n attributes reference existing keys."""
    print("\n🧪 Test 7: data-i18n Attributes Reference Valid Keys")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    i18n_file = Path(__file__).parent.parent / "web" / "i18n.json"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(i18n_file, 'r', encoding='utf-8') as f:
        i18n_data = json.load(f)
    
    de_keys = set(i18n_data['de'].keys())
    
    # Find all data-i18n attributes
    i18n_attrs = re.findall(r'data-i18n="([^"]+)"', html_content)
    
    invalid_keys = []
    for key in i18n_attrs:
        # Handle special syntax like [placeholder]key_name for input/textarea placeholders
        actual_key = key
        if key.startswith('['):
            # Extract key after ']'
            match = re.match(r'\[.*?\](.+)', key)
            if match:
                actual_key = match.group(1)
            else:
                continue  # Skip malformed attributes
        
        if actual_key not in de_keys:
            invalid_keys.append(key)
    
    if invalid_keys:
        print(f"❌ Found {len(invalid_keys)} invalid data-i18n keys:")
        for key in set(invalid_keys):
            print(f"   - {key}")
        return False
    
    print(f"✅ All {len(set(i18n_attrs))} unique data-i18n attributes are valid")
    return True


def test_t_function_calls_valid():
    """Test that t() function calls reference existing i18n keys."""
    print("\n🧪 Test 8: t() Function Calls Reference Valid Keys")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    i18n_file = Path(__file__).parent.parent / "web" / "i18n.json"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(i18n_file, 'r', encoding='utf-8') as f:
        i18n_data = json.load(f)
    
    de_keys = set(i18n_data['de'].keys())
    
    # Find all t('key') and t("key") calls - must have word boundary or specific chars before 't'
    # This avoids matching createElement('div') and similar
    # Match: \bt\( or [^a-zA-Z]t\( to ensure it's the t() function
    t_calls = re.findall(r"(?:\b|[^a-zA-Z])t\(['\"]([a-z_][a-z0-9_]*)['\"]\)", html_content, re.IGNORECASE)
    
    invalid_keys = []
    for key in t_calls:
        if key not in de_keys:
            invalid_keys.append(key)
    
    if invalid_keys:
        print(f"❌ Found {len(set(invalid_keys))} invalid t() keys:")
        for key in sorted(set(invalid_keys)):
            print(f"   - {key}")
        return False
    
    print(f"✅ All {len(set(t_calls))} unique t() calls are valid")
    return True


def main():
    """Run all i18n completeness tests."""
    print("=" * 60)
    print("🧪 Media Web Viewer - i18n Completeness Test Suite")
    print("=" * 60)
    
    tests = [
        test_i18n_json_structure,
        test_i18n_key_parity,
        test_required_i18n_keys_present,
        test_no_hardcoded_german_strings,
        test_no_i18n_function_calls,
        test_eel_expose_on_scan_media,
        test_data_i18n_attributes,
        test_t_function_calls_valid,
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
        print("  - Add missing i18n keys to web/i18n.json")
        print("  - Replace hardcoded strings with t() calls")
        print("  - Change i18n() to t() in JavaScript")
        print("  - Add @eel.expose to backend functions")
        sys.exit(1)
    else:
        print("\n✅ All i18n tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
