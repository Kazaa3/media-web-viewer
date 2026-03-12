# Phase 4: Exotic Formats & NTSC/PAL Handling 🎞️

**Datum:** 12. März 2026

---

## Erweiterte technische Metadatenextraktion

### 1. Deep Technical Metadata Extraction
- **Exotic Fields:**
  - Scan Type
  - Chroma Subsampling
  - Color Space
  - HDR Format (HDR10, HLG)
- **Parser-Erweiterungen:**
  - `pymediainfo_parser.py`: Erfasst Standard, HDR_Format, ChromaSubsampling.
  - `ffprobe_parser.py`: Extrahiert pix_fmt und dekodiert chroma/bit-depth.

### 2. Standardisierte Labelling & NTSC/PAL
- **Format Detection:**
  - Technische Tags werden priorisiert.
  - Video-Dateien und ISOs erhalten Premium-Labels:
    - PAL DVD (Abbild)
    - NTSC DVD (Abbild)
    - HDR HDR10 Video
    - HDR HLG Video
    - Interlaced Video
    - 12 Bit Deep Color Video

### 3. Model & DB Integration
- **models.py:**
  - Metadata-Whitelist aktualisiert, neue technische Felder werden persistiert.

---

## Verifikation
- **verify_exotic_formats.py:**
  - HDR Video (10-bit): ✅ PASS
  - Interlaced Video (1080i): ✅ PASS
  - Deep Color Video (12-bit): ✅ PASS
  - PAL DVD ISO: ✅ PASS
  - NTSC DVD ISO: ✅ PASS
- **Format Helpers:**
  - Scan Type (Progressive): Progressive
  - Scan Type (Interlaced): Interlaced (TFF)
  - Chroma (420): 4:2:0
  - Chroma (422): 4:2:2
  - Color Info (HDR10): {'color_space': 'BT2020', 'hdr_format': 'HDR10', 'matrix': 'BT2020NC'}
  - Color Info (HLG): {'color_space': 'BT2020', 'hdr_format': 'HLG'}

---

## Performance Tracking
- Granulare Zeitmessung für alle Parser.
- Beispiel: ⏱️ Detailed Timings: pymediainfo: 0.010s, ffprobe: 0.079s, ffmpeg: 0.081s

---

*Entry created: 12. März 2026*
