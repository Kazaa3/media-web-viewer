#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI / Media Visibility
# Eingabewerte: Datenbank-Items, Medienscann-Ergebnisse
# Ausgabewerte: Library-Visibility (bool), Kategorie-Diversity
# Testdateien: Diverse Media-Files (ISO, BIN, CUE, Audio/Video)
# ERWEITERUNGEN (TODO): [ ] Filter-Logik für Unterkategorien testen, [ ] Performance-Tests für große Libraries
# KOMMENTAR: Verifiziert die Sichtbarkeit von Medienobjekten in der UI basierend auf Kategorien.
# VERWENDUNG: pytest tests/integration/category/ui/test_ui_media_visibility.py

"""
KATEGORIE:
----------
UI / Media Visibility

ZWECK:
------
Verifiziert die Sichtbarkeit von Medienobjekten in der UI basierend auf Kategorien und Dateitypen.
Stellt sicher, dass der Scanner alle unterstützten Erweiterungen korrekt erfasst.

EINGABEWERTE:
-------------
- Datenbank-Items
- Medienscann-Ergebnisse

AUSGABEWERTE:
-------------
- Library-Visibility (bool)
- Kategorie-Diversity

TESTDATEIEN:
------------
- Diverse Media-Files (ISO, BIN, CUE, Audio/Video)

ERWEITERUNGEN (TODO):
---------------------
- [ ] Filter-Logik für Unterkategorien testen
- [ ] Performance-Tests für große Libraries

VERWENDUNG:
-----------
    pytest tests/integration/category/ui/test_ui_media_visibility.py
"""

from src.core.main import get_library, scan_media, PARSER_CONFIG
import src.core.db as db

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Ensure we have a clean state and some items in the DB."""
    # We use the real media folder because we want to see real results
    # We run this only once for the module to save time
    scan_media(clear_db=True)
    yield

def test_library_visibility_all_categories():
    """Verify that get_library returns items from various categories by default."""
    library = get_library()
    media = library.get('media', [])
    
    # We expect at least some items
    assert len(media) > 0, "Library should not be empty after scan"
    
    # Check for category diversity
    categories = {item.get('category') for item in media}
    print(f"\nFound categories: {categories}")
    
    # We expect at least Audio or Video/Film
    assert any(c in categories for c in ['Audio', 'Album', 'Film', 'Video']), "Expected at least some common categories"

def test_disk_image_visibility():
    """Verify that disk images (.iso, .bin) are visible in the library under 'abbild' filter."""
    # Temporarily force only 'abbild' display
    original_disp = PARSER_CONFIG.get("displayed_categories")
    PARSER_CONFIG["displayed_categories"] = ["abbild"]
    
    try:
        library = get_library()
        media = library.get('media', [])
        
        # Check if we have disk images (even if categorized as 'Film' or 'Unbekannt')
        # S3gold1_g.bin should be there as 'Unbekannt' category but 'abbild' setting should find it 
        # based on cat_map in main.py
        
        found_abbild = False
        for item in media:
            if item.get('extension') in ['ISO', 'BIN', 'CUE'] or 'Abbild' in item.get('category', ''):
                found_abbild = True
                break
        
        # Note: If the cat_map in main.py excludes 'Unbekannt', we might need to update it.
        # My manual check showed S3gold1_g.bin as 'Unbekannt'.
        assert found_abbild, "Disk images should be visible when 'abbild' category is active"
        
    finally:
        PARSER_CONFIG["displayed_categories"] = original_disp

def test_item_metadata_for_editor():
    """Verify that items have the necessary fields for the metadata editor."""
    library = get_library()
    media = library.get('media', [])
    
    if not media:
        pytest.skip("No media items found to test")
        
    sample = media[0]
    required_keys = ['name', 'path', 'tags', 'category', 'type', 'duration']
    for key in required_keys:
        assert key in sample, f"Item missing key: {key}"
        
    # Tags should be a dict
    assert isinstance(sample['tags'], dict), "Tags should be a dictionary"

def test_scanner_breadth_extensions():
    """Verify that the scanner picked up non-ISO disk images."""
    all_media = db.get_all_media()
    extensions = {item.get('path', '').split('.')[-1].lower() for item in all_media if '.' in item.get('path', '')}
    
    print(f"\nFound extensions: {extensions}")
    assert 'bin' in extensions or 'cue' in extensions, "Scanner should have detected .bin or .cue files"

if __name__ == "__main__":
    pytest.main([__file__])
