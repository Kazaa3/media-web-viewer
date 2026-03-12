# 98 – DVD-Ordner und Disk-Images (ISOs)

**Datum:** 10.03.2026  
**Version:** 1.3.6  
**Status:** ✅ Abgeschlossen

## Zielsetzung

Der Nutzer möchte, dass DVD-Ordnerstrukturen (mit/ohne ISOs) als einzelne "Film"-Objekte erkannt werden, statt als Sammlung einzelner Dateien (VIDEO_TS, etc.). Zudem soll eine klare Trennung zwischen "Bildern" (Fotos) und "Abbildern" (ISO/Disk Images) erfolgen.

## Umsetzung

### 1. Intelligente Ordner-Erkennung
- **`main.py`**: Der Scanner führt nun zwei Durchläufe aus. Im ersten Durchlauf werden "Medien-Ordner" identifiziert.
  - Erkennung von `VIDEO_TS` oder `BDMV` Unterordnern.
  - Erkennung von Ordnern, die direkt `.iso` Dateien enthalten.
- Diese Ordner werden als ein einziges `MediaItem` in die Datenbank aufgenommen. Alle Unterdateien dieser Pfade werden im zweiten Durchlauf übersprungen, um Duplikate zu vermeiden.

### 2. Kategorisierung & Naming
- **Kategorie "Abbild"**: Umbau von "ISO/Image" zu "Abbild" (Disk Image), um Verwechslungen mit Fotos zu vermeiden.
- **DVD/Blu-ray ISOs**: Werden automatisch als "Film" eingestuft, wenn sie Video-Inhalte repräsentieren.
- **Audio-Images**: SACDs und Audio-CD ISOs werden als "Album" kategorisiert.

### 3. Performance & Optimierung
- **`pycdlib` Integration**: Einsatz von `pycdlib` für den Metadaten-Zugriff auf ISOs. Dies ist signifikant schneller als herkömmliche Parser bei sehr großen Dateien (7GB+).
- **Benchmark**: Erstellung eines Benchmark-Scripts (`tests/benchmark_scanner.py`), um die Scan-Zeiten und Extraktions-Performance zu messen.

## Verifizierung

- ✅ **DVD-Ordner**: Wird als "Video/Film" erkannt.
- ✅ **7GB ISO**: Erfolgreich parsed mittels `pycdlib` ohne Timeout.
- ✅ **Disk Image vs. Bild**: Klare Trennung in der UI-Kategorie.

---

# 98 – DVD Folders and Disk Images (ISOs)

**Date:** March 10, 2026  
**Version:** 1.3.6  
**Status:** ✅ Completed

## Objective

The user requested that DVD folder structures (with/without ISOs) be recognized as single "Film" objects instead of a collection of individual files (VIDEO_TS, etc.). Furthermore, a clear distinction between "Images" (photos) and "Disk Images" (ISOs) was required.

## Implementation

### 1. Intelligent Folder Recognition
- **`main.py`**: The scanner now performs two passes. The first pass identifies "Media Folders".
  - Detection of `VIDEO_TS` or `BDMV` subfolders.
  - Detection of folders containing `.iso` files directly.
- These folders are added as a single `MediaItem` to the database. All sub-files within these paths are skipped in the second pass to avoid duplicates.

### 2. Categorization & Naming
- **Category "Disk Image"**: Renamed "ISO/Image" to "Disk Image" (Abbild) to avoid confusion with photos.
- **DVD/Blu-ray ISOs**: Automatically classified as "Film" if they represent video content.
- **Audio Images**: SACDs and Audio-CD ISOs are categorized as "Album".

### 3. Performance & Optimization
- **`pycdlib` Integration**: Used `pycdlib` for metadata access on ISOs. This is significantly faster than traditional parsers for very large files (7GB+).
- **Benchmark**: Created a benchmark script (`tests/benchmark_scanner.py`) to measure scanning time and extraction performance.

## Verification

- ✅ **DVD Folder**: Correctly recognized as "Video/Film".
- ✅ **7GB ISO**: Successfully parsed using `pycdlib` without timeout.
- ✅ **Disk Image vs. Photo**: Clear distinction in the UI category.
