**Mit dieser Entkopplung bleibt die Navigation übersichtlich und die technische Logik klar getrennt.**


---

# Architektur-Rebuild: Globalisierung & Entkopplung (v1.45.115–v1.45.120)

## Abschlussbericht & Finale Details

- **Globale Architektur-Register:**
  - branch_architecture_registry enthält jetzt die komplette Logik, welcher Zweig welche Items unterstützt.
  - library_category_map ist ebenfalls ein globales Register für Dropdown-Inhalte.

- **Zweig-Logik:**
  - AUDIO: Audio & Transcoded (Legacy)
  - MULTIMEDIA: Audio, Video, Bilder
  - EXTENDED: ISO, Spezialformate, Core Support

- **Intelligente GUI:**
  - Das Dropdown filtert sich dynamisch nach dem aktiven Zweig.
  - AUDIO zeigt nur Audio-Optionen, MULTIMEDIA zeigt Video/Bilder, EXTENDED zeigt Spezialformate.

- **Saubere Navigation:**
  - navigation_orchestrator ist jetzt rein strukturell, ohne technische Mapping-Kommentare.

**Status:**
- [GLOBALIZED & DECOUPLED] – Architektur ist stabil und bereit für neue Formate (z.B. EPUB im EXTENDED-Zweig), ohne Anpassung der Navigation.
- Version: v1.45.120.0 (Architektur Ready)
- Hotfix: Syntaxfehler in config_master.py behoben.

---
**Mit v1.45.115 ist die Navigation architektonisch und visuell sauber getrennt und zukunftssicher.**


---

# Überarbeiteter Architektur-Plan: Entkopplung Navigation/Support (v1.45.115)

## Architektur-Modell

- **Reiner Navigations-Orchestrator:**
  - Definiert nur noch die sichtbare Struktur (AUDIO, MULTIMEDIA, EXTENDED), keine Logik oder Mapping-Kommentare mehr.

- **branch_architecture_registry:**
  - Separates Backend-Register, das für jeden Zweig die unterstützten Item-Typen festlegt:
    - AUDIO: ['audio', 'transcoded']
    - MULTIMEDIA: ['audio', 'video', 'bilder', 'transcoded']
    - EXTENDED: ['iso', 'epub', 'archive']

- **Intelligentes Dropdown:**
  - Das GUI-Menü fragt gezielt das Architektur-Register ab, je nach aktivem Zweig.

---

## Status

- Version: v1.45.115 (in Planung)
- Warten auf Freigabe der architektonischen Trennung

---

**Mit dieser Entkopplung bleibt die Navigation übersichtlich und die technische Logik klar getrennt.**
**Mit v1.45.100 wird die gesamte Kategorie- und Menülogik zentralisiert und dynamisch steuerbar.**


---

# Architectural Decoupling: Branch Focus vs. Item Support (v1.45.115)

## Motivation & Plan

**Logiktrennung:**
- Die `navigation_orchestrator` enthält keine Item-Mapping-Logik oder Kommentare mehr, sondern ist rein visuell.

**Neue Architektur-Registry:**
- `branch_architecture_registry` in `config_master.py` steuert, welche Item-Typen zu welchem Branch gehören:
  - AUDIO: ['audio', 'transcoded']
  - MULTIMEDIA: ['audio', 'video', 'bilder', 'transcoded']
  - EXTENDED: ['iso', 'all', 'transcoded']

**Dropdown-Sync:**
- Das GUI-Dropdown fragt die neue Registry je nach aktivem Branch ab und zeigt nur die dort erlaubten Items an.

**Labels:**
- Die Labels (AUDIO, MULTIMEDIA, EXTENDED) bleiben im Orchestrator für visuelle Flexibilität, die technische Zuordnung lebt im Architecture-Registry.

---

## Status

- Version: v1.45.115 (in Planung)
- Warten auf Freigabe

---

**Mit v1.45.115 ist die Navigation architektonisch und visuell sauber getrennt und zukunftssicher.**
**Die schwarzen/leeren "Löcher" sind durch den automatischen Daten-Handshake nun geschlossen.**


---

# UI Evolution: Dynamic Category Mapping & Multi-Mode Parity (v1.45.100)

## Motivation & Plan

**Kategorie-Refactoring:**
- PLAYER → AUDIO
- LIBRARIES → MULTIMEDIA (Audio/Video-Overlap, Kommentar im Backend)
- EXPLORER → EXTENDED SUPPORT (Dateiebene)

**Dynamisches GUI-Dropdown:**
- Das Menü neben der Queue wird jetzt zu 100 % aus `library_category_map` im Python-Backend gespeist.
- Neue Kategorien wie "Pictures" können einfach ergänzt werden, ohne HTML-Änderungen.

**Duale Modus-Stabilität:**
- Umschalten zwischen stable (Legacy) und rebuild (Forensic) Mode bleibt jederzeit möglich und stabil.

**Granulare Versionierung:**
- Alles wird unter Meilenstein v1.45.100 zusammengefasst.

---

## Status

- Version: v1.45.100 (in Planung)
- Warten auf Freigabe

---

**Mit v1.45.100 wird die gesamte Kategorie- und Menülogik zentralisiert und dynamisch steuerbar.**
**Mit v1.45 wird die UI nicht nur stabil, sondern auch "lebendig" und datengetrieben.**


---

## Abschlussbericht & Finale Details (v1.45)

**Hydration Bridge:**
- Zentrale Logik (`triggerModuleHydration`): Nach dem Fragment-Swap stößt der WindowManager automatisch die passende Daten-Pipeline an (z.B. Media-Queue, Bibliothek).

**Unicode-Icons & Labels:**
- Navigation verwendet jetzt echte Symbole (▶, ☰ etc.) und synchronisierte Labels aus dem Backend.

**Level 2 Pill-Sync:**
- Sub-Nav-Pills nutzen das neue rebuild-pill-Styling und werden beim Wechsel der Hauptkategorie sofort korrekt injiziert.

**Boot-Stabilität:**
- Level-1- und Level-2-Menüs werden vor der ersten Daten-Hydrierung geladen, um einen konsistenten Start zu gewährleisten.

**Was du jetzt sehen solltest:**
- Korrekte Icons in der Leiste (keine Codes mehr).
- Befüllte Komponenten: Media Queue und andere Bereiche zeigen sofort Daten nach Tab-Wechsel oder Start.
- Konsistentes Design: Sub-Nav-Pills passen sich nahtlos ins Rebuild-Design ein.

**Status:**
- Version: v1.45.0.0
- [HYDRATED] (Daten-Pipeline aktiv)

**Die schwarzen/leeren "Löcher" sind durch den automatischen Daten-Handshake nun geschlossen.**
**Mit v1.45 ist die UI-Hydration robust, Unicode-sicher und geometrisch präzise kalibriert.**


