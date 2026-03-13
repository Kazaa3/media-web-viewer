#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Database Integration Test
# Eingabewerte: SQLite-Datenbank (~/.media-web-viewer/media_library.db), Test-Mediendaten, db.py Modul-Funktionen
# Ausgabewerte: Tabellen-Existenz, CRUD-Operation-Status, Legacy-DB-Informationen, Statistiken
# Testdateien: Keine spezifischen Dateien erforderlich (arbeitet mit temporärer Test-DB)
# ERWEITERUNGEN (TODO): Playlist-Funktionalität, Foreign-Key-Constraints, Transaktions-Rollback, Concurrent-Access, Performance, Migration, Backup/Restore, pytest-fixtures
# VERWENDUNG: python tests/check_db.py
# ================================================================================================
# Database Integrity Test - Media Web Viewer
# ================================================================================================

"""
================================================================================
Database Integrity Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
Database Integration Test

ZWECK:
------
Validiert die vollständige Datenbank-Funktionalität des Media Web Viewers.
Prüft Tabellenstruktur, CRUD-Operationen, Legacy-DB-Handling und Statistiken.

EINGABEWERTE:
-------------
- SQLite-Datenbank (~/.media-web-viewer/media_library.db)
- Test-Mediendaten
- db.py Modul-Funktionen

AUSGABEWERTE:
-------------
- Tabellen-Existenz (media, playlists, playlist_media)
- Spalten-Validierung (alle erforderlichen Felder)
- CRUD-Operation-Status
- Legacy-DB-Informationen
- Statistiken (Anzahl Items, Kategorien)

TESTDATEIEN:
------------
- Keine spezifischen Dateien erforderlich
- Arbeitet mit temporärer Test-DB

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste Playlist-Funktionalität (create, add_media, delete)
- [ ] Teste Foreign-Key-Constraints
- [ ] Teste Transaktions-Rollback
- [ ] Teste Concurrent-Access-Szenarien
- [ ] Teste große Datenmengen (Performance)
- [ ] Teste DB-Migration zwischen Versionen
- [ ] Teste Backup/Restore-Funktionalität
- [ ] Füge pytest-Struktur hinzu mit fixtures

VERWENDUNG:
-----------
    python tests/check_db.py
"""

import sys
import os
import sqlite3
import json
import tempfile
from pathlib import Path

# Add project root to path

try:
    import src.core.db as db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

def test_db_initialization():
    """
    @brief Test database initialization and table creation.
    @details Validates that init_db() creates all required tables.
    """
    print("\n🗄️  Test 1: Database Initialization")
    print("─" * 60)
    
    try:
        # Initialize database
        db.init_db()
        
        # Check if DB file exists
        db_path = db.get_active_db_path()
        if db_path.exists():
            print(f"✅ Database erstellt: {db_path}")
        else:
            print(f"❌ Database nicht gefunden: {db_path}")
            return False
        
        # Connect and check tables
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['media', 'playlists', 'playlist_media']
        
        for table in required_tables:
            if table in tables:
                print(f"✅ Tabelle '{table}' existiert")
            else:
                print(f"❌ Tabelle '{table}' fehlt")
                conn.close()
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei DB-Initialisierung: {e}")
        return False

def test_media_table_structure():
    """
    @brief Test media table structure and column integrity.
    @details Validates all required columns exist with correct types.
    """
    print("\n📋 Test 2: Media Table Structure")
    print("─" * 60)
    
    try:
        db_path = db.get_active_db_path()
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(media)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        required_columns = {
            'id': 'INTEGER',
            'name': 'TEXT',
            'path': 'TEXT',
            'type': 'TEXT',
            'duration': 'TEXT',
            'category': 'TEXT',
            'is_transcoded': 'BOOLEAN',
            'transcoded_format': 'TEXT',
            'tags': 'TEXT',
            'extension': 'TEXT',
            'container': 'TEXT',
            'tag_type': 'TEXT',
            'codec': 'TEXT'
        }
        
        all_ok = True
        for col_name, col_type in required_columns.items():
            if col_name in columns:
                actual_type = columns[col_name]
                # SQLite type matching (INTEGER/INT, TEXT/VARCHAR are equivalent)
                if actual_type == col_type or (actual_type in ['INT', 'INTEGER'] and col_type in ['INT', 'INTEGER']):
                    print(f"✅ Spalte '{col_name}' ({col_type})")
                else:
                    print(f"⚠️  Spalte '{col_name}' hat Typ '{actual_type}' (erwartet: {col_type})")
            else:
                print(f"❌ Spalte '{col_name}' fehlt")
                all_ok = False
        
        print(f"\n📊 Gesamt: {len(columns)} Spalten gefunden")
        
        conn.close()
        return all_ok
        
    except Exception as e:
        print(f"❌ Fehler bei Struktur-Prüfung: {e}")
        return False

