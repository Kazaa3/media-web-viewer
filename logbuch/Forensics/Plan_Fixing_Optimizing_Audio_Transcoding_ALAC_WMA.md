# Plan - Fixing and Optimizing Audio Transcoding (ALAC/WMA)

## Ziel
Nicht-funktionale ALAC- und WMA-Transcodierung wird behoben, ein Attributfehler in models.py gefixt und die Performance von Audio-Only-Streams durch strikte Trennung vom Video-Pfad optimiert.

---

## User Review Required
**WICHTIG**

- Strikte Trennung der Audio- und Video-Transcode-Kommandos in main.py für maximale Performance.
- Für ALAC (Lossless): Standardmäßig Transcodierung zu FLAC (Qualitätserhalt), Fallback zu AAC falls Browser kein FLAC kann.
- Für WMA (Lossy): Standardmäßig Transcodierung zu Opus oder AAC.

---

## Vorgeschlagene Änderungen

### [Component: Data Models]
**models.py**
- **Fix Identity Logic:** Ersetze das nicht existierende `self.type` durch `self.path.suffix.lower()` in `to_dict`, um ALAC und WMA korrekt zu erkennen.
- **Update Transcode Flags:** Setze `is_transcoded` für alle Formate aus AUDIO_TRANSCODE korrekt.

### [Component: Configuration]
**config_master.py**
- **Audio Transcode Profiles:** Definiere spezifische Profile für ALAC→FLAC und WMA→Opus/AAC für optimale Qualität und Performance.

### [Component: Streaming Engine]
**main.py**
- **Separate Audio/Video Command Building:** Refaktorisiere `stream_video_fragmented`, sodass früh zwischen Audio und Video getrennt wird.
- **Fix Content-Type:** Setze den Content-Type-Header dynamisch je nach Stream-Typ.
- **Optimize FFmpeg Parameters:** Nutze `-vn` und optimierte Buffer für Audio-Only-Streams zur CPU-Entlastung.

---

## Offene Fragen
- Soll ALAC immer zu AAC transkodiert werden (maximale Kompatibilität) oder bevorzugt zu FLAC (bessere Qualität, aber evtl. nicht überall unterstützt)?
- Gibt es eine WMA-Version (z.B. Pro, Lossless), die priorisiert werden soll, oder sollen alle WMA als lossy→Opus behandelt werden?

---

## Verifizierungsplan
### Automatisierte Tests
- Testskript `/tmp/test_audio_transcode.py` simuliert FFmpeg-Kommandos für ALAC und WMA und prüft, ob valide Streams entstehen.
- Mit ffprobe das Format und die Bitrate der transkodierten Streams prüfen.

### Manuelle Verifikation
- In der UI prüfen, ob ALAC und WMA jetzt den "Transcode"-Status anzeigen.
- Wiedergabe eines ALAC-Files im Browser-Player testen.

---

## Implementation Plan (Zusammenfassung)
- **Identity Bug:** models.py nutzt künftig `self.path.suffix` statt `self.type` zur Identifikation.
- **Performance:** Audio- und Video-Transcode werden strikt getrennt, Audio-only nutzt leichtgewichtige FFmpeg-Profile.
- **Content-Type:** Streaming-Header werden dynamisch gesetzt, um Browser-Kompatibilität zu sichern.

Bitte Rückmeldung geben, ob FLAC oder AAC als ALAC-Ziel bevorzugt wird und wie WMA behandelt werden soll.