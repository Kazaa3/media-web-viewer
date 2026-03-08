#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Event Persistence Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
Integration Test / Data Persistence

ZWECK:
------
Validiert, dass Daten nach einem Update-Event korrekt zurück in die Datenbank
und ins Dictionary geschrieben werden. Simuliert User-Event → Backend → DB Flow.

EINGABEWERTE:
-------------
- Test-MediaItem mit Tag-Dictionary
- Simuliertes Update-Event (neue Tags)
- Datenbank-Operationen

AUSGABEWERTE:
-------------
- Updated Tags in DB
- Retrieved Tags nach Reload
- Vergleich Original vs. Updated vs. Retrieved

TESTDATEIEN:
------------
- Keine spezifischen Dateien erforderlich
- Arbeitet mit temporärem DB-Eintrag

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste Concurrent Updates (Race Conditions)
- [ ] Teste Transaction Rollback bei Fehler
- [ ] Teste Event-Queue-Verarbeitung
- [ ] Teste Batch-Updates (mehrere Items gleichzeitig)
- [ ] Teste Partial Updates (nur einzelne Felder)
- [ ] Teste Complex Nested Updates (chapters, _parser_times)
- [ ] Teste Event-Listener-Benachrichtigung
- [ ] Füge pytest-Struktur mit Fixtures hinzu

VERWENDUNG:
-----------
    python tests/check_event_persistence.py