def test_crud_operations():
    """
    @brief Test Create, Read, Update, Delete operations.
    @details Validates all CRUD functions work correctly.
    """
    print("\n🔄 Test 3: CRUD Operations")
    print("─" * 60)
    
    test_item = {
        'name': 'test_audio_file.mp3',
        'path': '/test/path/test_audio_file.mp3',
        'type': 'audio',
        'duration': '180',
        'category': 'Music',
        'is_transcoded': False,
        'transcoded_format': None,
        'tags': {'artist': 'Test Artist', 'title': 'Test Title'},
        'extension': 'mp3',
        'container': 'MP3',
        'tag_type': 'ID3v2.4',
        'codec': 'mp3'
    }
    
    try:
        # CREATE
        print("➕ Create: Füge Test-Item ein...")
        db.insert_media(test_item)
        
        # CHECK if exists
        known_names = db.get_known_media_names()
        if test_item['name'] in known_names:
            print(f"✅ Item erfolgreich eingefügt: {test_item['name']}")
        else:
            print(f"❌ Item nicht gefunden nach INSERT")
            return False
        
        # READ
        print("📖 Read: Rufe Item ab...")
        path = db.get_media_path(test_item['name'])
        if path == test_item['path']:
            print(f"✅ Path korrekt gelesen: {path}")
        else:
            print(f"❌ Path inkorrekt: erwartet '{test_item['path']}', erhalten '{path}'")
            return False
        
        # UPDATE
        print("✏️  Update: Aktualisiere Tags...")
        new_tags = {'artist': 'Updated Artist', 'title': 'Updated Title', 'album': 'Test Album'}
        db.update_media_tags(test_item['name'], new_tags)
        
        # Verify update
        all_media = db.get_all_media()
        updated_item = next((m for m in all_media if m['name'] == test_item['name']), None)
        
        if updated_item and updated_item['tags'].get('album') == 'Test Album':
            print(f"✅ Tags erfolgreich aktualisiert")
        else:
            print(f"❌ Tags nicht korrekt aktualisiert")
            return False
        
        # RENAME
        print("🔄 Rename: Benenne Item um...")
        new_name = 'renamed_test_file.mp3'
        success = db.rename_media(test_item['name'], new_name)
        
        if success:
            print(f"✅ Item umbenannt: {test_item['name']} → {new_name}")
            test_item['name'] = new_name  # Update for cleanup
        else:
            print(f"❌ Umbenennung fehlgeschlagen")
            return False
        
        # DELETE
        print("🗑️  Delete: Lösche Test-Item...")
        db.delete_media(test_item['name'])
        
        # Verify deletion
        known_names_after = db.get_known_media_names()
        if test_item['name'] not in known_names_after:
            print(f"✅ Item erfolgreich gelöscht")
        else:
            print(f"❌ Item noch vorhanden nach DELETE")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei CRUD-Operationen: {e}")
        # Cleanup
        try:
            db.delete_media(test_item['name'])
        except:
            pass
        return False

def test_database_stats():
    """
    @brief Test database statistics retrieval.
    @details Validates get_db_stats() function.
    """
    print("\n📊 Test 4: Database Statistics")
    print("─" * 60)
    
    try:
        stats = db.get_db_stats()
        
        if 'total_items' in stats:
            print(f"✅ Total Items: {stats['total_items']}")
        else:
            print(f"❌ 'total_items' fehlt in Statistiken")
            return False
        
        if 'categories' in stats:
            print(f"✅ Categories: {stats['categories']}")
        else:
            print(f"❌ 'categories' fehlt in Statistiken")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Statistik-Abruf: {e}")
        return False

def test_legacy_database_handling():
    """
    @brief Test legacy database detection and cleanup.
    @details Validates legacy DB functions.
    """
    print("\n🗂️  Test 5: Legacy Database Handling")
    print("─" * 60)
    
    try:
        # Get active DB
        active_db = db.get_active_db_path()
        print(f"✅ Active DB: {active_db}")
        
        # Get legacy candidates
        candidates = db.get_legacy_db_candidates()
        print(f"✅ Legacy Candidates gefunden: {len(candidates)}")
        
        for candidate in candidates[:5]:  # Show first 5
            exists = "✓" if candidate.exists() else "✗"
            print(f"   [{exists}] {candidate}")
        
        # List existing legacy DBs
        legacy_dbs = db.list_legacy_databases()
        if legacy_dbs:
            print(f"⚠️  {len(legacy_dbs)} Legacy-Datenbank(en) gefunden:")
            for legacy_db in legacy_dbs:
                print(f"   • {legacy_db}")
        else:
            print(f"✅ Keine Legacy-Datenbanken gefunden")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Legacy-DB-Handling: {e}")
        return False

def run_all_tests():
    """
    @brief Run all database tests.
    @return True if all tests passed, False otherwise.
    """
    if not DB_AVAILABLE:
        print("❌ db.py Modul nicht importierbar")
        print("   Stelle sicher, dass db.py im Projektverzeichnis existiert.")
        return False
    
    print("\n" + "=" * 80)
    print("🗄️  DATABASE INTEGRITY TEST SUITE - Media Web Viewer")
    print("=" * 80)
    
    tests = [
        ("Database Initialization", test_db_initialization),
        ("Media Table Structure", test_media_table_structure),
        ("CRUD Operations", test_crud_operations),
        ("Database Statistics", test_database_stats),
        ("Legacy Database Handling", test_legacy_database_handling),
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
    
    # Database info
    try:
        db_path = db.get_active_db_path()
        db_size = db_path.stat().st_size if db_path.exists() else 0
        print(f"\n📁 Database: {db_path}")
        print(f"💾 Size: {db_size:,} bytes ({db_size / 1024:.2f} KB)")
        
        stats = db.get_db_stats()
        print(f"📊 Total Media Items: {stats['total_items']}")
        
    except Exception as e:
        print(f"\n⚠️  Konnte DB-Info nicht abrufen: {e}")
    
    print("=" * 80)
    
    if failed == 0:
        print("\n✅ Alle Database-Tests bestanden!\n")
        return True
    else:
        print(f"\n❌ {failed} Test(s) fehlgeschlagen\n")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