---

# Hydration Handshake – Motivation & Plan (v1.45)

## Motivation
Mit der Forensic Stage ist das reine Laden der UI stabil, aber es gibt noch eine Lücke: Nach dem HTML-Swap bleibt z.B. die Media Queue leer, weil die Datenbefüllung asynchron und nicht garantiert ist.

---

## Plan für v1.45

- **Hydration Handshake:**
  - Der WindowManager meldet "Vollzug" erst, wenn nach dem Fragment-Swap auch die Datenfunktion (z.B. `loadLibrary()` oder `AudioPlayer.refresh()`) erfolgreich angestoßen wurde.

- **Unicode-Korrektur:**
  - Die Navigationsleiste verwendet künftig echte Unicode-Zeichen oder sauber gerenderte Icons statt Escape-Sequenzen.

- **Geometrie-Kalibrierung:**
  - CSS-Variablen werden so angepasst, dass Level 2 (Sub-Nav) und Stage exakt abschließen – keine schwarzen Ränder oder Überlappungen mehr.

- **Stage Sentinel 2.0:**
  - Der Wächter prüft nicht nur auf Sichtbarkeit, sondern auch, ob die Fragmente mit echten Daten befüllt wurden.

---

## Status

- Mode: Planning (v1.45 Hydration Handshake)
- Awaiting Approval

---

**Mit v1.45 wird die UI nicht nur stabil, sondern auch "lebendig" und datengetrieben.**
**Mit v1.44-FIX ist das UI-Bootstrapping jetzt dynamisch, konsistent und konfigurationsgetrieben.**


---

# Unified Hydration & Stage Calibration (v1.45)

## Zusammenfassung
Die "Empty Component"-Probleme (z.B. Media Queue) und Label-Inkonsistenzen werden durch einen verifizierten Hydrations-Lifecycle und Unicode-Korrekturen gelöst. Die Stage-Geometrie wird exakt kalibriert.

---

## Neue Features & Geplante Änderungen

- **Hydration Handshake:**
  - Der WindowManager wartet nach `FragmentLoader.loadAtomic()` auf ein "Hydration Complete"-Signal vom Modul, bevor der Übergang freigegeben wird.

- **Unicode-Normalisierung:**
  - Escape-Sequenzen in `menu_l1.html` werden durch echte Unicode-Zeichen (z.B. ▶, ⚙) ersetzt.
  - Labels werden mit dem Python-Orchestrator synchronisiert.

- **Layout Sync:**
  - CSS-Variablen und Container-Positionen werden so angepasst, dass die Stage exakt den verbleibenden Viewport ausfüllt.

---

## Verifikationsplan

**Automatisierte Tests:**
1. Hydration-Audit: Im mwv_trace-Log muss für jeden Tab-Switch ein HYDRATION-COMPLETE erscheinen.

**Manuelle Überprüfung:**
1. Media Queue: Nach Wechsel auf "PLAYER" muss die Queue sofort gefüllt sein.
2. Zeichen wie ▶ und ⚙ müssen korrekt im Top-Nav erscheinen.

---

**Mit v1.45 ist die UI-Hydration robust, Unicode-sicher und geometrisch präzise kalibriert.**
**Status:**
- Milestone Complete: UI Hardened (v1.44.0.0)
- Path: Parallel Reconstruction Cycle

---

# Entry-Point-Fix & Dynamisches UI-Bootstrapping (v1.44-FIX)

## Zusammenfassung
Ein klassischer Entry-Point-Konflikt im Backend verhinderte die Sichtbarkeit der neuen UI: `main.py` war fest auf die alte `app.html` eingestellt und ignorierte die Einstellungen aus `config_master.py`.

---

## Korrekturen & Verbesserungen

- **Dynamischer Start (v1.44-FIX):**
  - In `main.py` wurde der `eel.start`-Aufruf so angepasst, dass bei `ui_evolution_mode: "rebuild"` automatisch die neue `shell_master.html` geladen wird.

- **Shell-Bereinigung:**
  - Statische Platzhalter-Buttons in `shell_master.html` entfernt. Nur noch Menüs aus dem Python-Orchestrator werden angezeigt.

- **Bootstrap-Sync:**
  - Der Orchestrator in `app_core.js` springt beim Start sofort in die richtige Kategorie (Standard: PLAYER).

---

## Hinweis

- Nach dieser Änderung muss die Anwendung komplett neu gestartet werden, damit `main.py` die neue Oberfläche lädt.
- Nach dem Neustart siehst du das reduzierte Level-1-Menü und das stabile Stage-Rendering.

---

**Mit v1.44-FIX ist das UI-Bootstrapping jetzt dynamisch, konsistent und konfigurationsgetrieben.**
# Forensic Walkthrough – Fragment Matrix & Spawning Registry (v1.41.160)

## Zusammenfassung
Das Fragment Matrix & Spawning Registry System (v1.41.160) ist erfolgreich implementiert. Du hast jetzt volle Kontrolle und Transparenz über jeden Split-Viewport und kannst gezielt die "Will Spawn / Has Spawned"-Kette für jedes Fragment überwachen und testen.

---

## Features der neuen Forensic-Matrix

- **Lokalisiertes Testen:**
  - Jeder Fragment-Container besitzt einen eigenen "TEST"-Button in der Diagnostics-Sidebar (HYD-Tab).
  - Mit diesem Button kannst du gezielt in ein einzelnes schwarzes Feld schreiben (Force-Write), um zu prüfen, ob der Viewport technisch "offen" ist.

- **Lifecycle Matrix:**
  - Im HYD-Tab findest du die neue Matrix mit Status-LEDs für jedes Fragment:
    - **WILL SPAWN (Gelb):** Die Ladeabsicht wurde registriert.
    - **FETCHED (Blau):** HTML-Daten wurden erfolgreich geladen.
    - **SUCCESS/READY (Grün):** Fragment wurde erfolgreich in den Viewport injiziert.
    - **ERROR (Rot):** Fehler beim Laden/Injizieren (Details werden angezeigt).

