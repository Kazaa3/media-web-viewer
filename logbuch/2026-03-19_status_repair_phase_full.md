# 🛠 Status & Repair Phase (19.03.2026)

## Aufgaben
- scripts/gui_validator.py für HTML-Depth-Trace und Audit erstellt
- Strukturelle Korrekturen in app.html (escaped nested <script>-Tags)
- appendUiTrace ReferenceError und UI-Leakage behoben
- App Naming ("dict" v1.34) im GUI synchronisiert
- Selenium-basierte GUI-Test-Suite (tests/gui_test.py) entwickelt
- DIV/Brace-Imbalancen und strukturelle Lecks repariert
- Premature Closure in General Options (Zeile 3277) identifiziert und gefixt

## HTML Struktur-Reparatur & Stabilisierung (Tabs, Left to Right)
1. Player Tab (Audit & Fix)
2. Library Tab (Audit & Fix)
3. Item Tab (Audit & Fix)
4. Datei Tab (Audit & Fix)
5. Edit Tab (Audit & Fix)
6. Options Tab (Audit & Fix)
   - Sub-tab 1: Allgemein
   - Sub-tab 2: Tools
   - Sub-tab 3: Architektur (Environment)
   - Persistent Navi (Fixed Header)
7. Parser Tab (Audit & Fix)
8. Debug Tab (Audit & Fix)
9. Tests Tab (Audit & Fix)
10. Reporting Tab (Audit & Fix, Buttons statt Select)
11. Logbuch Tab (Audit & Fix)
12. Playlist Tab (Audit & Fix)
13. Video Tab (Audit & Fix)

## Bug: Videoplayer im rechten Subtab des Video-Reiters fehlt
- Der Videoplayer wird im rechten Subtab des Video-Tabs nicht mehr angezeigt und ist aktuell "orphaned" (kein DOM-Element, keine Funktion).
- Ursache: Möglicherweise fehlerhafte Panel-Zuordnung, fehlendes HTML-Element oder ein Fehler im Tab-Switching/Rendering.
- ToDo: Panel- und Subtab-Logik im Video-Tab prüfen, Videoplayer-Element und -Initialisierung wiederherstellen.
- Siehe auch: app.html, switchTab('video'), Panel-ID: multiplexed-media-player-orchestrator-panel

## Bug: Logbuch-Panel unterhalb horizontalem Splitter
- Das Logbuch-Panel wird aktuell unterhalb eines horizontalen Splitters (Splitter-Element) auf halber Höhe angezeigt, statt im Hauptbereich.
- Symptom: Logbuch-Inhalt ist nach unten verschoben, der obere Bereich bleibt leer oder ist durch Splitter/Platzhalter blockiert.
- Ursache: Falsche Panel-Zuordnung, Splitter-Layout-Fehler oder fehlerhafte CSS-Regel.
- ToDo: Splitter- und Panel-Logik prüfen, Panel-Zuordnung und CSS anpassen, damit das Logbuch-Panel wieder im Hauptbereich angezeigt wird.
- Siehe auch: app.html, .sidebar, #main-splitter, #localized-markdown-documentation-journal-panel

## Bug: Environment-Ansicht nach Architektur-Subtab-Migration unvollständig
- Nach dem Merge der Environment-Ansicht in den Architektur-Subtab fehlen Funktionen oder UI-Elemente.
- Symptom: Environment-Infos, Aktionen oder Konfigurationsmöglichkeiten werden nicht oder nur teilweise angezeigt.
- Ursache: Unvollständige Migration, fehlende Panel-Initialisierung oder nicht übernommene Komponenten.
- ToDo: Architektur-Subtab "Environment" prüfen, fehlende Funktionen/Elemente nachziehen, Panel-Initialisierung und Datenanbindung sicherstellen.
- Siehe auch: app.html, switchOptionsView('environment'), #options-environment-view

## Bug: VLC/Stream/Drag&Drop Features orphaned
- Die Features für VLC, Stream und Drag&Drop sind aktuell im Code "orphaned" (nicht angebunden, keine UI oder Funktion).
- Es fehlt ein eigener Sub-Tab (z.B. im Video- oder Playlist-Bereich), um diese Funktionen zugänglich und bedienbar zu machen.
- ToDo: Sub-Tab für VLC/Stream/Drag&Drop anlegen, Features im Frontend und Backend wieder anbinden und UI/UX konsistent gestalten.
- Siehe auch: app.html, Tab- und Subtab-Logik, Panel-Initialisierung für VLC/Stream/Drag&Drop.

