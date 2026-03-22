# Phase 3: ISO Metadata Extraction Expansion (pycdlib)

**Datum:** 12. März 2026

---

## Erweiterungen & Verbesserungen

### 1. Extended PVD Metadata
- Extrahiert jetzt:
  - Volume ID
  - Publisher
  - Application ID
  - Preparer ID

### 2. Smart Date Formatting
- Volume-Erstellungsdaten werden automatisch als ISO-Timestamps ausgegeben.

### 3. Disc Content Detection
- **DVD-Video:** ISO wird automatisch als DVD-Video erkannt, wenn VIDEO_TS vorhanden.
- **Blu-ray:** ISO wird automatisch als Blu-ray erkannt, wenn BDMV vorhanden.

### 4. Support Flags
- Erkennt und meldet:
  - Joliet
  - Rock Ridge
  - UDF Extensions

### 5. Bulletproof Compatibility
- Robuste Decoding-Layer für pycdlib-Objekte:
  - Unterstützt FileOrTextIdentifier und VolumeDescriptorDate Klassen.
  - Versionstolerant für pycdlib-Updates.

### 6. Exotic Formats & NTSC Handling
- Erweiterte Erkennung und Handling für NTSC und andere exotische Dateiformate.
- Dokumentation und technische Details im Walkthrough.

---

*Entry created: 12. März 2026*
