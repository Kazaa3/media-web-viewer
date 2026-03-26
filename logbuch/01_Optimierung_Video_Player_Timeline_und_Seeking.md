## Refactoring Video Player UI and Test Suite (26.03.2026)

**Goal Description**
Vereinfachung der Video Player UI durch Entfernen des horizontalen Splits/Sub-Tabs und Reorganisation von "Test-Artefakten" (fehlplatzierte Python-Skripte) in einen eigenen tests/scr-Ordner.

**Proposed Changes**

**Video Player UI Cleanup**
- [MODIFY] app.html: Entferne vlc-info Panel (Zeilen 6947-6962).
- Entferne active-engine-status-strip (Zeilen 6965-6981).
- Entferne vlc-extern-fallback-bar (Zeilen 6996-7023).
- Stelle sicher, dass player-main-content-pane den gesamten vertikalen Platz für das Video nutzt.

**Test Suite Reorganization**
- [NEW] tests/scr/: Ordner für Utility- und Maintenance-Skripte.
- [MOVE] src/core/test_media_factory.py → tests/unit/core/test_media_factory.py
- [MOVE] src/core/curate_logbuch*.py → tests/scr/
- [MOVE] src/core/fix_logbuch_numbers*.py → tests/scr/
- [MOVE] src/core/reorganize_logbuch.py → tests/scr/
- [MOVE] src/core/foundational_restoration.py → tests/scr/
- [MOVE] src/core/final_history_fix.py → tests/scr/
- [MOVE] src/core/final_history_polish.py → tests/scr/
- [MOVE] inspect_db.py → tests/scr/
- [MOVE] Ausgewählte Dateien aus scripts/ (z.B. gui_validator.py, performance_test.py) → tests/scr/

**Verification Plan**

*Automated Tests*
- pytest tests/ ausführen, um sicherzustellen, dass die Kern-Tests weiterhin bestehen.
- Überprüfen, dass die verschobenen Skripte weiterhin ausgeführt werden können.

*Manual Verification*
- Video Player Tab öffnen und prüfen, dass das Layout aufgeräumt, vollflächig und ohne Split/Info-Panels ist.
- Prüfen, dass das Klicken auf ein Video in der Audio-Playlist weiterhin korrekt zum bereinigten Video Player führt.
## Bug: Unerwünschter horizontaler Split im Video Player Tab (26.03.2026)

**Beschreibung:**
Im Video Player Tab sorgt ein Splitter-Element (`player-analytics-splitter`) zusammen mit dem rechten Bereich (`video-queue-pane`) für einen horizontalen Split der Ansicht. Dies führt zu einer unnötig geteilten Oberfläche und beeinträchtigt das immersive Videoplayer-Erlebnis.

**Geplante Lösung:**
- Entfernen des Splitter-Elements und des rechten Playlist-Bereichs.
- Der Player-Bereich soll die volle Breite erhalten und als einspaltige Ansicht dargestellt werden.
- Die Initialisierung des Splitters im JavaScript wird entfernt.

**Status:**
Umbau zur einspaltigen, aufgeräumten Video-Player-Ansicht ist geplant.
## Walkthrough: Video Player Integration and UI Enhancements (26.03.2026)

### Changes Made

#### Frontend (Web UI)
- **Automatic Video Detection:**
	- Die Funktion `playMediaObject` erkennt jetzt Video-Dateien anhand ihrer Kategorie (z.B. 'Film', 'Serie', 'ISO/Image') und Dateiendung (.mp4, .mkv, .iso).
- **Seamless Redirection:**
	- Ein Klick auf ein Video-Item wechselt automatisch zum Video-Player-Tab und startet die Wiedergabe.
- **Larger, Responsive Player:**
	- Der Video-Player nutzt jetzt den maximal verfügbaren Platz (`flex: 1`, `max-height: 85vh`).
	- `aspect-ratio: 16 / 9` sorgt für ein kinoreifes, responsives Layout.
	- Verbesserte Optik durch Farbverlauf und Schatten für "Premium-Feeling".
- **Layout Stability Fix:**
	- Rücknahme zu aggressiver Flexbox-Einstellungen, die zu leeren/broken Tabs führten. `overflow-y: auto` stellt sicher, dass alle Controls erreichbar bleiben.
- **Audio Queue Redirection:**
	- Klick auf MP4-Dateien in der Audio-Queue leitet jetzt korrekt zum Video-Player-Tab weiter.
- **Syntax Integrity:**
	- Syntaxfehler (fehlende Klammer) in `onPlaylistItemClick` behoben.

### Verification Results

