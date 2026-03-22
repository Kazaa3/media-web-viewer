# 97 – Erweiterte Medien-Kategorisierung

**Datum:** 10.03.2026  
**Version:** 1.3.5  
**Status:** ✅ Abgeschlossen

## Zielsetzung

Implementierung spezifischer Medienkategorien zur besseren Unterscheidung und Filterung in der Benutzeroberfläche. Fokus auf die vom Nutzer gewünschten Hauptkategorien: **Audio**, **Hörbuch**, **Video**, **ISO/Image** und **Bilder**.

## Umsetzung

### 1. Backend-Erweiterungen (Python)

- **`parsers/format_utils.py`**: 
    - Einführung von `IMAGE_EXTENSIONS` für gängige Bildformate (.jpg, .png, .webp, etc.).
    - Update von `detect_file_format` zur Erkennung von Bildern.
    - Korrektur der Import-Reihenfolge zur Vermeidung von `NameError` während der Testphase.
- **`media_format.py`**:
    - Anpassung von `detect_type` zur Rückgabe der neuen Standard-Kategorien.
    - Implementierung einer Heuristik zur Erkennung von Hörbüchern (basierend auf `.m4b` Extension oder Schlüsselwörtern im Pfad wie "hörbuch", "audiobook").
- **`models.py`**:
    - Synchronisation von `detect_logical_type` und `get_category` mit den neuen Kategorien.
    - Sicherstellung, dass `.iso` Dateien einheitlich als `ISO/Image` klassifiziert werden.

### 2. Frontend-Integration (HTML/JS/i18n)

- **`web/app.html`**:
    - Erweiterung der `specialCategories` Liste, damit die neuen Kategorien korrekt als Badges in der Bibliotheksansicht angezeigt werden.
- **`web/i18n.json`**:
    - Ergänzung der Übersetzungen für "Bilder" und "ISO/Image" in Deutsch und Englisch.

## Verifizierung

Die funktionalität wurde durch eine neue Test-Suite `tests/test_media_categories.py` verifiziert.

**Testergebnisse:**
- ✅ **Audio**: Erkennt .mp3 korrekt.
- ✅ **Video**: Erkennt .mp4 als Film.
- ✅ **Hörbuch**: Erkennt .m4b und Pfad-Keywords.
- ✅ **ISO/Image**: Erkennt .iso und DVD-Inhalte.
- ✅ **Bilder**: Erkennt .jpg korrekt.

---

# 97 – Expanded Media Categorization

**Date:** March 10, 2026  
**Version:** 1.3.5  
**Status:** ✅ Completed

## Objective

Implementation of specific media categories for better differentiation and filtering in the UI. Focus on user-requested main categories: **Audio**, **Audiobook**, **Video**, **ISO/Image**, and **Images**.

## Implementation

### 1. Backend Enhancements (Python)

- **`parsers/format_utils.py`**: 
    - Introduction of `IMAGE_EXTENSIONS` for common image formats.
    - Updated `detect_file_format` to recognize images.
    - Fixed import order to prevent `NameError` during testing.
- **`media_format.py`**:
    - Adjusted `detect_type` to return the new standard categories.
    - Implemented heuristics for audiobook detection (based on `.m4b` extension or path keywords).
- **`models.py`**:
    - Synchronized `detect_logical_type` and `get_category` with the new categories.
    - Ensured `.iso` files are consistently classified as `ISO/Image`.

### 2. Frontend Integration (HTML/JS/i18n)

- **`web/app.html`**:
    - Expanded `specialCategories` list to ensure new categories are displayed as badges.
- **`web/i18n.json`**:
    - Added translations for "Images" and "ISO/Image" in German and English.

## Verification

The functionality was verified using a new test suite `tests/test_media_categories.py`.

**Test Results:**
- ✅ **Audio**: Correctly detects .mp3.
- ✅ **Video**: Correctly detects .mp4 as Film.
- ✅ **Audiobook**: Correctly detects .m4b and path keywords.
- ✅ **ISO/Image**: Correctly detects .iso and DVD content.
- ✅ **Images**: Correctly detects .jpg.
