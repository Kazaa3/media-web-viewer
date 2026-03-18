# Logbuch – 18. März 2026

## Video Player Visibility & Sidebar Metadata Fixes

### Zusammenfassung der Verbesserungen

**1. Sidebar Synchronisierung:**
- Die Sidebar-Update-Logik wurde in eine gemeinsame Funktion ausgelagert: `updateMediaSidebar(item, path)`.
- Diese Funktion wird jetzt sowohl beim Audio- als auch beim Video-Playback aufgerufen.
- Ergebnis: Die Sidebar zeigt immer den aktuellen Filmtitel, das Artwork und die Metadaten korrekt an (vorher wurde manchmal die falsche Datei angezeigt).

**2. Erweiterte Seek Controls:**
- Im Bereich "Advanced Player Controls" wurde ein dedizierter Seek-Slider ergänzt.
- Zusätzlich gibt es Zeit-Labels für aktuelle Position und Gesamtdauer (z.B. 00:00 / 00:00).
- Die Controls sind mit dem Video.js-Player synchronisiert und erlauben komfortables Scrubbing durch das Video.

**3. UI-Verfeinerung:**
- Das Layout der Sidebar-"Format Details" wurde übersichtlicher gestaltet.
- Verbesserte Lesbarkeit und Struktur.

**4. Logging:**
- Erfolgreiche Umsetzung und Test dokumentiert.

### Testhinweise
- Vortrag.mp4 im Video-Player öffnen.
- Video wird korrekt angezeigt.
- Sidebar zeigt die richtigen Metadaten und das Cover.
- Seekbar und Zeitlabels funktionieren und sind synchron mit dem Player.

**Status:** Gefixt & verifiziert (18.03.2026)

---

## Weitere Fixes – 18. März 2026

**1. Duplicate Playback Trigger Fixed:**
- Das doppelte Öffnen des Video-Players (VLC-Popup) wurde behoben.
- Ursache: Sowohl die Metadaten-Update-Logik als auch die Video-Initialisierung riefen einen Backend-Play-Befehl auf.
- Lösung: `eel.play_media` wird jetzt nur noch für Audio-Dateien aufgerufen. Video-Dateien werden ausschließlich über die `playVideo`-Logik behandelt. Dadurch startet keine zweite VLC-Instanz mehr.

**2. Footer Status Message Formatting:**
- Fehlende Übersetzungen und Abstandsprobleme im Sticky Footer wurden gelöst.
- Explizite Abstände (`&nbsp;`) und robuste Fallbacks (z.B. "Spielt:" / "von") sorgen dafür, dass die Statusleiste immer lesbar bleibt, auch wenn Übersetzungs-Keys verzögert laden.

**3. ISO/DVD Playback:**
- .iso-Dateien werden weiterhin im Standalone-VLC (ISO-Modus) geöffnet, da Browser keine DVD-Menüs oder ISO-Container abspielen können.
- Das "Double-Open"-Problem ist jetzt auch für ISO-Dateien behoben.

**Test:**
- 4 Koenige.iso und Vortrag.mp4 getestet: Kein doppeltes Popup mehr, Footer-Status korrekt formatiert.

**Status:** Gefixt & verifiziert (18.03.2026)

---

## Dual-Layer Bounce Lock & Embedded ISO Playback – 18. März 2026

**1. Dual-Layer Bounce Lock:**
- **Frontend:** In `playVideo()` (JS) wurde ein 1-Sekunden-Debounce-Lock eingebaut, um versehentliche Doppelklicks und Mehrfach-Requests zu verhindern.
- **Backend:** In `open_video_smart()` (Python) gibt es jetzt einen globalen 1-Sekunden-Lock. Selbst wenn zwei Requests fast gleichzeitig eintreffen (z.B. durch verschiedene UI-Events), wird nur der erste ausgeführt.

**2. Embedded ISO Playback (FragMP4):**
- Die "Smart Auto-Routing"-Logik im Backend wurde erweitert:
    - Öffnet man eine .iso-Datei im Auto-Modus, wird sie jetzt durch die FragMP4-Pipeline geroutet.
    - Das ISO spielt direkt im eingebetteten Video-Player-Tab – kein Standalone-VLC-Popup mehr nötig.
- Standard-MP4/MKV-Dateien nutzen weiterhin ihren optimalen Pfad (Direct oder PIPE-KIT), ohne doppelte Instanzen.

**3. Trace Logging:**
- Detaillierte `DEBUG: [Player-Trace]`-Logs in Python und JavaScript hinzugefügt.
- Bei Problemen ist jetzt exakt nachvollziehbar, welche Funktion wann und warum ausgelöst wurde.

**Test:**
- ISO-Dateien werden direkt im Player abgespielt, kein doppeltes Öffnen mehr.
- Normale Videos funktionieren wie gewohnt.

**Status:** Gefixt & verifiziert (18.03.2026)

---

*Erstellt durch Antigravity (AI Assistant)*