#### Manual Verification
- **MP4 Playback:** Klick auf MP4 in der Bibliothek → Video-Tab, sofortige Wiedergabe im großen Fenster.
- **MKV Playback:** Gleiches Verhalten für MKV-Dateien.
- **ISO/DVD Support:** ISO/DVD triggern VLC/HLS-Backend und werden im Video-Tab angezeigt.
- **Tab Switching:** Video-Tab wird korrekt hervorgehoben.
- **PiP Mode:** Picture-in-Picture-Button funktioniert und öffnet das Video im schwebenden Fenster.
- **Standard Library UI:** Alle anderen Navigations- und Bibliotheksfunktionen bleiben intakt.

### Hinweis

Der Video-Player verwendet jetzt standardmäßig ein "Theater Mode"-Layout im Video-Tab für ein immersiveres Filmerlebnis.
# Logbuch: Optimierung Video Player Timeline und Seeking

## Ziel
Sicherstellung einer stabilen und reaktionsschnellen Timeline-Steuerung für alle Video-Player-Modi, insbesondere für transkodierte Streams und VLC-HLS-Einstufungen.

---

## Konzept
- Implementierung eines effizienten Event-Handlings für den Seek-Slider, um unnötige Backend-Restarts beim "Scrubbing" (Ziehen des Sliders) zu vermeiden.
- Trennung von UI-Feedback (Dragging) und tatsächlichem Seek-Commit (Release).

---

## Umsetzung
- **Event-Refactor**: `seekSlider` nutzt nun `input` für die Live-Anzeige der Zeit im UI und `change` für das tatsächliche Absenden des Seek-Befehls an den Player.
- **Backend-Schonung**: Durch den Wechsel auf `change` wird bei Streaming-Modis (VLC Embedded, FFmpeg Transcode) nur noch ein einziger Backend-Restart ausgelöst, statt hunderte während der Mausbewegung.
- **Transcode-Seeking**: Die Hot-Reload-Logik in `app.html` (Zusatz von `?ss=TIME`) wurde für native Streams und HLS verifiziert.

---

## Vorteile
- Massive Reduktion der Serverlast bei Nutzung der Timeline.
- Verhindert Port-Kollisionen und Subprozess-Staus durch zu viele gleichzeitige VLC/FFmpeg-Instanzen.
- Bessere User Experience durch flüssiges Zeit-Feedback während des Slidings.

---

## Status
- Erledigt / Implementiert

**Stand:** 26. March 2026

---

## Kontext & Verweise
- Scripts: `scripts/logbook_manager.py` (zur Erstellung genutzt)
- Code: `web/app.html` (Funktion `startEmbeddedVideo`, `seekVideo`)


---

## Task-Liste: Video Player Integration und PiP Support (26.03.2026)

1. Recherche: Aktuelle Media-Playback- und Tab-Switching-Logik analysieren
2. Recherche: Video Player-Implementierung und PiP-Fähigkeiten prüfen
3. Implementation Plan erstellen
4. Automatisches Tab-Switching zum Video-Tab für Video-Items implementieren
5. Video Player UI mit größerem Embedded-Window und PiP-Button verbessern
6. Funktionalität mit verschiedenen Formaten (MP4, MKV, ISO etc.) verifizieren
7. Walkthrough erstellen
8. Debugging: Sichtbarkeits- und Layout-Probleme des Video Players beheben
9. CSS/JS-Konflikte im Video-Tab beheben
10. Fix mit MP4 und anderen Formaten verifizieren
---

## Walkthrough: Video Player Integration and UI Enhancements (26.03.2026)

**Ziel:** Direkte Videowiedergabe aus der Item-Liste mit automatischer Weiterleitung zum großen, responsiven Video-Player-Tab und Picture-in-Picture (PiP)-Support.

### Änderungen (Frontend / Web UI)

- **Automatische Video-Erkennung:** Die Funktion `playMediaObject` erkennt Video-Dateien anhand Kategorie (z.B. 'Film', 'Serie', 'ISO/Image') und Extension (.mp4, .mkv, .iso).
- **Nahtlose Weiterleitung:** Ein Klick auf ein Video-Item schaltet automatisch auf den Video-Player-Tab um und startet die Wiedergabe sofort.
- **Größerer, responsiver Player:**
	- Der Video-Container nutzt jetzt den maximal verfügbaren Platz (flex: 1, max-height: 85vh).
	- aspect-ratio: 16 / 9 sorgt für ein kinoreifes, responsives Layout.
	- Verbesserte Optik durch subtilen Farbverlauf und tiefe Schatten für ein "Premium"-Gefühl.
- **Tab-Persistenz-Fix:** Die Funktion `switchTab` hebt den aktiven Tab-Button jetzt auch bei programmatischem Wechsel korrekt hervor.
- **PiP-Support:** Der Picture-in-Picture-Button ist geprüft und funktioniert konsistent im neuen UI.

