# Phase 6: Comprehensive Media Support & Playability Logic

**Datum:** 12. März 2026

---

## Überblick
Die Implementierungsplanung wurde auf Phase 6 erweitert, um fortgeschrittene Datenträger-Erkennung und Playability-Logik zu integrieren.

---

### 1. Erweiterte Datenträger-Erkennung
- **Legacy Video:**
  - VCD und andere Video-CD-Formate werden zuverlässig identifiziert.
- **ISO-Metadaten:**
  - pycdlib-Parser wurde um Marker für Konsolen und VCD erweitert.

---

### 2. Playability-Filter
- **Logik:**
  - PC-Spiele und reine Daten-ISOs werden nur indexiert, nicht als abspielbar markiert.
  - ISO-Filme und Video-CDs bleiben im Player abspielbar.
- **MediaItem-Modell:**
  - Playability-Logik im Modell integriert.
  - Helper-Funktion `is_playable` in format_utils.py hinzugefügt.

---

### 3. UI-Anpassung
- **Unterscheidung:**
  - UI zeigt klar, welche Medien abspielbar sind und welche nur indexiert werden.

---

### 4. Aufgaben & Fortschritt
- pycdlib-Parser für Konsolen/VCD erweitert
- detect_file_format mit Playability-Logik aktualisiert
- is_playable-Helper in format_utils.py und MediaItem
- UI-Update für Playability
- Tests und manuelle Verifikation

---

*Entry created: 12. März 2026*

## Hinweis: Fehlerhandling & Proprietäre Formate

- Es ist wichtig, Fehler beim Parsen und Indexieren sauber abzufangen, damit die Medienbibliothek robust bleibt.
- Proprietäre Formate sollten möglichst nicht aufgenommen werden, da sie langfristig schlechter unterstützt und weniger kompatibel sind.
