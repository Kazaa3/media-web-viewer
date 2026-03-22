# Verbesserungen: Video-Playback & UI-Integration

**Datum:** 15.03.2026

## Key Changes

### 1. Drag & Drop im Video-Player-Tab
- "Drag & Drop (Extern)" als 6. Option im Video-Modus-Selector integriert.
- Bei Auswahl erscheint eine zentrale Dropzone, der integrierte Player wird ausgeblendet.
- Dateien, die hier abgelegt werden, werden sofort extern in VLC geöffnet.
- Die "VLC Ribbon"-Buttons am unteren Rand wurden entfernt – UI ist jetzt klarer.

### 2. Chrome Native Video Playback
- "Chrome Native" ist jetzt der Standardmodus.
- Kritischer Bug behoben: Chrome blockierte lokale Dateien (z. B. /home/xc/...) wegen Sicherheitsrichtlinien.
- Lösung: Die App streamt lokale Dateien über eine /media/-Bridge direkt in den Browser, ohne Transcoding, performant und kompatibel.

### 3. UI & Diagnostik vereinheitlicht
- "VLC Stream"-Bereich aufgeräumt und fokussiert.
- Der Button "In VLC öffnen" wird je nach Modus korrekt ein-/ausgeblendet (nicht sichtbar in Chrome Native und D&D).
- Fehlende Lokalisierungsschlüssel für video_mode_chrome und video_mode_dnd ergänzt (Deutsch/Englisch).

### 4. Navigation verbessert
- "In VLC öffnen" schaltet jetzt direkt in den VLC-Modus und öffnet das Video extern in einem Schritt.

## Verifikation: Chrome Native
- Ein Klick auf ein Video in der Bibliothek spielt es direkt im eingebetteten Player (Chrome Native).
- Nicht unterstützte Codecs: Einfach auf "FFmpeg Engine → Chrome" oder "Drag & Drop" (VLC) umschalten.

---

**Ergebnis:**
- Video-Playback und UI sind jetzt nahtlos, intuitiv und flexibel – für alle gängigen Formate und Workflows.
