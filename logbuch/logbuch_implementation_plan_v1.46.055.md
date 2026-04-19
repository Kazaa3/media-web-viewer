# Plan: Audio Player Repair & Forensic Synchronization

## Kontext
Nach erfolgreichem Systemscan (599 echte Items) ist das Ziel, den Audio Player für MP3-Wiedergabe zu reparieren und die Log-Ausgabe zu optimieren.

---

## User Review Required

### Wichtige Maßnahmen
- Fokus: "Black Hole"-Rendering im Audio Player beheben und HTML5-Audio-Pipeline robust initialisieren.

---

## Proposed Changes

### Audio Pipeline Hardening
#### [MODIFY] `audioplayer.js`
- `initAudioPipeline` um "Rescue Pulse" erweitern, der Events neu bindet, falls das Pipeline-Element bei Tab-Wechseln ersetzt/verloren geht.
- Granulares Error-Logging zu `pipeline.onerror` hinzufügen, um Browser-Decoding-Fehler gezielt zu erfassen.
- MIME-Type-Fallback in `playAudio` fixen.
- `crossorigin`-Attribute korrekt setzen.

#### [MODIFY] `main.py`
- `server_file_direct`-Route so anpassen, dass `bottle.static_file` Range-Requests für Audio korrekt behandelt.
- Fallback-MIME-Type für `.mp3` ergänzen (z.B. `audio/mpeg`).
- `accept-ranges: bytes` explizit setzen, um Seeking zu verbessern.

### UI Visibility (Nuclear Recovery)
#### [MODIFY] `nuclear_recovery_pulse.js`
- Recovery Pulse gezielt auf `audio-player-container` anwenden, Controls und Progressbar auf `visibility: visible` setzen.

### Log Optimization (Noise Reduction)
#### [MODIFY] `ffprobe_analyzer.py`
- `[Analyzer-Pulse] Forensic Subtype Detected` von `log.info` auf `log.debug` umstellen, um Log-Spam bei Scans zu vermeiden.

#### [MODIFY] `logger.py`
- UIHandler mit strikterem Rate-Limit: Cooldown, wenn >50 Logs/Sekunde eintreffen.

---

## Verification Plan

### Manual Verification
- Logs: Inkrementellen Scan starten, Konsole bleibt frei von "Forensic Subtype Detected"-Spam.
- Audio: MP3 abspielen, Fortschrittsbalken läuft, Ton hörbar.
- Trace: `[PLAY-PULSE]`-Logs prüfen, Route korrekt.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
