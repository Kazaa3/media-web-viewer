# Logbuch Meilenstein: Erweiterung Technische Metadaten (v1.35.68)

## Ziel
Vervollständigung der Premium-Sidebar durch zusätzliche technische Metadaten: File Type und Media Container neben Codec.

---

## Neue Features

### 1. File Type Identifier
- Zeigt die Medienkategorie (z.B. Audio, Video, Audiobook) für schnellen Kontext

### 2. Media Container Support
- Separates Tracking des Dateiformats (z.B. MP4, Matroska, FLAC, MP3) unabhängig vom Codec
- Fallback auf Dateiendung, falls Container-Tag fehlt

### 3. Dynamic Sync
- updateMediaSidebar hydratisiert File Type und Container dynamisch während der Wiedergabe
- Automatische Aktualisierung bei Track-Wechsel

### 4. Verbesserte Layout-Logik
- "Tech Box" nutzt flex-wrap für perfekte Ausrichtung auch bei hoher Informationsdichte

---

## Verifikation
- File Type, Container und Codec werden korrekt angezeigt
- Fallback auf Extension funktioniert
- UI bleibt lesbar und responsiv

---

**Meilenstein abgeschlossen: Erweiterung Technische Metadaten (v1.35.68)**
