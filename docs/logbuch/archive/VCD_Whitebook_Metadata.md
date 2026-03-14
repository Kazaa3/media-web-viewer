# VCD & Whitebook Standards: Metadata Extraction

**Datum:** 12. März 2026

---

## Unterstützung für VCD und Whitebook-Formate

### 1. VCD (Video CD)
- **Erkennung:**
  - Parser erkennt typische VCD-Strukturen (MPEGAV, CDI, EXT, SEGMENT).
  - Whitebook-konforme Dateisysteme werden identifiziert.
- **Metadaten:**
  - Extraktion von Disc-Typ (VCD 1.0, VCD 2.0, SVCD).
  - Erkennung von PAL/NTSC, MPEG-1 Video, Audio-Streams.
  - Erfassung von Track- und Segment-Informationen.

### 2. Whitebook Standards
- **Definition:**
  - Whitebook beschreibt das Format und die Struktur von Video-CDs.
- **Parser-Integration:**
  - Erweiterte Logik zur Erkennung und Extraktion von Whitebook-spezifischen Feldern.
  - Unterstützung für Mixed-Mode-CDs und interaktive Features (CDI).

### 3. Erweiterte Kompatibilität
- **Exotische Formate:**
  - Parser erkennt und behandelt auch SVCD, CD-i und Hybrid-Discs.
  - Fehlerrobuste Extraktion für seltene und gemischte Formate.

### 4. Verifikation
- **Automatisierte Tests:**
  - Testfälle für VCD, SVCD, CD-i und Whitebook-Discs.
  - Validierung der Metadaten und Format-Erkennung.

---

*Entry created: 12. März 2026*