### Verifikation

- **MP4-Playback:** Klick auf MP4-Datei in der Bibliothek → Weiterleitung zum Video-Tab, sofortige Wiedergabe im großen Fenster.
- **MKV-Playback:** MKV-Dateien lösen dieselbe Weiterleitung und Wiedergabe aus.
- **ISO/DVD-Support:** ISO- und DVD-Dateien triggern korrekt das VLC/HLS-Backend und werden im Video-Tab angezeigt.
- **Tab-Switching:** Der Video-Tab-Button wird beim Klick auf ein Item korrekt hervorgehoben.
- **PiP-Mode:** Der PiP-Button öffnet das Video erfolgreich als schwebendes Fenster.
- **Standard-Library-UI:** Alle anderen Navigations- und Bibliotheksfunktionen bleiben intakt.

**Hinweis:**
Der Video-Player verwendet jetzt im Video-Tab standardmäßig ein "Theater Mode"-Layout für ein immersiveres Erlebnis bei Filmen und Serien.
---

## Implementation Plan: Video Player Integration and UI Enhancements (26.03.2026)

**Ziel:** Nahtloser Übergang von der Item-Liste zum Video-Player für Video-Dateien (MP4, MKV, ISO etc.) mit großem Embedded-Player und Picture-in-Picture (PiP)-Support.

### Vorgeschlagene Änderungen (web/app.html)

- **Automatisches Tab-Switching:**
	- `playMediaObject(item)` erkennt Video-Dateien anhand Kategorie ('Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos') oder Extension (.mp4, .mkv, .iso, .webm, .avi, .mov, .ts).
	- Bei Video: Umschalten auf den Video-Player-Tab (`multiplexed-media-player-orchestrator-panel`) und Aufruf von `playVideo(item, item.path)`.
- **UI-Verbesserungen:**
	- Video-Container (`coordinated-media-renderer-pipeline-viewport`) wird responsiv (aspect-ratio: 16/9 oder flex: 1).
	- PiP-Button wird geprüft, gestylt und als Premium-Element hervorgehoben.
	- Standard-Mediaelement-Support wird sichergestellt.

### Verifikationsplan

- Automatisierte Tests (Selenium) für Video-Playback prüfen/anpassen.
- `scripts/logbook_manager.py lint` zur Logbuch-Konsistenz nach Änderungen ausführen.
- Manuelle Tests: Verschiedene Videoformate aus Item-Liste starten, Tab-Switch und Player-Fenster prüfen, PiP-Button testen, Audio-Playback weiterhin korrekt.

Diese Maßnahmen werden als nächstes umgesetzt und im Logbuch dokumentiert.
---

## Review & Feedback zum Implementation Plan (26.03.2026)

1. **Detection Criteria für Video-Items (Extensions & Kategorien):**
	- Die vorgeschlagenen Extensions (.mp4, .mkv, .iso, .webm, .avi, .mov, .ts) sind sehr umfassend und decken die gängigen Videoformate ab. Optional könnten noch .mpeg, .mpg, .wmv ergänzt werden, falls im Bestand vorhanden.
	- Die Kategorien ('Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos') sind sinnvoll gewählt. Falls es noch weitere relevante Kategorien gibt (z.B. 'Konzert', 'Dokumentation'), könnten diese ergänzt werden – das hängt aber von der Datenstruktur ab.

2. **UI-Enhancements für das große Video-Fenster:**
	- Die geplante responsive Gestaltung (aspect-ratio, flex) ist Best Practice.
	- Für ein „Premium“-Erlebnis werden folgende Media-Elemente/Controls empfohlen:
	  - Play/Pause, Seekbar, Lautstärke, Mute, Fullscreen, PiP, Zeit/Restzeit-Anzeige
	  - Optional: Download-Button, Untertitel/Sprachwahl, Quality-Switch (falls mehrere Streams)
	  - Keyboard Shortcuts (z.B. Space für Play/Pause)
	  - Visuelles Feedback bei PiP-Aktivierung
	- Prüfen, ob Accessibility (z.B. ARIA-Labels) und Touch-Support für mobile Geräte gegeben sind.

3. **Automatisches Umschalten auf Video-Tab:**
	- Der Video-Tab sollte für alle Videoformate inkl. DVD/ISO automatisch aktiv werden, sobald ein entsprechendes Item gewählt wird. Das sorgt für ein konsistentes Nutzererlebnis.

**Fazit:**
Der Plan ist sehr gut und praxisnah. Die Detection-Logik ist robust, die UI-Verbesserungen sind sinnvoll und zukunftssicher. Die genannten Ergänzungen sind optional und können je nach Bedarf umgesetzt werden.

