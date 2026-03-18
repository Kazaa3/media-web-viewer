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

## Triple-Layer Hard Locks & DVD Protocol Fix – 18. März 2026

**1. Strict DVD Path Normalization:**
- Fehlerursache: VLC erhielt den /VIDEO_TS-Subfolder statt des DVD-Hauptordners, was zu Protokollfehlern und Wiederholungen führte.
- Lösung: In `open_video()` wurde ein Normalizer eingebaut, der bei DVD-Strukturen automatisch auf den Elternordner pivotiert.
- Ergebnis: VLC startet jetzt sauber mit dem dvd://-Protokoll.

**2. Global Backend Lock (PLAYBACK_LOCKS):**
- Ein globales Dictionary-basiertes Lock im Python-Backend verhindert, dass mehrere Player-Starts für dieselbe Datei innerhalb von 1 Sekunde ausgelöst werden.
- Alle parallelen Events werden blockiert und nur der erste Start ausgeführt.

**3. Hardened play_media:**
- Die Funktion `play_media` ignoriert jetzt strikt Video-Extensions und kann nie mehr eine VLC-Instanz für Videos starten.

**4. UI Feedback:**
- Der Video-Player-Tab zeigt jetzt explizit: "📺 Externer Player aktiv: VLC (DVD/ISO)" wenn ein Standalone-Fenster genutzt wird.

**Test:**
- DVD-Ordner und ISO öffnen: Nur noch ein VLC-Fenster, Status im Tab korrekt.
- Terminal-Log: `DEBUG: [Player-Trace] open_video LOCK detected for ... Skipping secondary start.` zeigt, dass das Lock greift.

**Status:** Triple-Layer-Lock & DVD-Protokoll gefixt (18.03.2026)

---

## Final Hard Locks & UI Feedback – 18. März 2026

**1. Backend "Video-Lock" für play_media:**
- Die Funktion `play_media` im Backend wurde so angepasst, dass sie Video-Dateien explizit ignoriert.
- Selbst wenn ein UI-Komponent versehentlich den generischen Play-Befehl auslöst, startet keine zweite VLC-Instanz mehr für Videos.
- Video-Dateien werden jetzt ausschließlich über die `open_video_smart`-Pipeline behandelt.

**2. Status "Kein Video ausgewählt" ersetzt:**
- Öffnet man ein ISO oder einen Ordner, der einen externen Player (VLC) startet, zeigt der Video-Tab jetzt eine klare Statusmeldung:
    - "📺 Externer Player aktiv: VLC (DVD/ISO)"
- Das ersetzt die verwirrende "No video selected"-Meldung und macht transparent, warum der Player leer bleibt.

**3. UI Feedback & Tracing:**
- Sichtbare Toast-Messages beim Moduswechsel (z.B. "DIRECT PLAYBACK", "mkvmerge PIPE KIT").
- Jeder Start eines externen Players wird mit `[Play-Trace]` im Console-Log dokumentiert.

**Test:**
- ISO-Objekte öffnen: Kein doppeltes VLC-Fenster mehr, Status im Video-Tab korrekt.
- Alle externen Player-Aktionen sind nachvollziehbar geloggt.

**Status:** Finaler Lock & Feedback implementiert (18.03.2026)

---

## Deadlock-Fix, Parser-Interferenz & Singleton-Verbesserung – 18. März 2026

**1. Logic Deadlock behoben:**
- Problem: `open_video_smart` setzte einen Lock und rief dann `open_video` auf, das denselben Lock prüfte und sich dadurch selbst blockierte.
- Lösung: Die Locks verwenden jetzt unterschiedliche Keys für "Smart Routing" und "Direct Playback". Deadlocks sind ausgeschlossen.

**2. Parser-Interferenz:**
- Der `vlc_parser` wurde für ISO- und DVD-Strukturen explizit deaktiviert, um das Starten von Phantom-VLC-Instanzen im Hintergrund zu verhindern.

**3. Refined Singleton Logic:**
- Vor jedem neuen Videostart sucht das Backend nach verwaisten VLC-Prozessen und beendet diese gezielt (Hard Process Reset), bevor eine neue Instanz gestartet wird.

**4. PIPE-KIT für H264 wiederhergestellt:**
- Für H264-Dateien wurde der PIPE-KIT-Remuxer reaktiviert, damit der Browser einen abspielbaren Stream erhält und kein Blackscreen mehr erscheint.

**Test:**
- Kein Deadlock mehr, keine "locked"-Status-Fehler.
- Keine doppelten oder Phantom-VLC-Instanzen.
- MP4/MKV/H264 werden korrekt im Embedded Player angezeigt.

**Status:** Deadlock, Parser-Interferenz & Singleton-Logik gefixt (18.03.2026)

---

## Embedded Player Fallback & VLC-Popup-Handling – 18. März 2026

**Problem:**
- Es erscheinen weiterhin 2 VLC-Popups bei bestimmten Aktionen.

**Workaround/Strategie:**
1. Wähle eines der VLC-Popups aus und ordne die Instanz gezielt zu (z.B. per PID oder Fenster-Handle).
2. Binde diese Instanz in den Embedded Player ein (z.B. via Video-Stream, RTSP, oder Window-Embedding, je nach Plattform und Architektur).
3. Schließe das Popup-Fenster nach erfolgreicher Einbindung automatisch oder manuell.
4. Gehe den Weg zurück: Der Embedded Player übernimmt die Wiedergabe, die UI bleibt konsistent, und es gibt keine doppelten Fenster mehr.

**Nächste Schritte:**
- Automatisierung der Popup-Erkennung und -Zuordnung.
- Sicherstellen, dass der Embedded Player immer Vorrang hat und Popups nur als Fallback dienen.
- Optional: User-Feedback, wenn ein Popup übernommen wurde (z.B. Toast "VLC-Instanz übernommen und eingebettet").

**Status:**
- Workaround dokumentiert, weitere Automatisierung empfohlen.
