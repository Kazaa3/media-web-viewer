#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Dictionary Operations Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
Unit Test / Dictionary Operations

ZWECK:
------
Validiert alle Dictionary-Operationen für Metadaten-Tags.
Prüft JSON-Serialisierung, Deserialisierung, Merge-Operationen und Datenintegrität.

EINGABEWERTE:
-------------
- Tag-Dictionaries (artist, title, album, etc.)
- JSON-Strings
- Nested Dictionaries (_parser_times, chapters)

AUSGABEWERTE:
-------------
- Serialisierte JSON-Strings
- Deserialisierte Dictionaries
- Merged Dictionaries
- Validierungsergebnisse

TESTDATEIEN:
------------
- Keine spezifischen Dateien erforderlich
- Arbeitet mit In-Memory-Dictionaries

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste Deep-Copy vs Shallow-Copy
- [ ] Teste Dictionary-Diff-Operationen
- [ ] Teste Unicode und Sonderzeichen in Keys/Values
- [ ] Teste sehr große Dictionaries (Performance)
- [ ] Teste Circular-Reference-Handling
- [ ] Teste Schema-Validierung (required fields)
- [ ] Teste Type-Safety (str vs int vs float)
- [ ] Füge pytest-Struktur hinzu mit parametrize

VERWENDUNG:
-----------
    python tests/check_dict.py