## Bug: eel.scan_media is not a function
- Fehler beim Aufruf von `eel.scan_media`: Funktion ist im Frontend/JS definiert, aber im Python-Backend nicht (oder nicht korrekt) via `@eel.expose` bereitgestellt.
- Symptom: Beim Klick/Trigger auf "scan_media" erscheint im Browser die Fehlermeldung "eel.scan_media is not a function".
- Ursache: scan_media fehlt als @eel.expose im Python-Code oder ist falsch benannt/registriert.
- ToDo: Im Python-Backend prüfen, ob `@eel.expose
def scan_media(...):` existiert und korrekt importiert/initialisiert ist. Funktionsnamen und Eel-Initialisierung abgleichen.
- Siehe auch: main.py, eel.expose, scan_media-Handler im Backend und Frontend.

## UI Refactoring
- Options/Reporting Sub-Navi vereinheitlicht
- Reporting Sub-Navi (Buttons statt Select)
- Architektur-View (Menu-Visibility fix)
- Modale sauber getrennt & kommentiert
- i18n & Tab-Namens-Check

## Modulare Selenium Tests
- tests/gui/ Verzeichnis angelegt
- test_tabs.py, test_subtabs.py, test_modals.py implementiert
- Verifikation & Walkthrough durchgeführt

## Weitere Aufgaben
- gui_validator.py für Multi-Line-Tags/Kommentare gefixt
- Application State & DB-Schema prüfen
- Pyre/IDE-Lints in main.py/models.py fixen
- Startup/Eel-Fehler testen

## ⚓ Anchors (Completed)
- Database Evolution: db.py (ISBN, IMDb, ParentID), insert_media → Row-ID
- Core Model Refactor: models.py (Item/Object-Split, Remote-ID, Amazon-Cover, to_dict)
- Scanning Logic: main.py (Zwei-Pass scan_media, Parent-Child-Linking)

## 📝 Open Points (To Do)
- Categorization Upgrade (format_utils.py)
- ISBN Scanning API (normalize_isbn, api_scan_isbn, OpenLibrary)
- Frontend: Scan ISBN-Button, Media Cards Hierarchie, Remote-ID-Links
- scan_media mit echten ISBNs testen, Parent-ID-Zuweisung prüfen

---

## Implementation Plan - Status & Repair Phase

This plan addresses structural corruption in app.html, backend API exposure issues, GUI synchronization, and the development of a Selenium-based test suite.

### Proposed Changes

#### [HTML & GUI] web/app.html
- **DIV/Brace Balance:**
  - Entferne 3 überzählige </div>-Tags am Ende der Logbuch/Layout-Sektionen (ca. Zeilen 4926-4928).
  - Repariere weitere Imbalancen laut gui_validator.py.
- **Structural Repairs:**
  - Fix escaped nested script tags (z.B. <\/script> in Template-Strings, ca. Zeile 1870).
  - Options Sub-Navi und Reporting Sub-Navi vereinheitlichen (Buttons überall).
  - Architektur-View Visibility fixen.
- **Bug Fixes:**
  - Video Player: Fehlenden/orphaned Webplayer im rechten Subtab des Video-Tabs wiederherstellen.
  - Logbuch: Panel-Positionierung relativ zum horizontalen Splitter reparieren.
  - Environment View: Migration in Architektur-Subtab abschließen.
  - VLC/Stream/Drag&Drop: Neuen Sub-Tab anlegen und Features zugänglich machen.
  - appendUiTrace: Sicherstellen, dass Funktion immer definiert ist und korrekt mit Backend kommuniziert.

#### [Backend] src/core/main.py
- **Eel Exposure:**
  - Prüfen, dass alle kritischen Funktionen (scan_media, ui_trace, api_scan_isbn) via @eel.expose bereitgestellt sind.
  - Sicherstellen, dass eel.init und eel.start korrekt im Lifecycle aufgerufen werden.
- **Synchronization:**
  - App Naming und Versioning ("dict" v1.34) in allen APIs synchronisieren.
- **ISBN API:**
  - normalize_isbn und api_scan_isbn (inkl. OpenLibrary-Fetch) implementieren.
- **Lints:**
  - Kritische Pyre/IDE-Lints in main.py und models.py beheben.

