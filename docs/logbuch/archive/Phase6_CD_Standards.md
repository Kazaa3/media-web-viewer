# Phase 6: Official CD Standards & Proprietary Exclusion

**Datum:** 12. März 2026



## Bewertung: Antigarvit & Archivierung

- Für langfristige Archivierung und Kompatibilität sollten nur offizielle CD-Standards (White Book, Red Book, Yellow Book) verwendet werden.
- Proprietäre Formate (z.B. SVCD) sind nicht empfohlen und können in Zukunft schlechter unterstützt werden.

| Format | Standard | CD-Logo | Audio/Video | Codec |
|--------|----------|---------|-------------|-------|
| VCD    | White Book (offiziell) | ✅ Compact Disc | MPEG-1 Video | MPEG-1 Layer II |
| SVCD   | Proprietär | ❌ Kein CD-Logo | MPEG-2 Video | MPEG-1 Layer II |
| CD-DA  | Red Book (offiziell) | ✅ Compact Disc | Audio | PCM |
| CD-ROM | Yellow Book (offiziell) | ✅ Compact Disc | Daten | - |

---

## Proprietäre Standards
- Proprietäre Formate wie SVCD werden nicht als offizielle CD-Standards unterstützt.
- Nur White Book, Red Book und Yellow Book werden als "Compact Disc" mit Logo anerkannt.
- SVCD ist proprietär und besitzt kein offizielles CD-Logo.

---

## Parser-Logik
- Parser priorisieren offizielle Standards (VCD, CD-DA, CD-ROM).
- Proprietäre Formate werden erkannt, aber nicht als "offiziell" gelabelt.
- Keine proprietären Standards in der offiziellen Formatliste.

---

*Entry created: 12. März 2026*