"""

import sys
import json
from copy import deepcopy


def test_json_serialization():
    """
    @brief Test JSON serialization/deserialization of tag dictionaries.
    @details Validates that tags can be safely converted to/from JSON.
    """
    print("\n🔄 Test 1: JSON Serialization/Deserialization")
    print("─" * 60)
    
    test_dict = {
        'artist': 'Test Artist',
        'title': 'Test Title',
        'album': 'Test Album',
        'year': '2024',
        'track': '3',
        'genre': 'Rock',
        'bitrate': '320 kbps',
        'has_art': True,
    }
    
    try:
        # Serialize to JSON
        json_str = json.dumps(test_dict)
        print(f"✅ Serialization erfolgreich: {len(json_str)} Zeichen")
        
        # Deserialize back
        recovered_dict = json.loads(json_str)
        
        # Verify all keys are preserved
        if set(test_dict.keys()) == set(recovered_dict.keys()):
            print("✅ Alle Keys erhalten geblieben")
        else:
            print("❌ Keys unterschiedlich nach Deserialisierung")
            return False
        
        # Verify values
        all_match = True
        for key, value in test_dict.items():
            if recovered_dict[key] != value:
                print(f"❌ Wert für '{key}' unterschiedlich: {value} != {recovered_dict[key]}")
                all_match = False
        
        if all_match:
            print("✅ Alle Values identisch")
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ Fehler bei JSON-Serialisierung: {e}")
        return False


def test_nested_dict_serialization():
    """
    @brief Test serialization of nested dictionaries (_parser_times, chapters).
    @details Validates complex nested structures can be serialized.
    """
    print("\n🗂️  Test 2: Nested Dictionary Serialization")
    print("─" * 60)
    
    test_dict = {
        'title': 'Test Audiobook',
        'artist': 'Test Author',
        '_parser_times': {
            'filename': 0.001,
            'mutagen': 0.045,
            'ffmpeg': 0.000
        },
        'chapters': [
            {'start': 0, 'title': 'Chapter 1'},
            {'start': 120, 'title': 'Chapter 2'},
            {'start': 300, 'title': 'Chapter 3'}
        ]
    }
    
    try:
        # Serialize
        json_str = json.dumps(test_dict)
        print(f"✅ Nested Dict serialisiert: {len(json_str)} Zeichen")
        
        # Deserialize
        recovered = json.loads(json_str)
        
        # Verify nested dict
        if '_parser_times' in recovered and isinstance(recovered['_parser_times'], dict):
            print("✅ Nested Dict '_parser_times' erhalten")
        else:
            print("❌ Nested Dict '_parser_times' fehlt oder falsch")
            return False
        
        # Verify array
        if 'chapters' in recovered and isinstance(recovered['chapters'], list):
            if len(recovered['chapters']) == 3:
                print(f"✅ Array 'chapters' erhalten ({len(recovered['chapters'])} Einträge)")
            else:
                print(f"❌ Array 'chapters' hat falsche Länge: {len(recovered['chapters'])}")
                return False
        else:
            print("❌ Array 'chapters' fehlt oder falsch")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Nested-Serialisierung: {e}")
        return False


def test_dict_merge():
    """
    @brief Test merging dictionaries (update operations).
    @details Validates that tags can be updated without losing data.
    """
    print("\n🔀 Test 3: Dictionary Merge Operations")
    print("─" * 60)
    
    original = {
        'artist': 'Original Artist',
        'title': 'Original Title',
        'album': 'Original Album',
        'year': '2023',
        '_parser_times': {
            'filename': 0.001,
            'mutagen': 0.045
        }
    }
    
    updates = {
        'artist': 'Updated Artist',
        'album': 'Updated Album',
        'genre': 'Rock'  # New field
    }
    
    try:
        # Simulate update (like in saveTags)
        merged = deepcopy(original)
        merged.update(updates)
        
        # Verify updates applied
        if merged['artist'] == 'Updated Artist':
            print("✅ Update für 'artist' angewendet")
        else:
            print("❌ Update für 'artist' fehlgeschlagen")
            return False
        
        # Verify new fields added
        if 'genre' in merged and merged['genre'] == 'Rock':
            print("✅ Neues Feld 'genre' hinzugefügt")
        else:
            print("❌ Neues Feld 'genre' fehlt")
            return False
        
        # Verify untouched fields preserved
        if merged['title'] == 'Original Title':
            print("✅ Unveränderte Felder erhalten")
        else:
            print("❌ Unveränderte Felder wurden überschrieben")
            return False
        
        # Verify nested dict preserved
        if '_parser_times' in merged and isinstance(merged['_parser_times'], dict):
            print("✅ Nested Dict '_parser_times' erhalten nach Merge")
        else:
            print("❌ Nested Dict '_parser_times' verloren nach Merge")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Dict-Merge: {e}")
        return False


def test_dict_key_operations():
    """
    @brief Test dictionary key operations (get, has, delete).
    @details Validates safe key access patterns.
    """
    print("\n🔑 Test 4: Dictionary Key Operations")
    print("─" * 60)
    
    test_dict = {
        'artist': 'Test Artist',
        'title': 'Test Title',
    }
    
    try:
        # Test get with default
        album = test_dict.get('album', 'Unknown Album')
        if album == 'Unknown Album':
            print("✅ get() mit Default funktioniert")
        else:
            print(f"❌ get() liefert falschen Wert: {album}")
            return False
        
        # Test key existence
        if 'artist' in test_dict:
            print("✅ 'in' Operator funktioniert")
        else:
            print("❌ 'in' Operator fehlgeschlagen")
            return False
        
        # Test missing key
        if 'nonexistent' not in test_dict:
            print("✅ Fehlende Keys korrekt erkannt")
        else:
            print("❌ Fehlende Keys nicht erkannt")
            return False
        
        # Test pop with default
        genre = test_dict.pop('genre', 'Pop')
        if genre == 'Pop' and 'genre' not in test_dict:
            print("✅ pop() mit Default funktioniert")
        else:
            print("❌ pop() fehlgeschlagen")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Key-Operationen: {e}")
        return False


def test_dict_copy():
    """
    @brief Test dictionary copy operations (shallow vs deep).
    @details Validates that nested structures are properly copied.
    """
    print("\n📋 Test 5: Dictionary Copy Operations")
    print("─" * 60)
    
    original = {
        'artist': 'Original',
        '_parser_times': {
            'mutagen': 0.045
        }
    }
    
    try:
        # Deep copy
        deep = deepcopy(original)
        deep['artist'] = 'Modified'
        deep['_parser_times']['mutagen'] = 0.999
        
        # Verify original unchanged
        if original['artist'] == 'Original':
            print("✅ Deep Copy: Original nicht verändert")
        else:
            print("❌ Deep Copy: Original wurde verändert")
            return False
        
        if original['_parser_times']['mutagen'] == 0.045:
            print("✅ Deep Copy: Nested Dict im Original nicht verändert")
        else:
            print("❌ Deep Copy: Nested Dict im Original wurde verändert")
            return False
        
        # Shallow copy (dict() or .copy())
        shallow = original.copy()
        shallow['artist'] = 'Shallow Modified'
        
        if original['artist'] == 'Original':
            print("✅ Shallow Copy: Top-Level nicht verändert")
        else:
            print("❌ Shallow Copy: Top-Level wurde verändert")
            return False
        
        # Test shallow copy limitation
        shallow['_parser_times']['mutagen'] = 0.888
        if original['_parser_times']['mutagen'] == 0.888:
            print("⚠️  Shallow Copy: Nested Dict IST shared (erwartetes Verhalten)")
        else:
            print("❌ Shallow Copy: Unerwartet - Nested Dict wurde nicht geteilt")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Copy-Operationen: {e}")
        return False


def test_unicode_and_special_chars():
    """
    @brief Test Unicode and special characters in dictionaries.
    @details Validates international text and special characters.
    """
    print("\n🌍 Test 6: Unicode & Special Characters")
    print("─" * 60)
    
    test_dict = {
        'artist': 'Björk',
        'title': 'Ænima',
        'album': 'München – Der Süden',
        'comment': '日本語 • Deutsch • Español',
        'genre': 'Rock/Pop & Jazz',
    }
    
    try:
        # Serialize to JSON
        json_str = json.dumps(test_dict, ensure_ascii=False)
        print(f"✅ Unicode serialisiert: {len(json_str)} Zeichen")
        
        # Deserialize
        recovered = json.loads(json_str)
        
        # Verify all special chars preserved
        all_ok = True
        for key, value in test_dict.items():
            if recovered[key] != value:
                print(f"❌ '{key}': {value} != {recovered[key]}")
                all_ok = False
        
        if all_ok:
            print("✅ Alle Unicode-Zeichen erhalten")
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ Fehler bei Unicode-Handling: {e}")
        return False


def test_empty_and_none_values():
    """
    @brief Test handling of empty strings, None, and missing values.
    @details Validates edge cases in tag dictionaries.
    """
    print("\n⚠️  Test 7: Empty & None Values")
    print("─" * 60)
    
    test_dict = {
        'artist': '',
        'title': None,
        'album': 'Valid Album',
    }
    
    try:
        # Serialize (None remains None, not "None")
        json_str = json.dumps(test_dict)
        recovered = json.loads(json_str)
        
        # Verify empty string
        if recovered['artist'] == '':
            print("✅ Empty String erhalten")
        else:
            print(f"❌ Empty String wurde zu: '{recovered['artist']}'")
            return False
        
        # Verify None (becomes null in JSON)
        if recovered['title'] is None:
            print("✅ None erhalten")
        else:
            print(f"❌ None wurde zu: '{recovered['title']}'")
            return False
        
        # Test safe access patterns
        artist = recovered.get('artist') or 'Unknown Artist'
        if artist == 'Unknown Artist':
            print("✅ Empty String mit 'or' Fallback erkannt")
        else:
            print(f"❌ Empty String Fallback fehlgeschlagen: {artist}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Empty/None-Handling: {e}")
        return False


def run_all_tests():
    """
    @brief Run all dictionary operation tests.
    @return True if all tests passed, False otherwise.
    """
    print("\n" + "=" * 80)
    print("📚 DICTIONARY OPERATIONS TEST SUITE - Media Web Viewer")
    print("=" * 80)
    
    tests = [
        ("JSON Serialization", test_json_serialization),
        ("Nested Dict Serialization", test_nested_dict_serialization),
        ("Dictionary Merge", test_dict_merge),
        ("Key Operations", test_dict_key_operations),
        ("Copy Operations", test_dict_copy),
        ("Unicode & Special Chars", test_unicode_and_special_chars),
        ("Empty & None Values", test_empty_and_none_values),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Exception in {test_name}: {e}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    print("=" * 80)
    
    if failed == 0:
        print("\n✅ Alle Dictionary-Tests bestanden!\n")
        return True
    else:
        print(f"\n❌ {failed} Test(s) fehlgeschlagen\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
