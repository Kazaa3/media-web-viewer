# Redbook (Audio CD) Metadata Extraction

**Datum:** 12. März 2026

---

## Unterstützung für Redbook-Formate (Audio CD)

### 1. Redbook Standard
- **Definition:**
  - Redbook spezifiziert das Format für Audio-CDs (CD-DA).
  - PCM-Audio, 16-bit, 44.1 kHz, Stereo.

### 2. Erkennung & Extraktion
- **Parser erkennt:**
  - TOC (Table of Contents)
  - Track-Informationen (Nummer, Länge, Start/Ende)
  - CD-Text (Titel, Künstler, Album, falls vorhanden)
  - ISRC-Codes (International Standard Recording Code)
- **Metadaten:**
  - Extraktion von Track- und Disc-Informationen
  - Erkennung von Pre-Gap, Hidden Tracks, Index-Punkten

### 3. Kompatibilität & Fehlerbehandlung
- **Exotische Features:**
  - Unterstützung für Multi-Session-CDs, CD-Extra (Enhanced CD)
  - Fehlerrobuste Extraktion bei beschädigten oder ungewöhnlichen Discs

### 4. Verifikation
- **Automatisierte Tests:**
  - Testfälle für Standard- und Sonder-CDs
  - Validierung der Metadaten und Format-Erkennung

---

*Entry created: 12. März 2026*
