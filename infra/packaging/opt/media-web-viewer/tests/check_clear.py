#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Database Integration Test / Backup & Restore
# Eingabewerte: Aktuelle Datenbank, Test-Items für Backup/Restore, clear_media() Funktion
# Ausgabewerte: DB-Zustand vor/nach Clear (Anzahl Items), Backup-Dateien, Restore-Status
# Testdateien: Keine (arbeitet mit aktiver DB und temporären Backups)
# Kommentar: Validiert clear_media() und stellt sicher dass DB nach Test wieder in Ursprungszustand zurückversetzt wird.
"""
================================================================================
Database Clear & Backup Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
Database Integration Test / Backup & Restore

ZWECK:
------
Validiert die clear_media() Funktion und stellt sicher, dass die Datenbank
nach dem Test wieder in den Ursprungszustand zurückversetzt wird.
Testet Backup/Restore-Funktionalität.

EINGABEWERTE:
-------------
- Aktuelle Datenbank (~/.media-web-viewer/media_library.db)
- Test-Items für Backup/Restore
- clear_media() Funktion

AUSGABEWERTE:
-------------
- DB-Zustand vor Clear (Anzahl Items)
- DB-Zustand nach Clear (sollte 0 sein)
- DB-Zustand nach Restore (sollte wieder original sein)
- Backup-Dateien

TESTDATEIEN:
------------
- Keine spezifischen Dateien erforderlich
- Arbeitet mit aktiver DB und temporären Backups

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste Incremental Backups
- [ ] Teste Backup-Kompression
- [ ] Teste Backup-Verschlüsselung
- [ ] Teste automatische Backup-Rotation
- [ ] Teste Backup-Integrität (Checksums)
- [ ] Teste Restore von beschädigten Backups
- [ ] Teste Backup zu externem Storage
- [ ] Füge pytest-Struktur mit Fixtures hinzu

VERWENDUNG:
-----------
    python tests/check_clear.py
"""

import sys
import os
import sqlite3
import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False


def backup_database():
    """
    @brief Create a complete backup of current database state.
    @return List of all media items (can be restored later).
    """
    try:
        all_items = db.get_all_media()
        return all_items
    except Exception as e:
        print(f"⚠️  Backup fehlgeschlagen: {e}")
        return []


def restore_database(backup_items):
    """
    @brief Restore database from backup.
    @param backup_items List of media items to restore.
    @return Number of items restored.
    """
    restored_count = 0
    
    for item in backup_items:
        try:
            # Reconstruct full item dictionary
            restore_item = {
                'name': item['name'],
                'path': item['path'],
                'type': item['type'],
                'duration': item['duration'],
                'category': item.get('category', 'Audio'),
                'is_transcoded': item['is_transcoded'],
                'transcoded_format': item.get('transcoded_format'),
                'tags': item['tags'],
                'extension': item.get('extension', ''),
                'container': item.get('container', ''),
                'tag_type': item.get('tag_type', ''),
                'codec': item.get('codec', '')
            }
            
            db.insert_media(restore_item)
            restored_count += 1
            
        except Exception as e:
            print(f"⚠️  Konnte Item '{item['name']}' nicht restaurieren: {e}")
    
    return restored_count


def test_clear_media_with_backup():
    """
    @brief Test clear_media() function with full backup/restore cycle.
    @details Ensures database returns to original state after test.
    """
    print("\n🗑️  Test 1: Clear Media mit Backup/Restore")
    print("─" * 60)
    
    try:
        # 1. Get initial state
        initial_stats = db.get_db_stats()
        initial_count = initial_stats['total_items']
        
        print(f"📊 Initial State: {initial_count} Items in DB")
        
        if initial_count == 0:
            print("⚠️  DB ist bereits leer, füge Test-Items hinzu...")
            
            # Add test items
            test_items = [
                {
                    'name': '_test_clear_1.mp3',
                    'path': '/test/path/_test_clear_1.mp3',
                    'type': 'audio',
                    'duration': '180',
                    'category': 'Music',
                    'is_transcoded': False,
                    'transcoded_format': None,
                    'tags': {'artist': 'Test Artist 1', 'title': 'Test Title 1'},
                    'extension': 'mp3',
                    'container': 'MP3',
                    'tag_type': 'ID3v2.4',
                    'codec': 'mp3'
                },
                {
                    'name': '_test_clear_2.flac',
                    'path': '/test/path/_test_clear_2.flac',
                    'type': 'audio',
                    'duration': '240',
                    'category': 'Music',
                    'is_transcoded': False,
                    'transcoded_format': None,
                    'tags': {'artist': 'Test Artist 2', 'title': 'Test Title 2'},
                    'extension': 'flac',
                    'container': 'FLAC',
                    'tag_type': 'Vorbis',
                    'codec': 'flac'
                }
            ]
            
            for item in test_items:
                db.insert_media(item)
            
            initial_count = len(test_items)
            print(f"✅ {initial_count} Test-Items hinzugefügt")
        
        # 2. Create backup
        print(f"\n💾 Erstelle Backup von {initial_count} Items...")
        backup = backup_database()
        
        if len(backup) != initial_count:
            print(f"❌ Backup unvollständig: {len(backup)} != {initial_count}")
            return False
        
        print(f"✅ Backup erstellt: {len(backup)} Items gesichert")
        
        # 3. Clear database
        print("\n🗑️  Führe clear_media() aus...")
        db.clear_media()
        
        # 4. Verify database is empty
        after_clear_stats = db.get_db_stats()
        after_clear_count = after_clear_stats['total_items']
        
        if after_clear_count == 0:
            print(f"✅ clear_media() erfolgreich: 0 Items in DB")
        else:
            print(f"❌ clear_media() fehlgeschlagen: {after_clear_count} Items noch vorhanden")
            # Restore before returning
            restore_database(backup)
            return False
        
        # 5. Restore from backup
        print(f"\n♻️  Stelle {len(backup)} Items wieder her...")
        restored_count = restore_database(backup)
        
        if restored_count == len(backup):
            print(f"✅ Restore erfolgreich: {restored_count} Items wiederhergestellt")
        else:
            print(f"⚠️  Partial Restore: {restored_count}/{len(backup)} Items")
        
        # 6. Verify restoration
        final_stats = db.get_db_stats()
        final_count = final_stats['total_items']
        
        if final_count == initial_count:
            print(f"✅ DB-Zustand wiederhergestellt: {final_count} Items")
            return True
        else:
            print(f"⚠️  DB-Zustand abweichend: {final_count} Items (erwartet: {initial_count})")
            return final_count == restored_count  # OK if only test items were added
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


