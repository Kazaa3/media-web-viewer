# Walkthrough – Media Viewer Modularization & Theming (Meilenstein 1)

## Übersicht
Nach erfolgreicher Umsetzung der Modularisierung und Einführung eines modernen Theme-Systems ist die Media Viewer Anwendung nun deutlich wartungsfreundlicher, performanter und optisch ansprechender.

---

## 1. Architektur-Überblick
- **app.html**: Reduziert auf ~500 Zeilen, dient als schlanker Shell-Container. Alle 12 Kern-Tabs wurden in eigenständige Fragmente ausgelagert (`web/fragments/`).
- **web/fragments/**: Enthält die modularisierten UI-Komponenten (z.B. Player, Bibliothek, Tools, Logbuch, Diagnostics etc.).
- **ui_nav_helpers.js**: Stellt ein Mapping zwischen Tabs und Fragment-Containern bereit. Lädt Fragmente dynamisch und initialisiert sie bedarfsgerecht.
- **js/environment.js**: Zentrale Verwaltung von globalem State und Konfiguration für alle Module.

---

## 2. Dynamisches Fragment-Loading
- Beim Tab-Wechsel wird das entsprechende Fragment asynchron geladen und in den zugehörigen Container eingefügt.
- Initialisierungshooks sorgen für die korrekte Aktivierung von Modullogik (z.B. `loadLibrary()`, `refreshFilesystem()`).
- Performance: Die Startzeit der Anwendung ist durch das "on demand"-Laden der Module deutlich verbessert.

---

## 3. Theme-System (Light/Dark)
- **main.css**: Definiert CSS-Variablen für Farben, Transparenzen und Effekte im Glassmorphic-Stil.
- **theme_helpers.js**: Enthält Logik für Theme-Umschaltung und Persistenz (localStorage).
- **SVG-Toggle**: Im Header platziert, ermöglicht fließenden Wechsel zwischen Light- und Dark-Theme.
- User-Präferenz wird gespeichert und beim nächsten Start automatisch angewendet.

---

## 4. Fehlerbehebung & Stabilisierung
- Nach einem Extraktionsfehler wurden die Fragmente Logbuch, Tools und Diagnostics erfolgreich wiederhergestellt.
- Funktionale Parität mit der ursprünglichen monolithischen Version wurde für alle Module sichergestellt.

---

## 5. Verifikation
- Alle Fragmente wurden manuell und automatisiert getestet (UI-Test-Suite).
- Konsistenz, Performance und Theme-Umschaltung wurden überprüft.
- Keine Funktionseinbußen gegenüber der alten Version.

---

## 6. Ausblick
- Die neue Architektur ermöglicht eine einfache Erweiterung um weitere Module und Features.
- Das Theme-System kann um weitere Varianten ergänzt werden.

---

## 7. Final Polish (dict v1.34)
- **Header-Controls konsolidiert**: Der Hamburger-Button wurde aus dem Floating-Bereich in den Top-Header verlegt (neben Theme-Toggle), sodass Systemaktionen zentral und ergonomisch erreichbar sind.
- **Auto-Scan beim Erststart**: Wenn die Bibliothek beim Start leer ist, wird automatisch ein Initial-Scan von `/media` ausgelöst, damit Titel direkt in Queue und Player verfügbar sind.
- **Terminologie standardisiert**:
	- "Items" wurde vollständig ersetzt.
	- "Titel" für Player, Queue und Playlists.
	- "Medien / Mediathek" für Zähler und Verwaltungsansichten.
- **Bedienhinweis**: Das Programmmenü kann per `Alt` oder über den neuen Header-Menübutton geöffnet werden.

### Manuelle Schnellprüfung
- Header: Menübutton und Theme-Toggle sichtbar und bedienbar.
- Erststart mit leerer Bibliothek: Auto-Scan startet ohne zusätzliche Nutzeraktion.
- Queue/Player: Medien sind nach Scan sichtbar und direkt abspielbar.
- UI-Wording: Keine sichtbaren "Items"-Labels mehr vorhanden.

---

## 8. Navigation Restoration & Cross-Stack Logging
- **Sidebar-Restoration abgeschlossen**: `Edit`, `Reporting`, `Debug & DB` und `Testing` sind wieder als primäre Bereiche in der Sidebar erreichbar.
- **Library-Domain-Navigation eingeführt**: Der Bereich `Library` fungiert nun als Container für:
	- `Mediathek`
	- `Dateibrowser`
	- `Inventar`
- **Sub-Tab-Bug behoben**: Shorthand-Aufrufe wie `File` werden nicht mehr durch die Standardansicht `Visual` überschrieben.
- **Cross-Stack-Logging aktiviert**:
	- Backend: `log_gui_event` nimmt Frontend-Traces entgegen.
	- Frontend: `mwv_trace` protokolliert Navigation und Zustandswechsel.
	- DOM/Playwright: Browser-Konsole wird in die Testausgabe gespiegelt.
- **Verifiziert**: Sidebar-Kategorien sind erreichbar, Library-Domains schalten korrekt, Logging ist für Diagnosepfade verfügbar.

### Verifikation
- Server-Logs bestätigen Frontend-Navigation und Domain-Wechsel.
- Automatisierte Browser-Verifikation bestätigt Erreichbarkeit der Sidebar-Ziele.
- Library-Subnavigation wechselt stabil zwischen `Mediathek`, `Dateibrowser` und `Inventar`.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4

---

## 9. Walkthrough – Menu Entry Restoration (v1.34)
- **Fehlende Menüeinträge wiederhergestellt**: `Reporting` und `System Test` sind wieder über die togglebare Programm-Menüleiste erreichbar.
- **Top-Menü erweitert**: Das per `Alt` einblendbare Menü spiegelt jetzt alle primären Sidebar-Kategorien:
	- `Editor`
	- `Core Tools`
	- `Reporting`
	- `System Test`
- **Dynamische globale Sub-Navigation**: Unterhalb des Headers wurde eine sekundäre, horizontale Breadcrumb-/Pill-Leiste ergänzt. Sie füllt sich abhängig von der aktiven Hauptkategorie automatisch mit passenden Einträgen.

### Sub-Navigation nach Kategorie
- **Reporting**:
	- `Dashboard`
	- `DB Stats`
	- `Video Health`
	- `Parser Hub`
- **Tests**:
	- `System Health`
	- `Debug DB`
	- `Latency Profile`
- **Media**:
	- `Audio Player`
	- `Library Browser`
	- `Playlists`
- **Edit**:
	- `Metadata Tags`
	- `Artwork Lab`
	- `Media Analysis`

### UI- und UX-Verfeinerung
- **Glassmorphic Pills**: Die neue Sub-Navigation übernimmt dieselbe hochwertige Designsprache wie Header, Sidebar und Footer.
- **Aktive Zustandsanzeige**: Der aktive Sub-Navigationseintrag wird automatisch hervorgehoben und synchronisiert sich mit View-Wechseln.
- **Schnellerer Zugriff auf tiefe Module**: Versteckte Unterbereiche müssen nicht mehr über Scrollen oder indirekte Routen gesucht werden.

### Verifikation
- `Alt` drücken und prüfen, dass das obere Programmmenü sichtbar wird.
- `Reporting` oder `System Test` auswählen und bestätigen, dass die oberen Sub-Navigations-Pills erscheinen.
- Zwischen den Sub-Modulen wechseln und prüfen, dass die aktive Markierung korrekt mitspringt.
- Auch bei `Editor` und `Tools` prüfen, dass die neue Top-Sub-Navigation konsistent befüllt wird.

### Technische Zuordnung
- Shell/Struktur: `app.html`
- Routing/Navigationslogik: `ui_nav_helpers.js`
- Styling/Glassmorphism/Active State: `main.css`

**Tipp:**
Die neue globale Sub-Navigation macht tiefere Bereiche wie `Parser Hub`, `Debug DB` oder `Artwork Lab` direkt aus dem aktiven Kontext erreichbar.
