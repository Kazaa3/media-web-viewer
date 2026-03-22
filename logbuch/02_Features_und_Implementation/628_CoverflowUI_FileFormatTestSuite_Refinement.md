# Logbuch: Coverflow UI & File Format Test Suite – Refinement

**Datum:** 17. März 2026

## Zielsetzung
- Strukturierte Test-Suite für Dateiformate (Mock/Real Layer)
- Umbenennung des Library-Tabs zu "File / Datei"
- Coverflow-UI mit 3D-Depth und Tastatur-Navigation veredeln

---

## Änderungen & Umsetzung

### [Backend-Testing] Structured Test Suite
- **test_file_formats_suite.py**
  - **Mock Layer:**
    - Testet MetadataExtractor und Scanner-Logik mit gemockten OS-/Parser-Abhängigkeiten
  - **Real Layer:**
    - Testet echtes Filesystem-Scanning mit temporären Verzeichnissen und Dummy-Dateien
  - **Formate:**
    - Audio: MP3, FLAC, WAV, M4A, OGG
    - Video: MP4, MKV, AVI, MOV
    - Images
    - Disk Images: ISO, DVD-Ordner

### [Frontend-UI] Coverflow & Tab Refinements
- **app.html**
  - Tab-Benennung: "File / Datei" (technische Liste), "Library / Bibliothek" (Coverflow)
  - 3D-CSS: Reflexionen, Box-Shadow, Perspektive verbessert
  - Tastatur-Navigation (Links/Rechts/Enter) für Coverflow
- **i18n.json**
  - Fehlende Subkategorie-Filter-Keys ergänzt

---

## Verifikationsplan

### Automatisierte Tests
- `PYTHONPATH=. python3 tests/test_file_formats_suite.py`
- Mock- und Real-Layer müssen bestehen
- Alle Formate (Audio, Video, Disk) werden korrekt erkannt und mit Artwork versehen

### Manuelle Verifikation
- Tastatur-Navigation im Coverflow-Tab testen
- 3D-Effekte (Tiefe, Skalierung) auf verschiedenen Bildschirmgrößen prüfen
- Tab-Titel in Deutsch und Englisch kontrollieren

---

Weitere Details siehe vorherige Logbuch-Einträge und Testskripte.