#### [Scripts] scripts/gui_validator.py
- **Parser Upgrade:**
  - Datei komplett lesen, Multi-Line-Regex oder State-Machine für Tags/Kommentare über mehrere Zeilen.
  - Erkennung von orphaned </div> und {}-Imbalancen verbessern.

#### [Testing] Selenium Test Suite
- **Directory:** tests/gui/ anlegen.
- **Tests:**
  - test_tabs.py: Wechsel zwischen allen 13 Haupt-Tabs prüfen.
  - test_subtabs.py: Sub-Navigation in Optionen, Reporting, Video prüfen.
  - test_modals.py: Öffnen/Schließen von Modals prüfen.

### Verification Plan

#### Automated Tests
- **GUI Audit:**
  - `python3 scripts/gui_validator.py web/app.html` → 0 Imbalancen
- **Backend Lints:**
  - `flake8 src/core/main.py src/core/models.py`
- **Selenium Suite:**
  - `pytest tests/gui/` (App muss laufen oder Mock-Eel-Server, ideal: Live-App)
  - Start: `python3 src/core/main.py` (im Hintergrund), dann `pytest tests/gui/`
- **Database Check:**
  - `python3 inspect_db.py` → ISBN/IMDb/ParentID-Spalten prüfen

#### Manual Verification
- **Startup Check:**
  - App via run.sh starten, auf Eel-Connection-Fehler achten
- **UI Audit:**
  - Video-Tab: Webplayer sichtbar/funktional rechts
  - Logbuch-Tab: Panel korrekt im Hauptbereich (nicht unter Splitter)
  - ISBN-Scan-Button in Metadata-View prüfen
- **VLC/Stream Sub-Tab:**
  - Sub-Tab öffnen, Features prüfen

---

## Implementation Plan - GUI Reconstruct & Scrolling Fix

This plan details the systematic reconstruction of the GUI structure in app.html to resolve layout breakages, enable scrolling in all sub-tabs, and improve visual clarity.

**User Review Required**
**IMPORTANT**
This plan involves significant structural changes to app.html. I will be rebuilding containers piece by piece to ensure stability.

### Proposed Changes

#### [HTML & CSS] web/app.html

1. **Global Scrolling & Layout Fix**
   - .tab-content Audit: Ensure all main tab containers have `height: 100%` and `overflow-y: auto` unless they are intended to be non-scrolling flex containers.
   - Sub-tab Containers: Add `overflow-y: auto` to every sub-view container (e.g., `.options-view`, `.lib-subtab-view`).
   - Parent Clipping: Check that no parent containers of scrolling areas have `overflow: hidden` in a way that clips the content prematurely.