"""

import sys
import os
import json
from pathlib import Path
from copy import deepcopy

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False


def test_basic_update_persistence():
    """
    @brief Test basic tag update persistence to database.
    @details Simulates: Create item → Update tags → Verify in DB.
    """
    print("\n💾 Test 1: Basic Update Persistence")
    print("─" * 60)
    
    test_name = "_test_event_persistence_item.mp3"
    
    # Original tags
    original_tags = {
        'artist': 'Original Artist',
        'title': 'Original Title',
        'album': 'Original Album',
        'year': '2023',
    }
    
    # Updated tags (simulates user edit)
    updated_tags = {
        'artist': 'Updated Artist',
        'title': 'Updated Title',
        'album': 'Updated Album',
        'year': '2024',
        'genre': 'Rock',  # New field
    }
    
    try:
        # 1. Create test item in DB
        test_item = {
            'name': test_name,
            'path': f'/test/path/{test_name}',
            'type': 'audio',
            'duration': '180',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': original_tags,
            'extension': 'mp3',
            'container': 'MP3',
            'tag_type': 'ID3v2.4',
            'codec': 'mp3'
        }
        
        db.insert_media(test_item)
        print(f"✅ Test-Item erstellt: {test_name}")
        
        # 2. Simulate event: Update tags (wie in saveTags())
        db.update_media_tags(test_name, updated_tags)
        print("✅ Event ausgeführt: update_media_tags()")
        
        # 3. Retrieve from DB (simuliert Reload)
        all_media = db.get_all_media()
        retrieved_item = next((m for m in all_media if m['name'] == test_name), None)
        
        if not retrieved_item:
            print("❌ Item nicht in DB gefunden nach Update")
            return False
        
        retrieved_tags = retrieved_item['tags']
        print("✅ Item aus DB geladen")
        
        # 4. Verify all updates persisted
        verification_ok = True
        
        for key, expected_value in updated_tags.items():
            actual_value = retrieved_tags.get(key)
            
            if actual_value == expected_value:
                print(f"   ✅ '{key}': {expected_value}")
            else:
                print(f"   ❌ '{key}': erwartet '{expected_value}', erhalten '{actual_value}'")
                verification_ok = False
        
        if verification_ok:
            print("\n✅ Alle Updates korrekt persistiert")
            return True
        else:
            print("\n❌ Einige Updates gingen verloren")
            return False
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False
    finally:
        # Cleanup
        try:
            db.delete_media(test_name)
            print(f"\n🧹 Cleanup: {test_name} gelöscht")
        except:
            pass


def test_nested_dict_persistence():
    """
    @brief Test persistence of nested dictionaries (_parser_times, chapters).
    @details Validates complex structures survive the event cycle.
    """
    print("\n🗂️  Test 2: Nested Dictionary Persistence")
    print("─" * 60)
    
    test_name = "_test_nested_persistence.m4b"
    
    original_tags = {
        'artist': 'Test Author',
        'title': 'Test Audiobook',
        '_parser_times': {
            'filename': 0.001,
            'mutagen': 0.045,
            'ffmpeg': 0.000
        },
        'chapters': [
            {'start': 0, 'title': 'Chapter 1'},
            {'start': 120, 'title': 'Chapter 2'}
        ]
    }
    
    # Simulate chapter title update
    updated_tags = deepcopy(original_tags)
    updated_tags['chapters'][0]['title'] = 'Updated Chapter 1'
    updated_tags['artist'] = 'Updated Author'
    
    try:
        # Create item
        test_item = {
            'name': test_name,
            'path': f'/test/path/{test_name}',
            'type': 'audio',
            'duration': '3600',
            'category': 'Hörbuch',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': original_tags,
            'extension': 'm4b',
            'container': 'M4B',
            'tag_type': 'MP4',
            'codec': 'aac'
        }
        
        db.insert_media(test_item)
        print(f"✅ Test-Item erstellt: {test_name}")
        
        # Update with nested structure
        db.update_media_tags(test_name, updated_tags)
        print("✅ Nested Dict-Update ausgeführt")
        
        # Retrieve
        all_media = db.get_all_media()
        retrieved_item = next((m for m in all_media if m['name'] == test_name), None)
        
        if not retrieved_item:
            print("❌ Item nicht gefunden")
            return False
        
        retrieved_tags = retrieved_item['tags']
        
        # Verify nested dict preserved
        if '_parser_times' in retrieved_tags and isinstance(retrieved_tags['_parser_times'], dict):
            print("✅ Nested Dict '_parser_times' erhalten")
        else:
            print("❌ Nested Dict '_parser_times' fehlt oder falsch")
            return False
        
        # Verify array preserved
        if 'chapters' in retrieved_tags and isinstance(retrieved_tags['chapters'], list):
            if len(retrieved_tags['chapters']) == 2:
                print(f"✅ Array 'chapters' erhalten ({len(retrieved_tags['chapters'])} Einträge)")
            else:
                print(f"❌ Array 'chapters' hat falsche Länge")
                return False
        else:
            print("❌ Array 'chapters' fehlt oder falsch")
            return False
        
        # Verify chapter title update
        chapter1_title = retrieved_tags['chapters'][0]['title']
        if chapter1_title == 'Updated Chapter 1':
            print(f"✅ Chapter-Update korrekt: '{chapter1_title}'")
        else:
            print(f"❌ Chapter-Update fehlgeschlagen: '{chapter1_title}'")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False
    finally:
        try:
            db.delete_media(test_name)
            print(f"\n🧹 Cleanup: {test_name} gelöscht")
        except:
            pass


def test_partial_update():
    """
    @brief Test partial tag updates (only some fields changed).
    @details Validates unmodified fields are preserved.
    """
    print("\n🔀 Test 3: Partial Update (Selective Fields)")
    print("─" * 60)
    
    test_name = "_test_partial_update.flac"
    
    original_tags = {
        'artist': 'Original Artist',
        'title': 'Original Title',
        'album': 'Original Album',
        'year': '2023',
        'track': '5',
        'totaltracks': '12',
    }
    
    # Only update artist and year
    partial_update = {
        'artist': 'Partial Updated Artist',
        'year': '2024',
    }
    
    try:
        # Create item
        test_item = {
            'name': test_name,
            'path': f'/test/path/{test_name}',
            'type': 'audio',
            'duration': '240',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': original_tags,
            'extension': 'flac',
            'container': 'FLAC',
            'tag_type': 'Vorbis',
            'codec': 'flac'
        }
        
        db.insert_media(test_item)
        print(f"✅ Test-Item erstellt: {test_name}")
        
        # Get current tags and merge partial update
        # (This simulates what saveTags() does in app.html)
        current = deepcopy(original_tags)
        current.update(partial_update)
        
        db.update_media_tags(test_name, current)
        print("✅ Partial Update ausgeführt")
        
        # Retrieve
        all_media = db.get_all_media()
        retrieved_item = next((m for m in all_media if m['name'] == test_name), None)
        
        if not retrieved_item:
            print("❌ Item nicht gefunden")
            return False
        
        retrieved_tags = retrieved_item['tags']
        
        # Verify updated fields
        if retrieved_tags['artist'] == 'Partial Updated Artist':
            print("✅ Updated Field: artist")
        else:
            print(f"❌ artist nicht korrekt: {retrieved_tags['artist']}")
            return False
        
        if retrieved_tags['year'] == '2024':
            print("✅ Updated Field: year")
        else:
            print(f"❌ year nicht korrekt: {retrieved_tags['year']}")
            return False
        
        # Verify unmodified fields preserved
        preserved_fields = ['title', 'album', 'track', 'totaltracks']
        all_preserved = True
        
        for field in preserved_fields:
            expected = original_tags[field]
            actual = retrieved_tags.get(field)
            
            if actual == expected:
                print(f"✅ Preserved Field: {field}")
            else:
                print(f"❌ {field} verändert: erwartet '{expected}', erhalten '{actual}'")
                all_preserved = False
        
        return all_preserved
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False
    finally:
        try:
            db.delete_media(test_name)
            print(f"\n🧹 Cleanup: {test_name} gelöscht")
        except:
            pass


def test_multiple_update_cycles():
    """
    @brief Test multiple sequential updates (edit → save → edit → save).
    @details Validates data integrity across multiple update cycles.
    """
    print("\n🔄 Test 4: Multiple Update Cycles")
    print("─" * 60)
    
    test_name = "_test_multiple_updates.mp3"
    
    initial_tags = {
        'artist': 'Initial Artist',
        'title': 'Initial Title',
        'version': '1',
    }
    
    try:
        # Create item
        test_item = {
            'name': test_name,
            'path': f'/test/path/{test_name}',
            'type': 'audio',
            'duration': '180',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': initial_tags,
            'extension': 'mp3',
            'container': 'MP3',
            'tag_type': 'ID3v2.4',
            'codec': 'mp3'
        }
        
        db.insert_media(test_item)
        print(f"✅ Test-Item erstellt (Version 1)")
        
        # Cycle 1: Update artist
        update1 = deepcopy(initial_tags)
        update1['artist'] = 'Updated Artist V2'
        update1['version'] = '2'
        db.update_media_tags(test_name, update1)
        print("✅ Update Cycle 1 ausgeführt (Version 2)")
        
        # Cycle 2: Update title
        update2 = deepcopy(update1)
        update2['title'] = 'Updated Title V3'
        update2['version'] = '3'
        db.update_media_tags(test_name, update2)
        print("✅ Update Cycle 2 ausgeführt (Version 3)")
        
        # Cycle 3: Add genre
        update3 = deepcopy(update2)
        update3['genre'] = 'Rock'
        update3['version'] = '4'
        db.update_media_tags(test_name, update3)
        print("✅ Update Cycle 3 ausgeführt (Version 4)")
        
        # Retrieve final state
        all_media = db.get_all_media()
        retrieved_item = next((m for m in all_media if m['name'] == test_name), None)
        
        if not retrieved_item:
            print("❌ Item nicht gefunden")
            return False
        
        retrieved_tags = retrieved_item['tags']
        
        # Verify final state
        expected_final = {
            'artist': 'Updated Artist V2',
            'title': 'Updated Title V3',
            'genre': 'Rock',
            'version': '4',
        }
        
        print("\n📊 Final State Verification:")
        all_correct = True
        
        for key, expected_value in expected_final.items():
            actual_value = retrieved_tags.get(key)
            
            if actual_value == expected_value:
                print(f"   ✅ {key}: {expected_value}")
            else:
                print(f"   ❌ {key}: erwartet '{expected_value}', erhalten '{actual_value}'")
                all_correct = False
        
        return all_correct
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False
    finally:
        try:
            db.delete_media(test_name)
            print(f"\n🧹 Cleanup: {test_name} gelöscht")
        except:
            pass


def run_all_tests():
    """
    @brief Run all event persistence tests.
    @return True if all tests passed, False otherwise.
    """
    if not DB_AVAILABLE:
        print("❌ db.py Modul nicht importierbar")
        print("   Stelle sicher, dass db.py im Projektverzeichnis existiert.")
        return False
    
    print("\n" + "=" * 80)
    print("💾 EVENT PERSISTENCE TEST SUITE - Media Web Viewer")
    print("=" * 80)
    print("\nSimuliert User-Event → Backend → DB → Reload Flow\n")
    
    tests = [
        ("Basic Update Persistence", test_basic_update_persistence),
        ("Nested Dict Persistence", test_nested_dict_persistence),
        ("Partial Update", test_partial_update),
        ("Multiple Update Cycles", test_multiple_update_cycles),
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
    
    # Info
    try:
        db_path = db.get_active_db_path()
        stats = db.get_db_stats()
        print(f"\n📁 Database: {db_path}")
        print(f"📊 Total Items (inkl. Test-Items): {stats['total_items']}")
    except:
        pass
    
    print("=" * 80)
    
    if failed == 0:
        print("\n✅ Alle Event-Persistence-Tests bestanden!\n")
        return True
    else:
        print(f"\n❌ {failed} Test(s) fehlgeschlagen\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