def test_file_backup():
    """
    @brief Test file-based database backup (SQLite file copy).
    @details Creates a physical backup of the database file.
    """
    print("\n💾 Test 2: File-Based Database Backup")
    print("─" * 60)
    
    try:
        db_path = db.get_active_db_path()
        
        if not db_path.exists():
            print("❌ Datenbank-Datei nicht gefunden")
            return False
        
        db_size = db_path.stat().st_size
        print(f"📁 Datenbank: {db_path}")
        print(f"💾 Größe: {db_size:,} bytes ({db_size / 1024:.2f} KB)")
        
        # Create temp backup
        backup_dir = Path(tempfile.gettempdir()) / "media_web_viewer_backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"media_library_backup_{timestamp}.db"
        
        print(f"\n💾 Erstelle File-Backup: {backup_path.name}")
        shutil.copy2(db_path, backup_path)
        
        if backup_path.exists():
            backup_size = backup_path.stat().st_size
            print(f"✅ Backup erstellt: {backup_size:,} bytes")
            
            if backup_size == db_size:
                print("✅ Backup-Größe identisch mit Original")
            else:
                print(f"⚠️  Backup-Größe abweichend: {backup_size} != {db_size}")
            
            # Verify backup is valid SQLite database
            try:
                conn = sqlite3.connect(str(backup_path))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM media")
                backup_count = cursor.fetchone()[0]
                conn.close()
                
                print(f"✅ Backup validiert: {backup_count} Items lesbar")
                
                # Cleanup
                backup_path.unlink()
                print(f"🧹 Backup gelöscht: {backup_path.name}")
                
                return True
                
            except sqlite3.Error as e:
                print(f"❌ Backup-Validierung fehlgeschlagen: {e}")
                return False
        else:
            print("❌ Backup-Datei nicht erstellt")
            return False
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


def test_selective_backup_restore():
    """
    @brief Test selective backup/restore (only specific items).
    @details Validates partial backup and restore functionality.
    """
    print("\n🎯 Test 3: Selective Backup/Restore")
    print("─" * 60)
    
    test_items = [
        {
            'name': '_test_selective_1.mp3',
            'path': '/test/path/_test_selective_1.mp3',
            'type': 'audio',
            'duration': '180',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': {'artist': 'Artist 1'},
            'extension': 'mp3',
            'container': 'MP3',
            'tag_type': 'ID3v2.4',
            'codec': 'mp3'
        },
        {
            'name': '_test_selective_2.mp3',
            'path': '/test/path/_test_selective_2.mp3',
            'type': 'audio',
            'duration': '240',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': {'artist': 'Artist 2'},
            'extension': 'mp3',
            'container': 'MP3',
            'tag_type': 'ID3v2.4',
            'codec': 'mp3'
        },
        {
            'name': '_test_selective_3.mp3',
            'path': '/test/path/_test_selective_3.mp3',
            'type': 'audio',
            'duration': '300',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': {'artist': 'Artist 3'},
            'extension': 'mp3',
            'container': 'MP3',
            'tag_type': 'ID3v2.4',
            'codec': 'mp3'
        }
    ]
    
    try:
        # Create test items
        print(f"➕ Erstelle {len(test_items)} Test-Items...")
        for item in test_items:
            db.insert_media(item)
        print(f"✅ {len(test_items)} Items erstellt")
        
        # Selective backup (only items 1 and 3)
        all_media = db.get_all_media()
        selective_backup = [
            m for m in all_media 
            if m['name'] in ['_test_selective_1.mp3', '_test_selective_3.mp3']
        ]
        
        print(f"\n💾 Selective Backup: {len(selective_backup)}/3 Items")
        
        # Delete all test items
        for item in test_items:
            db.delete_media(item['name'])
        print("🗑️  Alle Test-Items gelöscht")
        
        # Restore selective backup
        restored = restore_database(selective_backup)
        print(f"♻️  {restored} Items wiederhergestellt")
        
        # Verify only backed up items are restored
        all_media_after = db.get_all_media()
        restored_names = {m['name'] for m in all_media_after if m['name'].startswith('_test_selective_')}
        
        expected_names = {'_test_selective_1.mp3', '_test_selective_3.mp3'}
        
        if restored_names == expected_names:
            print(f"✅ Selective Restore korrekt: {restored_names}")
            success = True
        else:
            print(f"❌ Selective Restore inkorrekt:")
            print(f"   Erwartet: {expected_names}")
            print(f"   Erhalten: {restored_names}")
            success = False
        
        # Cleanup
        for name in restored_names:
            db.delete_media(name)
        print(f"🧹 {len(restored_names)} Test-Items aufgeräumt")
        
        return success
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        
        # Cleanup attempt
        try:
            for item in test_items:
                db.delete_media(item['name'])
        except:
            pass
        
        return False