Bei Bedarf kann eine Checkliste für Media-Controls oder ein Beispiel für die Format-Erkennung bereitgestellt werden.
# 01_Optimierung_Video_Player_Timeline_und_Seeking

**Datum:** 26. März 2026

## Zusammenfassung

Im Rahmen der heutigen Sitzung wurden folgende Optimierungen und Anpassungen am Video-Player und der UI vorgenommen:

### 1. Layout-Anpassungen (Sidebar & Tabs)
- **Permanente Sidebar-Ausblendung:** Die Main Sidebar (links) wird in den Tabs Bibliothek, Item, Datei, Edit und Optionen grundsätzlich ausgeblendet. Diese Tabs nutzen nun die volle Bildschirmbreite für eine bessere Übersicht.
- **Exklusivität:** Die Sidebar mit Artwork und Metadaten ist exklusiv dem Player-Tab vorbehalten.
- **Header- & Footer-Bereinigung:** Die Option "Minimal-Player Ansicht" steuert jetzt gezielt das Ausblenden der Navigations-Tabs und der Statusleiste im Player-Modus für ein minimalistisches Wiedergabe-Erlebnis.

### 2. Video-Player Optimierungen (Timeline & Seeking)
- **Effizientes Seeking:** Der Seek-Slider unterscheidet jetzt zwischen Ziehen (input) und Loslassen (change). Die Zeit wird beim Ziehen live im UI aktualisiert, der eigentliche Seek-Befehl wird erst beim Loslassen ausgelöst.
- **Serverlast-Reduktion:** Verhindert das massenhafte Spawnen von VLC/FFmpeg-Subprozessen während des Scrubbings und erhöht die Stabilität.
- **Kompatibilitäts-Fix:** Ergänzung fehlender CSS-Eigenschaften für den Slider für einheitliche Darstellung in verschiedenen Browsern.

### 3. Logbuch-Management
- Neuer Eintrag dokumentiert die heutigen Optimierungen und dient als Referenz für zukünftige Audits.

---

Die Anwendung ist nun robuster und benutzerfreundlicher in Navigation und Medienwiedergabe.

---

## 4. Geplante Erweiterung: Video-Playback aus der Item-Liste

- **Direktes Abspielen von Videos:** Künftig soll das Starten von Videos (MP4, DVD/ISO, MKV etc.) direkt aus der Item-Liste möglich sein. Ein Klick auf ein Video-Item wechselt automatisch in den Video-Player-Tab.
- **Großes Embedded-Video-Fenster:** Im Player-Tab wird ein großes, zentriertes Video-Element angezeigt, das moderne Features wie Picture-in-Picture (PiP) und MediaElement-Controls unterstützt.
- **User Experience:** Ziel ist ein nahtloser Übergang von der Medienauswahl zur Wiedergabe, unabhängig vom Dateityp.

Diese Erweiterung ist in Planung und wird als nächster Schritt umgesetzt.

---

## 5. Implementation Plan: Video Player Integration und UI-Verbesserungen

**Ziel:** Nahtloser Übergang von der Item-Liste zum Video-Player für Video-Dateien (MP4, MKV, ISO etc.) mit großem Embedded-Player und Picture-in-Picture (PiP)-Support.

### Geplante Änderungen (web/app.html)

- **Automatisches Tab-Switching:**
	- `playMediaObject(item)` erkennt Video-Dateien anhand Kategorie ('Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos') oder Extension (.mp4, .mkv, .iso, .webm, .avi, .mov, .ts).
	- Bei Video: Umschalten auf den Video-Player-Tab (`multiplexed-media-player-orchestrator-panel`) und Aufruf von `playVideo(item, item.path)`.
- **UI-Verbesserungen:**
	- Video-Container (`coordinated-media-renderer-pipeline-viewport`) wird responsiv (aspect-ratio: 16/9 oder flex: 1).
	- PiP-Button wird geprüft, gestylt und als Premium-Element hervorgehoben.
	- Standard-Mediaelement-Support wird sichergestellt.

### Verifikationsplan

- Automatisierte Tests (Selenium) für Video-Playback prüfen/anpassen.
- `scripts/logbook_manager.py lint` zur Logbuch-Konsistenz nach Änderungen ausführen.
- Manuelle Tests: Verschiedene Videoformate aus Item-Liste starten, Tab-Switch und Player-Fenster prüfen, PiP-Button testen, Audio-Playback weiterhin korrekt.

Diese Maßnahmen werden als nächstes umgesetzt und im Logbuch dokumentiert.

Weitere Optimierungen gerne melden!
