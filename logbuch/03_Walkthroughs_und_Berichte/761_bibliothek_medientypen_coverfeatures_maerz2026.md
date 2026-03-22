# Bibliothek-Ansicht: Medien-Typen & Cover-Features – März 2026

## Ziel
Die Bibliothek wurde um folgende Medientypen und Ansichten erweitert:
- Film (Objekt)
- Album
- Compilation
- Serie
- Video
- später noch diverse weitere (Audio,Soundtrack, Podcast, Klassik, Playliste, Doku, TV)

## Features & Umsetzung
### 1. Film
- Zeigt Filmcover mit Dropdown oben rechts:
  - Filmcover Deutsch
  - Filmcover Englisch
  - Filmcover Originalversion
  - DVD Cover (de/en/original)
  - Blu-ray Cover (de/en/original)
  - Audio-CD Cover (original)
- Dropdown-Menü ermöglicht Auswahl der gewünschten Cover-Ansicht des Film-Unterreiter-Menüs aus diesen Auswahlmöglichkeiten.

### 2. Audio (Album/Compilation)
- Verwendet automatisch das Cover aus dem jeweiligen Ordner (folder.png/jpg/cover).

### 3. Video
- Ansicht ähnlich Videoplattformen: Grid/Kachel mit Vorschaubild (Thumbnail).
- Bei Mouseover läuft das Video im Kachel-Player, Seekbar sichtbar, Ton optional schaltbar.
- Cover/Thumbnail kann ein spezielles Bild oder ein Frame aus dem Video sein; später auch aus DVD-Menü extrahierbar.

## Technische Hinweise
- Neue Datenstrukturen und UI-Komponenten für die Medientypen implementiert.
- Cover-Auswahl und Video-Preview als interaktive UI-Elemente realisiert.
- Backend liefert für jeden Medientyp die passenden Cover- und Vorschaubilder.

## Fix Footer, Tabs, and Startup Speed (März 2026)

### Ziel
Mehrere UI- und Performance-Probleme im gui_media_web_viewer beheben:
- Audio-Player-Footer immer sichtbar und nicht überlappend
- Tabstruktur: Parser, Debug, Tests als eigenständige Hauptreiter
- Startup-Optimierung: UI-Start priorisieren, Blockaden vermeiden

### Umsetzung
#### UI Fixes (web/app.html)
- **Audio Player Footer:**
  - `.player-container` auf `position: fixed; bottom: 0; left: 0; right: 0;` gesetzt
  - `body { padding-bottom: ... }` ergänzt, damit Content nicht hinter Footer verschwindet
- **Tabstruktur (DIV-Balance):**
  - Extra `</div>` entfernt, um die Balance (574/574 oder 575/575) herzustellen
  - Parser, Debug, Tests als unabhängige Tabs auf Top-Level-Ebene gerendert

#### Startup-Optimierung (src/core/main.py)
- **UI-Start priorisieren:**
  - `ensure_singleton()` und andere schwere Checks in Hintergrund-Thread oder nach eel.start() verschoben
  - Blockierendes `time.sleep(2.0)` entfernt oder in nicht-blockierende Sequenz verschoben
  - Nicht-kritische Validierungen (z.B. env_handler.validate_safe_startup) nach UI-Launch ausgelagert

### Verifikationsplan
- **Automatisierte Tests:**
  - `python3 tests/test_ui_integrity.py` prüft DIV-Balance und Tab-IDs
  - App-Startzeit messen (UI muss schnell erscheinen, Hintergrundtasks laufen weiter)
  - Tabs durchklicken: Player, Library, Options, Parser, Debug, Tests – alle unabhängig sichtbar
- **Manuelle Checks:**
  - Footer bleibt beim Scrollen immer sichtbar
  - Options-Subtabs funktionieren unabhängig
  - Parser, Debug, Tests sind nicht in Options verschachtelt

### Lessons Learned
- DIV-Balance und Panel-Struktur sind kritisch für UI-Stabilität
- Footer muss sticky und unabhängig sein
- Früher UI-Start verbessert die User Experience deutlich
- Hintergrundinitialisierung verhindert Blockaden beim Start

---

## Task: Fix Audio Player Footer, Tab Structure, and Startup Speed (März 2026)

### Audio Player Footer
- Footer in `web/app.html` lokalisiert und CSS auf `position: fixed; bottom: 0; left: 0; right: 0;` gesetzt.
- `body`-Padding angepasst, damit Content nicht vom Footer überlappt wird.
- Fix im Browser überprüft: Footer bleibt beim Scrollen immer sichtbar.

### Tab Display Issues
- Struktur der Tabs "Options", "Parser", "Debug", "Test" in `web/app.html` analysiert.
- DIV-Fehler behoben:
  - Extra `</div>` bei Zeile 3574 entfernt
  - Fehlendes schließendes `</div>` bei Zeile 3909 ergänzt
  - Falsches Tag bei Zeile 6347 korrigiert
- Sicher gestellt, dass alle vier Tabs unabhängig und auf Top-Level gerendert werden.
- Fix mit `python3 tests/test_ui_integrity.py` verifiziert (DIV-Balance und Tab-IDs geprüft).

### Startup Optimization
- Bottlenecks in `src/core/main.py` identifiziert und schwere Tasks in Hintergrund-Threads ausgelagert (wo noch nötig).
- Redundante UI-Startverzögerungen entfernt.
- Startup-Geschwindigkeit manuell und per Log überprüft: UI erscheint schneller, Hintergrundtasks laufen weiter.

### Lessons Learned
- Footer und Tabstruktur müssen regelmäßig auf Segmentierungsfehler geprüft werden.
- Automatisierte Tests (z.B. test_ui_integrity.py) sind essenziell für UI-Stabilität.
- Früher UI-Start und Hintergrundinitialisierung verbessern die User Experience deutlich.