2. **Sub-tab Visual Separation**
   - Sub-Nav Styling: Add distinct background colors (e.g., #f0f0f0 or light blue), borders, and padding to sub-navigation bars (Options sub-nav, Library sub-nav, Video sub-nav).
   - Active State: Ensure the active sub-tab has a strong visual indicator (e.g., bottom border or different color).

3. **Modal Reconstruction**
   - Modal Base Classes: Ensure all modals (about-imprint-modal, debug-flags-modal, feature-status-modal, logbook-modal, test-edit-modal, logbuch-editor-modal) share a consistent, robust structure:
     - Fixed overlay with semi-transparent background.
     - Centered content box with appropriate padding and max-height.
     - Scrolling within the modal body if content is long.

4. **Structural Audit & Repair**
   - Div Balance: Manually verify and fix DIV nesting for major sections:
     - Options Tab & Sub-views.
     - Library Tab & Sub-views.
     - Video Player Orchestrator.
     - Logbuch Tab.

### Verification Plan

#### Automated Tests
- **DIV Count:**
  - Run `grep -oP '<div' web/app.html | wc -l` and `grep -oP '</div>' web/app.html | wc -l` after each major section fix to ensure balance is maintained.

#### Manual Verification
- **Scrolling Audit:**
  - Navigate to Options → General, Options → Tools, Options → Environment. Verify that long content can be scrolled down.
  - Navigate to Library sub-tabs (Coverflow, Grid, Details). Verify scrolling.
  - Open all modals and verify they are centered and readable.
- **Visual Audit:**
  - Verify that sub-tabs are clearly separated from the main content and other tabs.
- **Tab Persistence:**
  - Verify that switching tabs does not reset scrolling or break the layout of other tabs.

---

## Walkthrough: HTML Stabilization & UI Fixes

I have completed the stabilization of app.html and addressed several UI issues as requested.

### Changes Made

1. **Structural Stabilization (Anchor Comments)**
   - Detaillierte Anchor-Kommentare für alle Hauptbereiche:
     - Navigation Tabs: <!-- TAB BUTTONS START/END -->
     - Sidebar: <!-- SIDEBAR END -->
     - Tab Panels: <!-- TAB: [Name] START/END -->
   - Kritischer Nesting-Fehler behoben: options-tools-view fehlte ein </div>, was alle nachfolgenden Tabs versteckte.

2. **Options Tab & Sub-tabs**
   - Zentraler Header (ID: options-main-header) hinzugefügt, der dynamisch aktualisiert wird.
   - Sub-tab Styling: Inline-Styles entfernt, .options-subtab.active CSS-Klasse eingeführt (blaues Underlining).
   - Funktion: switchOptionsView aktualisiert Header und Button-States korrekt.

3. **Audio Player Footer ("Spielt: von")**
   - i18n-Logik in updateMediaSidebar verbessert: Zeigt "Select a song" korrekt an, wenn kein Media aktiv ist.

4. **Sidebar Transcoding Tag**
   - [TRANSCODED]-Badge im Sidebar wiederhergestellt; erscheint korrekt bei item.is_transcoded.

### Verification Results

**HTML Structural Integrity**
- gui_validator.py auf app.html ausgeführt:
  - Final DIV stack size: 0
  - Final BRACE depth: 0
  - SUCCESS: Keine strukturellen Imbalancen.

**UI Functionality**
- Tab Switching: "Parser", "Debug", "Tests" verwenden eindeutige IDs und werden korrekt angesteuert.
- Options Header: Reflektiert aktiven Sub-Tab.
- Transcoding Tag: Logik im JS bestätigt.

### How to Verify
- Options-Tab öffnen, Header beim Wechsel zwischen "Allgemeine Einstellungen", "Advanced Tools", "System-Infrastruktur" prüfen.
- Transcodiertes Media-Item abspielen, Sidebar auf [TRANSCODED]-Badge prüfen.
- Footer prüfen: Bei keinem Song "Select a song" (bzw. deutsche Übersetzung).

---

## Walkthrough: Structural & Migration Repairs

This walkthrough documents the repairs made to web/app.html and scripts/gui_validator.py to resolve structural corruption, UI leakage, and migration issues in the Environment view.

### Changes Made

#### 1. web/app.html Structural Repairs

**DIV Imbalance & UI Leakage**
- Logbuch Tab: Removed three extra </div> tags that were causing the Logbuch panel to be orphaned and shifted (lines 4926-4928).
- Video Player: Corrected premature closing tags in the multiplexed-media-player-orchestrator-panel (lines 4348-4350), restoring the visibility of the player orchestrator.
- Environment View: Fixed severe structural corruption in the options-environment-view where tags were unclosed and attribute fragments were dangling outside tags (lines 3544-3553).

**ID Unification & Conflicts**
- Duplicate IDs: Renamed duplicate btn-shuffle and btn-repeat IDs in the Video Player to btn-shuffle-video and btn-repeat-video to prevent conflicts with the Sticky Footer Player (lines 4641, 4654).

**Template String Integrity**
- Nested Script Tags: Re-escaped </script> as <\/script> within JavaScript template strings to prevent premature script termination (line 1870).

#### 2. scripts/gui_validator.py Improvements

- Robust Parsing: Rewrote the validator to use a state machine that handles tags, comments, and JavaScript template strings (backticks) spanning multiple lines.
- Accuracy: Improved brace and tag tracking to differentiate between HTML/CSS context and script blocks.

### 3. Backend Synchronization

- App Naming: Verified that VERSION ("1.34") and app_name ("dict") are correctly synchronized from main.py to the frontend via Eel APIs.

## Verification Results

### Structural Audit
- Running the improved gui_validator.py confirms that the DIV stack and brace depth are now balanced across the entire 10k+ line app.html file.

### UI Integrity
- Video Player orchestrator is correctly nested and visible.
- Logbuch panel is correctly positioned within the main layout container.
- Environment view in the Architecture subtab correctly displays system status and Python info.
- No duplicate ID warnings in the browser console.

### Automated Tests
- Verified eel.scan_media and eel.get_version are correctly exposed and functional.
- Prepared the environment for subsequent Selenium-based testing.
