# Walkthrough: Integrated Web Player & Streaming

**Datum:** 12. März 2026

---

## Überblick
Wir haben eine vollständig integrierte Web-Player-Erfahrung implementiert, die externe Abhängigkeiten ersetzt und nahtlose In-Browser-Wiedergabe ermöglicht.

---

### 1. Backend Streaming Engine
- **app_bottle.py:**
  - Neue Route `/video-stream/` hinzugefügt.
  - FFmpeg liefert einen Live-Stream als fragmented MP4.
  - Optimiert für niedrige Latenz mit `-preset ultrafast` und `-tune zerolatency`.
  - ISO/DVD-Unterstützung: Routing über FFmpeg oder nativen Fallback.

    - MKVInfo (CLI): Für MKV-Metadatenextraktion wird das Standard-CLI mkvinfo als Fallback genutzt.
      - Beispiel: `mkvinfo /pfad/zur/datei.mkv` gibt strukturierte Metadaten aus.
      - Integration: Die Parser-Architektur nutzt mkvinfo, wenn mkvmerge nicht verfügbar ist.

### 2. Frontend Player Selection
- **app.html:**
  - Selektierbarer Player-Modus im Video-Tab.
  - Chrome Native: Direkte Wiedergabe kompatibler Formate.
  - VLC Integrated (Stream): Live-Transkodierung und Streaming für MKV, ISO und komplexe Formate.
  - VLC (Extern): Option zum Starten des externen VLC-Players.

### 3. Localization & UI Polish
- **i18n.json:**
  - Neue Labels für Player-Modi (Deutsch/Englisch).
  - Verbesserte Video-Player-UI mit besserem State-Handling und Platzhalter-Übergängen.

### 4. Dependency & Environment Fixes
- **Environment Hygiene:**
  - Kritischer Fix: .venv_core enthielt fehlende Abhängigkeiten.
  - Installation aller Pakete aus requirements-core.txt (inkl. eel, bottle, mutagen, gevent, etc.) in .venv_core.
  - Startup Protection: mutagen-Fehler behoben, der den Start verhinderte.

### 5. Click-to-Play Functionality
- **Smart Redirection:**
  - Automatisches Öffnen des Video-Player-Tabs beim Klick auf ein Video-Item.
  - ISO-Support: .iso als Video-Erweiterung erkannt, integrierte Wiedergabe für DVD-Images.
  - Verbesserte Tab-Navigation mit Element-IDs.

---

## Ultimate Mode & Tag Saving
- **Ultimate Mode Scan:**
  - Neuer Deep-Scan-Modus: 100% Roh-Metadaten aus allen Parsern (VLC, Mutagen, FFprobe, MKVMerge) werden in full_tags gespeichert.
- **Tag Persistence:**
  - Bearbeitete Metadaten können direkt in Mediendateien gespeichert werden.
  - Unterstützte Formate: MP3, FLAC, M4A/MP4 (Mutagen), MKV (MKVToolNix).
- **UI Integration:**
  - "Save to File"-Button im Metadata Editor.
  - Workflow mit Erfolg-/Fehlerbenachrichtigung.
  - Automatische Schema-Migration für das full_tags-Feld.

---

## Enhanced Metadata Parsers
- **MKVMerge (JSON):** Zuverlässige Metadatenextraktion mit `mkvmerge -J`.
- **MKVInfo (CLI):** Fallback mit Standardausgabe.
- **VLC (libvlc):** Universelle Metadaten (Titel, Artist, Dauer, etc.).
- **Smart Integration:** media_parser.py priorisiert diese Tools für MKV und andere Medien.
- **User Interface:** Alle neuen Parser in den Settings konfigurierbar.

---

## Streaming & Player
- **libx264:** Verfügbar für hochwertige, latenzarme H.264-Kodierung.
- **Fragmented MP4:** `frag_keyframe+empty_moov` für Streamability in Chromium.
- **UI Interaction:** Player-Modus kann dynamisch gewechselt werden; Routing erfolgt je nach Modus.

---

## Zusammenfassung
Die Anwendung bietet jetzt eine professionelle, integrierte Medienwiedergabe. Externe Fenster sind nicht mehr nötig, selbst komplexe Formate wie ISO/DVD können direkt im Web-Interface gestreamt werden.

---

*Entry created: 12. März 2026*