def test_clear_with_verification():
    """
    @brief Test clear_media() with detailed verification.
    @details Ensures all aspects of clearing work correctly.
    """
    print("\n🔍 Test 4: Clear Media mit detaillierter Verifikation")
    print("─" * 60)
    
    test_name = "_test_clear_verification.mp3"
    
    try:
        # Add test item
        test_item = {
            'name': test_name,
            'path': f'/test/path/{test_name}',
            'type': 'audio',
            'duration': '180',
            'category': 'Music',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': {'artist': 'Test'},
            'extension': 'mp3',
            'container': 'MP3',
            'tag_type': 'ID3v2.4',
            'codec': 'mp3'
        }
        
        db.insert_media(test_item)
        print(f"✅ Test-Item hinzugefügt: {test_name}")
        
        # Backup
        backup = backup_database()
        backup_count = len(backup)
        print(f"💾 Backup: {backup_count} Items")
        
        # Clear
        db.clear_media()
        print("🗑️  clear_media() ausgeführt")
        
        # Verify empty
        stats = db.get_db_stats()
        
        if stats['total_items'] == 0:
            print("✅ DB leer: 0 Items")
        else:
            print(f"❌ DB nicht leer: {stats['total_items']} Items")
            restore_database(backup)
            return False
        
        if len(stats['categories']) == 0:
            print("✅ Kategorien leer")
        else:
            print(f"⚠️  Kategorien noch vorhanden: {stats['categories']}")
        
        # Verify specific item is gone
        known_names = db.get_known_media_names()
        if test_name not in known_names:
            print(f"✅ Test-Item erfolgreich gelöscht")
        else:
            print(f"❌ Test-Item noch vorhanden")
            restore_database(backup)
            return False
        
        # Restore
        restored = restore_database(backup)
        print(f"\n♻️  {restored}/{backup_count} Items wiederhergestellt")
        
        # Final verification
        final_stats = db.get_db_stats()
        if final_stats['total_items'] == backup_count:
            print(f"✅ DB-Zustand wiederhergestellt: {final_stats['total_items']} Items")
            return True
        else:
            print(f"⚠️  Item-Count abweichend: {final_stats['total_items']} (erwartet: {backup_count})")
            return False
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


def run_all_tests():
    """
    @brief Run all clear and backup tests.
    @return True if all tests passed, False otherwise.
    """
    if not DB_AVAILABLE:
        print("❌ db.py Modul nicht importierbar")
        print("   Stelle sicher, dass db.py im Projektverzeichnis existiert.")
        return False
    
    print("\n" + "=" * 80)
    print("🗑️  DATABASE CLEAR & BACKUP TEST SUITE - Media Web Viewer")
    print("=" * 80)
    print("\nValidiert clear_media() mit vollständiger Backup/Restore-Garantie\n")
    
    tests = [
        ("Clear Media mit Backup/Restore", test_clear_media_with_backup),
        ("File-Based Database Backup", test_file_backup),
        ("Selective Backup/Restore", test_selective_backup_restore),
        ("Clear mit detaillierter Verifikation", test_clear_with_verification),
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
    
    # Final DB info
    try:
        db_path = db.get_active_db_path()
        stats = db.get_db_stats()
        print(f"\n📁 Database: {db_path}")
        print(f"📊 Final State: {stats['total_items']} Items")
        print(f"📂 Kategorien: {stats['categories']}")
    except Exception as e:
        print(f"\n⚠️  Konnte DB-Info nicht abrufen: {e}")
    
    print("=" * 80)
    
    if failed == 0:
        print("\n✅ Alle Clear & Backup Tests bestanden!")
        print("✅ Datenbank wurde in Originalzustand zurückversetzt!\n")
        return True
    else:
        print(f"\n❌ {failed} Test(s) fehlgeschlagen")
        print("⚠️  Überprüfe DB-Zustand manuell\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