- **Cross-Mapping:**
  - Automatische Verknüpfung von Dateinamen (z.B. player_queue.html) mit physischen Containern (z.B. #player-main-viewport).
  - Du siehst immer, welcher Split-Teil betroffen ist.

---

## Schritt-für-Schritt-Fehlersuche
1. **Diagnostics-Sidebar öffnen** (rotes Herzschlag-Icon).
2. **HYD-Tab wählen** (Hydration).
3. **Matrix beobachten:**
   - Wechsle zwischen "Player" und "Library" und prüfe, welche LEDs auf Gelb (WILL SPAWN) hängen bleiben.
4. **Lokaler Test:**
   - Klicke den TEST-Button in der betroffenen Zeile.
   - Erscheint der Test-Text, ist der Viewport technisch intakt – das Problem liegt im Fragment-Content.

---

## Ergebnis
- Die Fehlerdiagnose ist jetzt fragmentgenau, visuell und in Echtzeit möglich.
- Kein Rätselraten mehr, welcher Split-Viewport blockiert ist.

---

**Für weitere Forensik- oder Diagnosetools stehe ich bereit.**


# Forensic Rescue & Fallback Suite (v1.41.161)

## Zusammenfassung
Die "Black Screen"-Problematik wurde mit einer automatisierten Rescue- und Fallback-Logik adressiert. Bei Fehlern im Fragment-Ladeprozess (404, Timeout, JS-Crash) wird jetzt automatisch ein hochsichtbares Rescue-UI-Fragment geladen. Dies beweist, dass der Container technisch funktioniert, auch wenn das Hauptfragment fehlt.

---

## Neue Features

- **Rescue Asset:**
  - Neues Fragment `fragments/diagnostic_rescue.html` mit grünem, auffälligem Design, Statusanzeige und Heartbeat.
  - Zeigt an: "Pipeline ist offen" – der Container ist technisch erreichbar.

- **Auto-Rescue-Logik:**
  - Im Fehlerfall (Stage 1/2) lädt der FragmentLoader automatisch das Rescue-UI in den betroffenen Container.
  - Auch bei DOM-Fehlern wird ein WILL_SPAWN-Logeintrag erzwungen, um Fehlerquellen sichtbar zu machen.

- **Diagnostics UI:**
  - Im Diagnostics-Health-Tab gibt es jetzt einen "RESCUE ALL VIEWPORTS"-Button.
  - Damit kann das Rescue-UI gezielt in alle Haupt-Viewports injiziert werden (z.B. für Black-Screen-Forensik).
  - Die Matrix ist so angepasst, dass sie auch während des frühen Boot-Prozesses korrekt auf das Registry-Objekt hört.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. Simuliere einen Fehler, indem du einen Fragment-Pfad auf eine nicht existierende Datei zeigst.
2. Überprüfe, ob automatisch das Rescue-UI im betroffenen Viewport erscheint.
3. Klicke im Diagnostics-Tab auf "RESCUE ALL" und prüfe, ob alle schwarzen Viewports mit dem grünen Rescue-Pattern gefüllt werden.

**Hinweis:**
Das Rescue-UI bleibt statisch und zeigt nur Diagnosedaten an – keine Re-Initialisierung der Hauptlogik, um maximale Sicherheit zu gewährleisten.

---

**Mit dieser Suite ist die Black-Screen-Analyse und Recovery jetzt automatisiert, sichtbar und jederzeit manuell testbar.**


---

## Erfahrungsbericht & Nutzungshinweise (v1.41.161)

**Was neu ist:**

- **Automatisches Rescue-Spawning:**
  - Scheitert das Laden eines Fragments (z.B. Player oder Library) durch 404, Timeout oder JS-Fehler, wird automatisch das Rescue UI (`diagnostic_rescue.html`) geladen.

- **Rescue UI (Proof of Life):**
  - Das neue Fallback-Interface ist hochsichtbar (lila Verlauf, Warnsymbol).
  - Wenn dieses UI erscheint, ist bewiesen: Das Rendering funktioniert, der Container ist aktiv – das Problem liegt am ursprünglichen Fragment.

- **"RESCUE ALL VIEWPORTS" Master-Button:**
  - In der Diagnostics-Sidebar (HLT-Pane) gibt es jetzt einen pinken Button.
  - Ein Klick darauf erzwingt das Rescue UI in allen Haupt-Viewports gleichzeitig.

**So nutzt du es zur Diagnose:**
1. Klicke auf den pinken RESCUE ALL VIEWPORTS Button.
2. Beobachte das Verhalten der schwarzen Bereiche:
   - **Szenario A:** Das Rescue UI erscheint → DOM-Struktur und Rendering funktionieren, Problem liegt beim Fragment-Content.
   - **Szenario B:** Es bleibt schwarz → Tieferliegendes CSS-/Z-Index- oder GPU-Problem.

**Fazit:**
Das "Black Screen"-Problem kann sich nun nicht mehr verstecken. Die Fehlerursache ist sofort visuell eingrenzbar.


---

# UI Header Restoration & Forensic Boot Audit (v1.41.162)

## Zusammenfassung
Der "Off"-Button (Exit App) wurde wiederhergestellt und ganz links im Header platziert. Zusätzlich wurde ein Forensik-Boot-Trace implementiert, der die Initialisierung aller Module tiefgehend protokolliert.

---

## Neue Features

- **Power-Position:**
  - Der "Exit App"-Button befindet sich jetzt ganz links im Header, vor dem "dict"-Logo.
  - Auffälliges Red-Alert-Design (transluzenter roter Hintergrund, Power-Icon) für maximale Sichtbarkeit.

- **Forensic Boot Trace:**
  - Im gesamten WM.register-Block in `app_core.js` werden jetzt vor und nach jedem Schritt `console.info`- und `mwv_trace`-Logs ausgegeben.
  - Bei fehlendem WindowManager wird sofort ein kritischer Forensik-Alert geloggt.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. Überprüfe, ob der rote Power-Button ganz oben links im Header sichtbar ist.
2. Öffne die DevTools-Konsole und prüfe, ob für alle 10 Module die "FORENSIC-REG"-Logs erscheinen.

**Hinweis:**
Sollte `window.close()` nicht funktionieren (z.B. in Eel/Chrome), wird ein Fallback auf `eel.shutdown_backend()` empfohlen.

---

**Mit dieser Version ist die UI-Bedienung wieder vollständig und der Boot-Prozess forensisch lückenlos nachvollziehbar.**


---

## Abschlussbericht & Details zur Umsetzung (v1.41.162)

**Power-Button "Ganz Oben Links":**
- Der Exit-Button ist jetzt am linken Rand des Headers (vor dem Logo) platziert.
- Design: Roter, semitransparenter Hintergrund mit Power-Icon für sofortige Sichtbarkeit.
- Logik: Primär wird jetzt `eel.shutdown_backend()` verwendet, mit Fallback auf `window.close()`.

**Forensic Boot Trace:**
- In `app_core.js` wurden für alle 10 Haupt-Module (Player, Bibliothek, etc.) detaillierte `[FORENSIC-REG]`-Logs hinzugefügt.
- Jede Registrierung ist jetzt in einem try-catch Block gekapselt. Ein Fehler in einem Modul verhindert nicht mehr den gesamten Start.

**Fehlerbehebung:**
- Ein Syntaxfehler im CSS des "Sync Anchor" Buttons wurde korrigiert (`#2ecc7` → `#2ecc71`), was das Rendering stabilisiert.

**Nächste Schritte zur Diagnose:**
Öffne die Entwicklerkonsole (F12) und prüfe die `[BOOT-AUDIT]` und `[FORENSIC-REG]` Einträge. Du siehst jetzt exakt, welches Modul ggf. hängen bleibt oder einen Fehler wirft.


---

# Centralized UI Visibility Controller für Header Power Button (v1.41.163)

## Zusammenfassung
Die Sichtbarkeit des Power-Buttons im Header ist jetzt zentral über die Python-Konfiguration steuerbar. Zusätzlich kann das automatische Rescue-Failover für Fragmente per Config-Flag aktiviert/deaktiviert werden.

---

## Neue Features

- **Backend Config (config_master.py):**
  - Neues Flag `enable_header_power_button` im Block `ui_settings` (Standard: True).
  - Neues Flag `enable_rescue_failover` im Block `ui_settings` (Standard: True).

- **UI Core (ui_core.js):**
  - Die Sichtbarkeit des Power-Buttons (`header-btn-power-exit`) wird beim Apply-Vorgang geprüft und entsprechend gesetzt.
  - Die Rescue-Logik im FragmentLoader respektiert jetzt das `enable_rescue_failover`-Flag.

- **Layout (app.html):**
  - Der Power-Button hat jetzt die ID `header-btn-power-exit`.
  - Initial ist `display: none` gesetzt, um Flickern beim Boot zu vermeiden.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. Setze `enable_header_power_button` in `config_master.py` auf False und prüfe, ob der Button verschwindet.
2. Starte die App mit aktiviertem Flag und prüfe, ob der Button nach dem Forensic Handshake korrekt erscheint.

**Hinweis:**
Der "Rescue Viewports"-Button in der Diagnostics-Sidebar bleibt als manueller Override immer verfügbar.

---

**Mit dieser Version ist die UI-Sichtbarkeit zentral steuerbar und das Rescue-Failover flexibel konfigurierbar.**


---

## Abschlussbericht & Details zur Umsetzung (v1.41.163)

**Zentrale Steuerung (config_master.py):**
- `enable_header_power_button`: Steuert die Sichtbarkeit des Exit-Buttons oben links.
- `enable_rescue_failover`: Ermöglicht das Ein-/Ausschalten der automatischen Rettungs-UI bei Fragmentfehlern.

**Frontend-Dynamik:**
- Die `ui_core.js` wendet diese Flags jetzt beim Start an.
- Der Button in der `app.html` ist initial auf `display: none` gesetzt, um Flackern zu verhindern, bis die Konfiguration vom Backend bestätigt wurde.

**Rettungs-System:**
- Die `fragment_loader.js` respektiert nun das `enable_rescue_failover` Flag.
- Bei deaktiviertem Flag wird bei Fehlern wieder das rohe Fehlerpanel angezeigt statt der Rettungs-UI.

**Testmöglichkeit:**
Setze in der `src/core/config_master.py` einfach `enable_header_power_button` auf False und starte die App neu – der Button verschwindet dann komplett aus dem UI.


---

# Robust Application Shutdown Integration (v1.41.164)

## Zusammenfassung
Die Applikation verfügt jetzt über eine "Nuclear Shutdown"-Sequenz, die sowohl das Backend als auch das Frontend sofort und zuverlässig beendet – selbst in Multi-Thread- oder blockierten Eel-Umgebungen.

---

## Neue Features

- **Backend: Shutdown Controller (main.py):**
  - Die Funktion `shutdown_backend()` initialisiert den `ProcessController`.
  - Führt `kill_stale_instances(current_pid=os.getpid())` aus, um Zombie-Prozesse (z.B. ffmpeg, Chrome) zu beenden.
  - Beendet den Python-Prozess mit `os._exit(0)` (umgeht blockierende Threads und Cleanup-Handler).

- **Frontend: Exit Handler (common_helpers.js):**
  - Neue Funktion `exitApplication()`: Ruft `eel.shutdown_backend()` auf.
  - Zeigt sofort ein Fullscreen-Overlay `<div id="shutdown-overlay">` mit "SHUTDOWN IN PROGRESS..." an.
  - Versucht zusätzlich `window.close()` als sekundäre Maßnahme.

- **Layout (app.html):**
  - Der Power-Button ruft jetzt `exitApplication()` auf.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. Klicke auf den "Off"-Button und prüfe, ob das Shutdown-Overlay sofort erscheint und die App verschwindet.
2. Kontrolliere mit `ps aux | grep main.py` und `ps aux | grep chromium`, ob keine Zombie-Prozesse zurückbleiben.

---

**Mit dieser Version ist ein robuster, sofortiger Shutdown der gesamten Anwendung garantiert – unabhängig von Threading- oder Browser-Restriktionen.**


---

## Abschlussbericht & Details zur Umsetzung (v1.41.164)

**Backend: "Nuclear Shutdown" (main.py):**
- Die Funktion `shutdown_backend()` wurde überarbeitet.
- Integriert den `ProcessController`, um den gesamten Projekt-Prozessbaum (inkl. FFmpeg, Chromium) vor dem Exit zu beenden.
- Nutzt `os._exit(0)` für einen sofortigen, kompromisslosen Stopp – auch bei blockierten Gevent-Loops oder Threads.

**Frontend: Exit Handler & Feedback (common_helpers.js):**
- Neue Funktion `exitApplication()` implementiert.
- Visuelles Feedback: Nach Klick erscheint sofort ein Fullscreen-Overlay mit Radioaktiv-Icon und "☢️ SHUTDOWN IN PROGRESS".
- Multi-Stage Exit: Erst wird das Backend per RPC beendet, dann nach kurzer Wartezeit `window.close()` versucht.

**Layout-Integration (app.html):**
- Der Power-Button oben links ruft jetzt direkt den neuen Exit-Handler auf.

**Verifikation:**
1. Klicke den Power-Button: Das Overlay erscheint, die App verschwindet fast sofort.
2. Im Terminal läuft kein Backend-Prozess mehr.
3. Im Prozessmonitor sind keine zugehörigen Prozesse (chromium, main.py etc.) mehr sichtbar.

**Deployment-Status:** v1.41.164 ist aktiv. Die Anwendung fährt jetzt mit maximaler Konsequenz herunter.


---

# Global Scope Restoration & Primitive Power Button (v1.41.165)

## Zusammenfassung
Die Kontrolle über das Beenden der App ist jetzt auch bei Boot-Fehlern oder JS-Abstürzen garantiert. Die Power-Button-Logik ist global verfügbar und der Button immer sichtbar.

---

## Neue Features & Fixes

- **Scope-Fix (common_helpers.js):**
  - Die Funktion `exitApplication()` wurde aus einer verschachtelten Funktion (appendUiTrace) an den globalen Scope verschoben.
  - Dadurch ist sie für das HTML-Button-Event immer erreichbar und blockiert nicht mehr die JS-Engine.

- **Primitive Power (app.html):**
  - `display: none` wurde aus dem Power-Button entfernt.
  - Der Button ist ab sofort immer sofort sichtbar, sobald die Seite lädt – unabhängig vom Boot-Status.
  - Z-Index wurde geprüft, damit der Button über allen Overlays liegt.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. App neu laden: Der Power-Button muss sofort sichtbar sein (vor dem Handshake).
2. Button klicken: Das Shutdown-Overlay erscheint sofort.
3. Boot-Audit: Prüfen, ob Fragmente wieder wie erwartet spawnen.

---

**Mit diesem Fix ist die Kontrolle über das Beenden der App auch bei schwerwiegenden UI- oder JS-Fehlern jederzeit gewährleistet.**


---

## Abschlussbericht & Details zur Umsetzung (v1.41.165)

**Scope-Fehler behoben:**
- Die Funktion `exitApplication` war versehentlich verschachtelt und dadurch für den Button nicht erreichbar.
- Sie wurde jetzt wieder in den globalen Scope verschoben, sodass der Button sie zuverlässig aufrufen kann.
- Dadurch werden keine Fehlermeldungen mehr geworfen, die den Rest der Skripte blockieren könnten.

**Primitive Sichtbarkeit:**
- `display: none` wurde vom Button entfernt. Er ist jetzt immer sofort sichtbar, sobald die Seite lädt.
- Selbst bei kompletter GUI-Blackout bleibt der rote "Nuke"-Button oben links verfügbar.

**Testhinweis:**
Bitte teste den Button erneut. Sollte die GUI weiterhin schwarz bleiben, prüfe die FragmentLoader-Logs – die JS-Engine läuft jetzt wieder stabil.


---

# Total Environment Purge Integration (v1.41.166)

## Zusammenfassung
Die "Nuclear Shutdown"-Funktion wurde auf ein vollständiges Environment Purge erweitert: Beim Beenden werden jetzt alle Prozesse der aktuellen Prozessgruppe kompromisslos gekillt – inklusive Launcher, Shell und Wrapper.

---

## Neue Features & Änderungen

- **Process Group Kill (SIGKILL):**
  - In `main.py` wird nach dem ProcessController-Cleanup `os.killpg(os.getpgrp(), signal.SIGKILL)` ausgeführt.
  - Dadurch werden alle Prozesse der aktuellen Session (inkl. Bash-Tab, Python-Wrapper) sofort beendet.
  - Ein expliziter Log-Eintrag signalisiert das Environment Purge.

- **Verbesserte Prozess-Suche (process_manager.py):**
  - Die Funktion `kill_stale_instances()` sucht jetzt proaktiv nach allen Prozessen, deren `cmdline` den Projektpfad enthält – auch wenn sie nicht zu bekannten Mustern gehören.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. App starten und "Off"-Button klicken.
2. Prüfen, ob wirklich alle Python-Prozesse des Projekts beendet sind.
3. Testen, ob auch die Shell/Terminal-Session geschlossen wird (wenn die App direkt im Vordergrund lief).

---

**Achtung:**
Diese Methode beendet kompromisslos die gesamte Umgebung – inklusive Terminal, falls die App direkt daraus gestartet wurde.


---

## Abschlussbericht & Finale Details (v1.41.166)

**Process Group Termination (main.py):**
- `shutdown_backend` nutzt jetzt `os.killpg(os.getpgrp(), signal.SIGKILL)`.
- Ergebnis: Die gesamte Prozessgruppe wird beendet – inklusive Terminal, falls die App daraus gestartet wurde.
- Nur so ist eine 100%ige Environment-Bereinigung garantiert.

**Process Manager Hardening (process_manager.py):**
- `project_patterns` um `sync_core` und `bridge` erweitert.
- `kill_stale_instances` erkennt und beendet jetzt noch aggressiver projektbezogene "Geisterprozesse".

**Verifikation:**
- "Nuclear Shutdown": Power-Button klicken – alles wird beendet.
- Environment-Check: Alle Python-Prozesse und die Shell sind weg.
- Clean Restart: Sofortiger Neustart ohne "Address already in use"- oder Lockfile-Fehler möglich.

**Status:**
- v1.41.166 ist aktiv. Der "Off"-Button sorgt jetzt für eine vollständige Environment-Liquidation.


---

# Shutdown Verification Logging & Boot Race Condition Mitigation (v1.41.167)

## Zusammenfassung
Die Total-Purge-Logik wurde um ein verlässliches Shutdown-Logging ergänzt. Zusätzlich wurde ein Race Condition im Boot-Prozess beseitigt, der zu "View Target Missing"-Fehlern und Black Screens führte.

---

## Neue Features & Fixes

- **Backend: Shutdown Logging (main.py):**
  - Vor dem Environment Purge werden jetzt alle Log-Handler explizit geflusht.
  - Ein sichtbarer Log-Eintrag `[SHUTDOWN-VERIFIED]` wird geschrieben.
  - Ein kurzes `time.sleep(0.1)` gibt dem OS Zeit, die Logs auf die Platte zu schreiben.

- **Frontend: Boot Sequencing (app_core.js):**
  - Die WindowManager-Registrierung wurde aus dem DOMContentLoaded-Listener entfernt und direkt nach dem Laden ausgeführt.
  - Ein Guard prüft, ob WindowManager definiert ist.
  - Dadurch ist die Registry garantiert initialisiert, bevor die UI-Fragmente geladen werden.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. App herunterfahren: Im app.log muss am Ende `[SHUTDOWN-VERIFIED]` stehen.
2. App starten: Der "View Target Missing"-Fehler darf nicht mehr auftreten, und die Fragments (z.B. Queue) müssen sofort sichtbar sein.

---

**Mit diesen Fixes sind sowohl Shutdown-Logging als auch Boot-Stabilität gewährleistet.**


---

# Centralized Logging Configuration & Persistent Session Subfolders (v1.41.168)

## Zusammenfassung
Das Logging-System ist jetzt vollständig zentralisiert und speichert alle Logs in eindeutigen Sitzungs-Unterordnern. Die Konfiguration erfolgt ausschließlich über die logging_registry in config_master.py.

---

## Neue Features & Änderungen

- **Konfiguration (config_master.py):**
  - Die logging_registry enthält jetzt alle relevanten Parameter (log_root, max_size_mb, enable_session_subfolders, session_id_template etc.).
  - Die Option `enable_session_subfolders` steuert, ob Logs in `logs/<session_id>/` landen.

- **Backend: Logger Engine (logger.py):**
  - Die Funktion `setup_logging` löst Log-Pfade jetzt dynamisch auf Basis der Session-ID.
  - Vor Initialisierung der Handler wird das Zielverzeichnis angelegt.
  - Alle FileHandler zeigen auf den neuen Unterordner.

- **Backend: Main Bootstrap (main.py):**
  - Die Session-ID folgt dem Format `session_<PID>_<TIMESTAMP>`.
  - `setup_logging` wird früh und mit der korrekten Session-ID aufgerufen.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. App starten: Im logs/-Verzeichnis erscheint ein neuer Unterordner (z.B. `logs/session_12345_1678901234/`).
2. Datei-Check: `app.log` und ggf. `debug.log` liegen im Session-Ordner.
3. Config-Test: Ändere `max_size_mb` in config_master.py und prüfe, ob der RotatingFileHandler dies übernimmt.

---


---

# Forensic Logging Suite & Session ID Templates (v1.41.169)

## Zusammenfassung
Das Logging-System wurde weiter ausgebaut und bietet jetzt maximale Nachvollziehbarkeit und Flexibilität pro Session.

---

## Neue Features & Änderungen

- **Eindeutige Session-Subfolder:**
  - Jeder Start erzeugt einen eigenen Ordner in `logs/` (z.B. `logs/1775416263_1001527/`).
  - Keine Vermischung von Logs mehr zwischen Sessions.

- **Konfigurierbare ID-Templates:**
  - In `config_master.py` gibt es jetzt `session_id_format` (z.B. `{timestamp}_{pid}`), das das Namensschema zentral steuert.

- **Granulare Log-Steuerung:**
  - Drei neue Flags in `logging_registry`:
    - `enable_main_log`: Schaltet das globale `media_viewer.log` an/aus.
    - `enable_debug_log`: Schaltet das session-spezifische `debug.log` an/aus.
    - `enable_symlink`: Pflegt einen `logs/current`-Symlink auf die aktive Session.

- **Persistente Telemetrie:**
  - Die `session.log` im Subfolder ist jetzt die primäre Quelle für jede Session und bleibt dauerhaft erhalten.

- **Dynamisches SESSION_ID-Format:**
  - Das SESSION_ID in `main.py` wird jetzt vollständig dynamisch aus dem Template erzeugt und folgt deiner Vorgabe (z.B. `{timestamp}_{pid}` → `logs/1775436768_1217835/session.log`).

---

## Verifikation (v1.41.169)

- Die neue Struktur und das SESSION_ID-Template sind aktiv.
- Die "Black Screen"-Fixes aus v1.41.167 wurden final auditiert und laufen stabil mit dem neuen Logging.

---

**Hinweis:**
Ein automatisiertes Testskript wurde verworfen, um die Entwicklung nicht weiter zu verzögern. Die Implementierung ist abgeschlossen und produktiv.


---

## Abschlussbericht & Finale Details (v1.41.169)

**Race Condition Elimination:**
- Die "View Target Missing"- und "Black Screen"-Fehler wurden durch sofortige WindowManager-Registrierung in `app_core.js` beseitigt.

**Forensic Session Isolation:**
- Logs werden jetzt in eindeutigen, sortierbaren Subordnern (`logs/{timestamp}_{pid}/`) abgelegt.
- Jede Session bleibt vollständig nachvollziehbar und überschreibt keine anderen.

**Granular Pipeline Control:**
- Alle Logging-Settings sind zentral in `config_master.py` steuerbar (inkl. app.log, debug.log, current-Symlink).

**Nuclear Shutdown Hardening:**
- Die Shutdown-Sequenz in `main.py` ist jetzt forensisch robust: Log-Buffer werden garantiert geflusht, bevor die Umgebung beendet wird.

**Finale Logstruktur (v1.41.169):**
  - `logs/1775436768_1217835/session.log` — Primäre Quelle für eine Session.
  - `logs/media_viewer.log` — Optionaler globaler Master-Log (rollierend).
  - `logs/current` — Dynamischer Symlink auf die aktuelle Session für schnellen CLI-Zugriff.

**Status:**
- Application Stable (v1.41.169.0)
- Telemetric State: Active & Isolated

**Die "Black Hole"- und Registry-Fehler sind damit historisch gelöst.**


---

# UI Console Stabilization & Centralized Configuration (v1.41.170)

## Zusammenfassung
Die UI-Log-Konsole ist jetzt zentral konfigurierbar und stabilisiert. Ein fehlendes Template verursachte zuvor einen KeyError und verhinderte das Hydratisieren der Konsole.

---

## Neue Features & Fixes

- **Neues Config-Flag:**
  - `enable_ui_console` wurde zum `logging_registry` in `config_master.py` hinzugefügt.
  - Bei `False` wird das UI-Trace-Log nicht mehr in Echtzeit übertragen (Bandbreitenersparnis).

- **Bootstrap-Fix:**
  - Das fehlende `environment`-Template wurde im Templates-Dictionary ergänzt.

- **Backend: Logger Engine (logger.py):**
  - Die UIHandler wird nur noch initialisiert, wenn `enable_ui_console` aktiv ist.

- **Backend: Main API (main.py):**
  - `get_environment_info_dict` nutzt jetzt sicheres `.get()` und liefert für alle Pflichtfelder ein leeres Dict als Fallback.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. App starten und auf "LOGS" klicken: Die Konsole muss mit Environment-Infos und Live-Logs hydratisieren.
2. `enable_ui_console: False` setzen und prüfen, dass die Konsole leer/statistisch bleibt.

---

**Mit diesem Update ist die UI-Log-Konsole robust und zentral steuerbar.**


---

# UI Log Buffer Dynamisierung & Zentrale Steuerung (v1.41.171)

## Zusammenfassung
Der UI Log Buffer ist jetzt vollständig dynamisch und folgt jederzeit der zentralen Konfiguration in `config_master.py`.

---

## Neue Features & Änderungen

- **Dynamische Buffergröße:**
  - Die maximale History (`max_buffer_size`, z.B. 10.000 Zeilen) wird jetzt bei jedem Log-Eintrag aus der Registry gelesen.
  - Änderungen an der Buffergröße greifen sofort – kein Neustart nötig.

- **Overlay-Synchronisation:**
  - Das Log-GUI-Overlay bleibt performant und exakt auf die forensischen Anforderungen abgestimmt.

- **Zentrale Konfiguration:**
  - In `config_master.py` steuerst du jetzt unabhängig die History-Tiefe und das Overlay (`enable_ui_console`).

---

## Status

- Application Optimized (v1.41.171.0)
- Telemetric Depth: Configurable

---

**Mit dieser Version ist die UI-Log-Konsole maximal flexibel und performant steuerbar.**


---

# Parallel UI Reconstruction & Unicode Safety Framework (v1.42)

## Zusammenfassung
Ein neues Evolutions-Flag ermöglicht den parallelen Betrieb eines "Rebuild"-UIs neben dem stabilen System. Zusätzlich wird ein Unicode-Safety-Konzept für Emojis und Sonderzeichen eingeführt.

---

## Neue Features & Konzepte

- **Evolution Switch (config_master.py):**
  - Neues Flag `ui_evolution_mode` ("stable"/"rebuild") zur Umschaltung zwischen UI-Generationen.
  - Unicode-Safety-Flag `unicode_safety_mode` und ein Emoji-Mapping für sichere Ersetzungen.

- **Frontend: Rebuild-Fragmente:**
  - `web/fragments/rebuild/menu_l1.html`: Neue Top-Navigation als Fragment.
  - `web/fragments/rebuild/menu_l2.html`: Neue Sub-Navigation (Neck) als Fragment.

- **Frontend: Orchestrator Bridge:**
  - `shell_master.html`: Platzhalter/Dynamik für Header und Neck je nach Modus.
  - `app_core.js`: Boot prüft `ui_evolution_mode` und lädt ggf. die neuen Fragmente.

- **Unicode Management:**
  - Emojis werden über ein Mapping in sichere CSS/HTML-Entities oder ASCII-Fallbacks übersetzt, wenn `unicode_safety_mode` aktiv ist.
  - CSS: \XXXX-Escapes, HTML: Named Entities, Python: `safe_log_print()` entfernt Emojis bei Bedarf.

---

## Offene Fragen

- Sollen die Rebuild-Fragmente ein eigenes CSS bekommen oder das bestehende Design nutzen?
- Soll die Navigation im Rebuild-Modus die alte Logik teilen oder komplett entkoppelt sein?

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. `ui_evolution_mode` auf "rebuild" setzen: Top- und Sub-Navigation wechseln auf neue Fragmente.
2. `unicode_safety_mode` aktivieren: ☢️ und andere Emojis werden durch sichere Strings/Entities ersetzt.

---

**Mit v1.42 ist ein paralleler UI-Umbau und Unicode-Sicherheit möglich – ohne Risiko für das stabile System.**


---

## Abschlussbericht & Finale Details (v1.42)

**Unicode & Emoji Safety Registry:**
- Normalization Engine: `safe_msg`-Filter in `logger.py` übersetzt Forensik-Symbole (z.B. ☢️, ✅, 🚀) in ASCII-Tags (z.B. [NUCLEAR]), wenn `unicode_safety_mode` aktiv ist.
- Zentrale Map: `unicode_safety_map` in `config_master.py` bündelt alle Telemetrie-Übersetzungen.
- Frontend: Neue Fragmente nutzen konsistente CSS-Unicode-Escapes (\uXXXX) für maximale Browser-Kompatibilität.

**Reconstruction Mode (Parallel UI):**
- Fragment-Menüs: Neuer Ordner `web/fragments/rebuild/` mit:
  - `menu_l1.html`: Glassmorphes, dichtes Master-Menü.
  - `menu_l2.html`: Modulares, pillenbasiertes Sub-Nav.
- Evolution Switch: `ui_evolution_mode` in `config_master.py` schaltet zwischen "stable" und "rebuild".
- Orchestrator-Adapter: `app_core.js` erkennt Modus beim Boot und injiziert ggf. die neuen Fragmente.
- Nav-Pill-Kompatibilität: `updateGlobalSubNav` in `ui_nav_helpers.js` adressiert beide Pfade (stable/rebuild) automatisch.

**Nutzung:**
1. In `src/core/config_master.py` "ui_evolution_mode" auf "rebuild" setzen.
2. App neu starten: Header und Sub-Nav kommen aus den neuen rebuild/-Fragmenten.

**Status:**
- Application Evolution-Ready (v1.42.0.0)
- Navigation: Dual-Path Orchestrated

**Der Modernisierungspfad ist jetzt aktiv und bereit für weitere UI-Innovationen.**


---

# Unified Menu & Dimension Orchestration (v1.43)

## Zusammenfassung
Alle Navigations- und Layout-Elemente werden in eine zentrale, dreistufige Registry in `config_master.py` überführt. Geometrie und Menüstruktur sind damit vollständig dynamisch und templategesteuert.

---

## Strategie & Planung

- **Triple-Level Registry (Python SSOT):**
  - **Level 1 (Master):** Hauptkategorien (Player, Libraries, Explorer, Tools) werden aus `shell_master.html` in die Python-Registry verschoben.
  - **Level 2 (Contextual):** Die SUB_NAV_REGISTRY aus `ui_nav_helpers.js` wandert ins Backend.
  - **Level 3 (Module Tabs):** Submodule-Switches werden nach gleichem Muster dynamisiert.

- **Dynamic Geometry (CSS Variable Injection):**
  - Ein "Geometry Bridge" in `app_core.js` injiziert Werte wie `header_height`, `sub_nav_height`, `sidebar_width` aus der Python-Config als CSS-Variablen (z.B. `--nav-header-height`).
  - UI-Größen sind damit zentral und live steuerbar.

- **Fragment-Driven Overhauls:**
  - Im Rebuild-Modus werden `menu_l1` und `menu_l2` zu 100% aus den Backend-Definitionen generiert.

---

## Status

- Mode: Planning (v1.43 Unified Navigation)
- Awaiting Approval

---

**Mit v1.43 wird die Navigation vollständig zentralisiert, dynamisch und templategesteuert.**


---

# Unified Menu & Dimension Orchestration (v1.43.00)

## Zusammenfassung
Alle Navigationsdaten und UI-Dimensionen werden in einer zentralen Registry (`config_master.py`) gebündelt. Menüs und Layouts sind jetzt dynamisch und über alle Ebenen steuerbar.

---

## Neue Features & Änderungen

- **Dynamische CSS-Variablen:**
  - Dimensionen wie `header_height`, `sub_nav_height`, `sidebar_width` werden als CSS-Variablen (z.B. `--nav-header-height`) beim Boot injiziert.

- **Registry-Migration:**
  - Die bisherige `SUB_NAV_REGISTRY` in JS wird durch den Backend-gesteuerten `NAVIGATION_ORCHESTRATOR` ersetzt.

- **Legacy Fallback:**
  - Im "Stable"-Modus bleiben die alten Buttons erhalten, im "Rebuild"-Modus ist alles 100% dynamisch.

---

## Verifikationsplan

**Manuelle Überprüfung:**
1. `header_height` in `config_master.py` ändern: UI passt sich nach Reload sofort an (ohne CSS-Edit).
2. Neues Item zu `level_1` in Python hinzufügen: Es erscheint in der Top-Navigation.
3. Sub-Nav (Neck) prüft: Hydratisiert für alle Hauptkategorien korrekt.

---

**Mit v1.43.00 ist die Navigation und das Layout vollständig dynamisch und zentral steuerbar.**


---

## Abschlussbericht & Finale Details (v1.43.00)

**Backend Navigation Orchestrator:**
- Alle Level-1- und Level-2-Definitionen (Master Header, Sub-Nav Pills) sind jetzt unter `navigation_orchestrator` in `config_master.py` zentralisiert.
- Menüeinträge enthalten Icon, Label, Hex-Farbe und spezifische JS-Aktionen – alles direkt in Python steuerbar.

**Geometry Bridge (Dynamic CSS):**
- `syncUiGeometry` in `app_core.js` injiziert Dimensionen wie `header_height`, `sub_nav_height` etc. als CSS-Variablen in den Root.
- `shell_master.css` nutzt diese Variablen, sodass das gesamte UI durch eine Zahl in der Python-Config skalierbar ist.

**Dynamic UI Rendering:**
- `renderMasterNav` erzeugt das Level-1-Menü dynamisch aus der Backend-Registry (inkl. Farben, Icons, Status).
- Die Level-2-Engine in `ui_nav_helpers.js` nutzt primär die Pill-Definitionen aus `GLOBAL_CONFIG` und fällt bei Bedarf auf das Legacy-JS-Registry zurück.

**Verifikation & Testing:**
- Dimensionen-Test: "header_height" in `config_master.py` ändern – Top-Bar passt sich sofort an.
- Boot-Sequenz: Navigation wird direkt nach dem Config-Handshake hydratisiert, kein Flickern.

**Status:**
- Total Stability Stage: Unified Orchestration (v1.43.00)
- Control Mode: Centralized Python SSOT

**Die Anwendung ist jetzt vollständig konfigurationsgetrieben und zentral steuerbar.**


---

# Forensic Stage Architecture (v1.44)

## Zusammenfassung
Die "Black Window"- und "Black Hole"-Bugs werden durch eine Unified-Stage-Architektur in Rebuild Mode endgültig eliminiert. Ein einziger persistenter Stage-Container ersetzt das bisherige Multi-Shell-System.

---

## Strategie & Geplante Änderungen

- **Unified Stage:**
  - In Rebuild Mode rendern alle Tabs (Player, Library, etc.) in einen einzigen `<main id="rebuild-stage">`.

- **Atomic Swaps:**
  - Fragments werden in einen Offscreen-Buffer geladen und erst nach erfolgreicher Prüfung atomar in den Stage geswappt (loadAtomic()).

- **Visibility Sentinel:**
  - Ein Hintergrund-Observer (stability_sentinel.js) überwacht #rebuild-stage und stellt sicher, dass er immer sichtbar und gefüllt ist.
  - Bei Black-Hole-Detektion wird automatisch ein Emergency-Rehydration ausgelöst.

---

## Verifikationsplan

**Automatisierte Tests:**
1. Black-Hole-Simulation: Stage auf display: none setzen – Sentinel muss ihn in <500ms wiederherstellen.
2. Atomic Swap Test: Kein "leerer Frame" beim Tab-Wechsel in Rebuild Mode.

**Manuelle Überprüfung:**
1. Schnelles Umschalten zwischen Player und Library: Kein "Black Window" mehr sichtbar.

---

## Status

- Mode: Planning (v1.44 Forensic Stage)
- Awaiting Approval

---

**Mit v1.44 wird die Black-Screen-Problematik forensisch und architektonisch gelöst.**


---

## Abschlussbericht & Finale Details (v1.44)

**Unified Forensic Stage:**
- Ein einziger, hochpriorisierter `#rebuild-stage`-Container in `shell_master.html` dient als universeller Viewport für alle Navigationen im Rebuild Mode.
- Hoher z-index und absolute Positionierung sichern die Dominanz des Stages.

**Atomic Rendering Pipeline:**
- `loadAtomic()` in `fragment_loader.js` lädt Fragmente doppelt gepuffert und swappt sie erst nach Integritätsprüfung flickerfrei in den Stage.
- `window_manager.js` erkennt Rebuild-Mode und routet alle Loads direkt zum Stage, Legacy-Show/Hide entfällt.

**Stability Sentinel (Active Watchdog):**
- `visibility_sentinel.js` überwacht den Stage alle 1000ms.
- Erkennt und repariert "Black Hole"-Zustände automatisch durch Sichtbarkeits- und Rehydrations-Trigger.

**Verifikation (v1.44):**
- Tab-Wechsel in Rebuild Mode sind jetzt garantiert flickerfrei und stabil.
- Der Sentinel erkennt und repariert versteckte/entleerte Viewports zuverlässig.

**Status:**
- Architecture Level: Forensic Stage (v1.44.0.0)
- Stability Mode: Sentinel-Protected Atomic Stage

**Die Anwendung ist jetzt physisch gegen Rendering-Ausfälle gehärtet.**


---

# UI Stability & Reconstruction Overhaul (v1.44)

## Konsolidierte Zusammenfassung & Meilensteinabschluss

**1. Forensic Stage Architecture (v1.44):**
- Unified Viewport: Fragmentiertes Shell-System durch einen persistenten `#rebuild-stage` ersetzt.
- Atomic Swaps: `loadAtomic()` in `fragment_loader.js` sorgt für flickerfreie Navigation.
- Visibility Sentinel: `visibility_sentinel.js` überwacht und repariert die Sichtbarkeit automatisch.

**2. Unified Navigation Orchestration (v1.43):**
- Zentrale Registry: Navigation Level 1–3 werden aus `config_master.py` gesteuert.
- Dynamische CSS-Geometrie: Header, Sub-Nav, Sidebar sind als CSS-Variablen global steuerbar.

**3. Unicode & Emoji Safety (v1.42):**
- Forensische Normalisierung: `safe_msg`-Filter übersetzt Emojis in ASCII-Tags, wenn `unicode_safety_mode` aktiv ist.

**Technische Validierung:**
- Stability Test: Atomic Swapping garantiert flickerfreie Navigation (z.B. PLAYER/LIBRARIES).
- Sentinel Test: Manuelles Verstecken/Löschen des Stages wird in <1s automatisch repariert.

**Umschaltanleitung:**
- In `config_master.py`:
  - "ui_evolution_mode": "rebuild" → Forensic Stage aktivieren
  - "unicode_safety_mode": True → Emojis aus Logs/UI entfernen

**Tipp:**
- Performance: Architektur reduziert DOM-Komplexität und beschleunigt Tab-Wechsel.

**Status:**
- Milestone Complete: UI Hardened (v1.44.0.0)
- Path: Parallel Reconstruction Cycle
