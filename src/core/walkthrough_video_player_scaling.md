## Logbuch: Fix Logbuch-Tab Rendering & Layout (26.03.2026)

- **Problem:** Logbuch-Tab zeigte weißen Bildschirm, Einträge wurden nicht geladen.
- **Ursache:**
  - Fehlende Backend-Funktion `read_file` verhinderte das Laden der Markdown-Dateien.
  - HTML-Strukturfehler: Fehlender Schließ-Tag bei `video-queue-pane` führte dazu, dass der Logbuch-Panel im DOM versteckt/nicht sichtbar war.
- **Lösung:**
  - `read_file` in main.py implementiert.
  - HTML-Struktur geprüft und fehlenden Schließ-Tag ergänzt.
  - Gesamtes Layout auf weitere Strukturfehler auditiert.
- **Ergebnis:** Logbuch-Tab lädt und zeigt Markdown-Einträge wieder korrekt an. Layout ist stabil.
## Walkthrough: Media Library Expansion & Playback Debugging (26.03.2026)

### Key Accomplishments
1. **Video Library Expansion**
  - **Dedicated Video View:** "Videos"-Sub-Tab in der Bibliothek mit responsivem Card-Grid.
  - **Persistence Layer:** `playback_position` und `duration_sec` werden in der Datenbank getrackt, um Videos an letzter Stelle fortzusetzen.
  - **Hover Preview:** YouTube-ähnlicher Hover-Effekt, der eine stummgeschaltete Vorschau auf der Karte abspielt.
  - **CD-Style Albums:** Album-Ansicht nutzt 1:1-Format mit `object-fit: contain` für unbeschnittene Cover.
  - **Datenbank View:** Neuer "Datenbank"-Sub-Tab mit durchsuchbarer Tabelle aller indizierten Medien und Schnellaktionen für Playback und Metadatenbearbeitung.

2. **Enhanced Video Format Test Suite**
  - **ISO Support:** .iso-Dateien werden automatisch in die Test-Suite aufgenommen.
  - **Real-Time Playback Monitoring:** `monitorVjsPlayback` prüft echte Frame-Bewegung statt nur Player-Init.
  - **Automated UI Flow:** Tests wechseln automatisch in den "Video"-Tab für visuelles Feedback.

3. **Critical Playback Debugging**
  - **Circular Dependency Fix:** Kritischer Fehler durch zirkulären Import in `VideoHandler` behoben (Remux-Logik ausgelagert nach `remux_utils.py`).
  - **Signature Mismatch:** Fehlerhafte `playVideo`-Aufrufe aus der Test-Suite korrigiert.
  - **Robustness:** `analyze_media` global mit try-except abgesichert, Frontend-Fehlermodal zeigt jetzt technische Exception-Details.

### Visual Proof
- **Video Streaming Selection:** Automatisierte Test-Suite läuft mit verschiedenen Videoformaten.
- **Playback Error Modal:** Neues Debugging-Modal zur Identifikation von Media-Analyse-Fehlern.

### Technical Changes
**Backend:**
- `src/core/main.py`: `analyze_media` refaktoriert, Remux-Logik ausgelagert.
- `src/core/remux_utils.py`: Neue Utility zur Auflösung von Abhängigkeitskreisen.
- `src/core/handlers/video_handler.py`: Importe aktualisiert.
**Frontend:**
- `web/app.html`: `playVideo`-Aufrufe gefixt, `onPlaylistItemClick` verbessert, Modal-Fehleranzeige erweitert.
## Walkthrough: Media Library & Video Verification (26.03.2026)

### 1. Library & UI Expansions
Die Bibliothek wurde um zwei neue Navigations-Ebenen erweitert:

- **Album View:** Eine quadratische CD-Cover Ansicht (1:1), die Cover im Originalformat (un-cropped) anzeigt.
- **Folge-View:** Eine dedizierte Ansicht für Serien und aufeinanderfolgende Medien.
- **Video Grid:** Ein modernes YouTube-ähnliches Grid mit Hover-Preview und Fortschrittsbalken.

### 2. Video Test-Suite (Enriched)
Die Test-Matrix im Reporting-Tab kann nun die tatsächliche Wiedergabe validieren:

- **Playback Monitoring:** Das System misst, ob der Player wirklich Frames abspielt (currentTime > 0.1s).
- **Fehler-Erkennung:** Video.js Fehler (z.B. Codec-Inkompatibilität) werden abgefangen und in der Historie geloggt.
- **ISO/DVD Support:** .iso Dateien werden jetzt automatisch zu VLC geroutet und sind Teil der Test-Matrix.
- **Technical Feedback:** Ein neues Modal zeigt bei Fehlern detaillierte Codec- und Routing-Infos an.

### 3. Playback Persistence
- **Auto-Resume:** Die Anwendung speichert alle 5s die Position und stellt sie beim nächsten Start wieder her.
- **Progress Sync:** Die Duration wird beim ersten Playback synchronisiert, um korrekte Balken im Grid zu zeigen.

### 4. Codec & Routing Fixes
- **MP4 Direct Play:** Bug im Path-Mapping für /direct/ behoben.
- **ISO Routing:** Korrektes Routing zu VLC für Disk-Images statt FFmpeg-Transcode.

### Verification Results
- **Video Library:** Alle Kategorien (Film, Serie, etc.) sichtbar.
- **Album View:** Korrektes 1:1 Aspect Ratio und proportionales Scaling.
- **Test Suite:** Automatischer Tab-Wechsel und Playback-Validierung aktiv.
- **Persistence:** Positionen bleiben über Sessions hinweg erhalten.
## Update: Album-Card-Format, ISO/DVD-Routing & Playback-Error-Modal (26.03.2026)

### Verbesserte Album-Ansicht
- Albumkarten nutzen jetzt ein quadratisches CD-Cover-Format (1:1) für authentische, visuell geordnete Darstellung.
- Cover werden mit `object-fit: contain` im Original-Seitenverhältnis angezeigt – kein Artwork geht verloren.

### Robustes Video-Routing für ISO/DVD
- ISO/DVD-Dateien werden automatisch an VLC weitergeleitet, statt im Browser transkodiert zu werden.
- Dadurch funktionieren Menüs und komplexe Disc-Strukturen stabil und originalgetreu.

### Playback Error Modal & Debugging
- Ein neues Playback-Error-Modal erscheint, wenn ein Video nicht geladen werden kann.
- Das Modal zeigt technische Metadaten (Video-/Audio-Codecs, Quality Score, Routing Mode, Dateipfad) zur schnellen Fehleranalyse.
- Hilft beim Testen und Debuggen von problematischen Formaten und Codecs.

**Fazit:**
Diese Verbesserungen sorgen für ein hochwertigeres Album-Erlebnis und bieten volle technische Transparenz bei der Videowiedergabe und beim Debugging.

## Walkthrough: Media Library & Video Streaming Enhancements (26.03.2026)

## Update: Neue Sub-Tabs "Album" & "Der Folgende" sowie Video Library/MP4-Fixes (26.03.2026)

### Neue Sub-Tabs in der Bibliothek
- **Album-Ansicht:** Eigener Unterreiter, der alle Audiodateien nach Album gruppiert. Ermöglicht das Durchstöbern und Abspielen kompletter Alben mit nur einem Klick.
- **Der Folgende (TV/Serien):** Spezieller Sub-Tab für Serien und Episoden. Hier können Nutzer direkt in ihre Lieblingsserien einsteigen und die nächste Folge abspielen.

### Video Library & MP4-Playback Fixes
- **Leere Video-Library behoben:** Die Filterlogik für Videos wurde erweitert, sodass alle relevanten Kategorien und Dateitypen erkannt werden. Dadurch werden jetzt alle Videos korrekt im Streaming-Tab angezeigt.
- **MP4-Playback repariert:** Ein Fehler in der Pfadauflösung im Backend wurde behoben. MP4-Dateien werden jetzt zuverlässig abgespielt, unabhängig vom Ursprungsort oder der Kategorie.

### UI & Konsistenz-Verbesserungen
- Einheitliches Playback-Routing: Das Abspielen von Medien funktioniert jetzt konsistent über Sidebar, Playlists und Bibliothek hinweg.
- Navigation: Die neuen Sub-Tabs sind direkt in der Bibliothek verfügbar und bieten eine übersichtliche Navigation für verschiedene Medientypen.
- Walkthrough und Logbuch wurden mit Details zu den neuen Navigationsfeatures und Bugfixes aktualisiert.

**Hinweis:** Die neuen Tabs findest du im Bibliotheksbereich. Bei weiteren Wünschen oder Anpassungen bitte melden!

### 1. Dedizierte Video-Bibliothek
Ein neuer "Videos"-Sub-Tab wurde zur Bibliothek hinzugefügt und bietet ein modernes, YouTube-ähnliches Grid für komfortables Browsen.

**Key Features:**
- Responsive Grid: Dunkles, modernes Layout, optimiert für Videoinhalte
- Hover-to-Play Previews: Mouseover auf eine Video-Karte startet eine stummgeschaltete, loopende Vorschau
- Visuelle Fortschrittsbalken: Bereits angesehene Videos zeigen einen roten Fortschrittsbalken am Thumbnail

**Video Library Overview:**
Beispiel für das neue Video-Streaming-Grid mit Hover-Preview und Fortschrittsanzeige.

### 2. Playback Position Persistence
Die Anwendung merkt sich jetzt automatisch, wo du in jedem Video aufgehört hast.

**Funktionsweise:**
- Automatisches Speichern: Während der Wiedergabe wird die Position alle 5 Sekunden in der Datenbank gespeichert
- Nahtloses Fortsetzen: Beim erneuten Abspielen springt der Player automatisch zur letzten gespeicherten Position
- Datenbank-Backend: Nutzt die neuen Spalten `playback_position` und `last_played` in der `media`-Tabelle

### 3. Media Routing & Reporting
Das Reporting-Dashboard wurde um detaillierte Metriken zu Video-Codecs und Routing-Performance erweitert.

- Codec Distribution: Visuelle Aufschlüsselung der Videoformate in der Bibliothek
- Routing Analysis: Detaillierte Reports, ob ein Video per Direct Remux, HLS Fallback oder Transcoding abgespielt wurde

**Verifikation:**
Alle Backend-Persistence-APIs und Frontend-UI-Komponenten sind funktional und getestet.
---

## Task-Status: Media Library Expansion & Video Library (26.03.2026)

### Status
- Video Player Sichtbarkeit repariert (redundante Tags entfernt)
- Bug bei absoluter Pfadauflösung im /direct/-Route behoben
- get_routing_suite_report via Eel bereitgestellt
- Video Player Architektur im Logbuch dokumentiert
- Routing Test Suite erweitert
- Video Library & Persistence:
  - Backend: Spalten playback_position, last_played, duration_sec zur media-Tabelle hinzugefügt
  - Backend: Persistence-API in db.py implementiert
  - Backend: Persistence-API in main.py via Eel bereitgestellt
  - Frontend: "Videos"-Sub-Tab in der Bibliothek ergänzt
  - Frontend: Video Streaming Grid mit Hover-Preview umgesetzt
  - Frontend: Video.js an Persistence-API angebunden (Progress speichern/laden)

### Verifikation & Final Polish
- End-to-End-Test der Persistence (Schema und Backend-Logik verifiziert)
- Walkthrough mit Video-Library-Demo aktualisiert
- Media-Duration-Sync für exakte Fortschrittsbalken

### Details: Video Streaming Library
- Dedizierter Sub-Tab in der Bibliothek
- YouTube-ähnliches Card-Layout mit Hover-to-Play-Vorschau
- Fortschrittsbalken auf Video-Karten für angefangene Inhalte
- Automatische Positionswiederherstellung beim Starten der Wiedergabe
- Dynamisches Duration-Syncing für stets akkurate Fortschrittsanzeigen

### Details: Media Routing Tests
- Validierung der direct-, transcode- und hls-Logik
- Funktionaler Test für alle wichtigen Streaming-Endpunkte
---

## Walkthrough: Finalisierung Video Library & Playback Persistence (26.03.2026)

### Highlights
- **Full Persistence:** Der Player merkt sich Wiedergabeposition und Gesamtdauer jedes Videos – auch nach Neustart.
- **Verbesserte UI:** Der Video-Library-Unterreiter nutzt ein responsives Grid mit Hover-to-Play-Previews und Fortschrittsanzeige.
- **Backend-Stabilität:** Das Datenbankschema ist geprüft, alle Persistence-Spalten sind korrekt indiziert und werden via Eel aktualisiert.
- **Auto-Sync:** Die Frontend-Logik synchronisiert die Videodauer automatisch mit dem Backend, sodass der Fortschritt für alle Medien exakt getrackt wird.

**Details zur Implementierung und Verifikation sind in task.md und walkthrough.md dokumentiert.**
---

## Notiz: MongoDB als Alternative für Medienverwaltung (26.03.2026)

**Was ist MongoDB?**
MongoDB ist eine dokumentenorientierte NoSQL-Datenbank. Sie speichert Daten als flexible JSON-ähnliche Dokumente (BSON) statt in starren Tabellen.

**Vorteile:**
- Sehr flexibel bei sich ändernden oder unstrukturierten Daten (z.B. Medien mit variablen Metadaten, viele Cover, Scraper-Infos)
- Keine feste Schemadefinition nötig, Felder können je Dokument unterschiedlich sein
- Gute Skalierbarkeit und Performance bei großen Datenmengen
- Einfache Speicherung von verschachtelten Strukturen (z.B. Listen von Covern, Autoren, Editionen)

**Nachteile:**
- Keine klassischen SQL-Tabellen, keine Joins wie in relationalen DBs
- Konsistenz und Transaktionen eingeschränkt im Vergleich zu SQL
- Für sehr strukturierte, relationale Datenmodelle weniger geeignet

**Einsatzszenario:**
MongoDB eignet sich besonders, wenn Medienobjekte sehr unterschiedliche oder dynamische Metadaten haben, viele verschachtelte Listen (z.B. mehrere Cover, Autoren, Editionen) oder wenn das Datenmodell häufig angepasst werden muss.

**Fazit:**
Für klassische Medienverwaltungen mit klaren Beziehungen ist SQL/SQLAlchemy meist besser. Für sehr flexible, dynamische Medien- und Metadatenstrukturen kann MongoDB eine sinnvolle Alternative sein.
---

## Notiz: Migration von Datenbanken (26.03.2026)

**Was ist eine Migration?**
Eine Migration bezeichnet die Übertragung von Daten und/oder Struktur von einer Datenbank in eine andere – z.B. von SQLite nach PostgreSQL, von einer alten Struktur auf ein neues Modell oder zwischen verschiedenen DB-Typen.

**Typische Migrationsszenarien:**
- Wechsel von SQLite auf PostgreSQL/MySQL für bessere Skalierbarkeit
- Umstellung von Einzel-DB auf Multi-DB-Architektur
- Strukturänderungen (z.B. neue Felder, Tabellen, Beziehungen)
- Zusammenführung oder Aufteilung von Datenbanken

**Herausforderungen:**
- Datenkonsistenz und -integrität sicherstellen
- Migration von Beziehungen, Fremdschlüsseln, Indizes
- Umgang mit großen Datenmengen (Performance, Downtime)
- Anpassung von Applikationslogik und Schnittstellen

**Tools & Strategien:**
- ORMs wie SQLAlchemy bieten Migrations-Frameworks (z.B. Alembic) für strukturierte, versionierte Migrationen
- Für reine Datenmigration: Export/Import (CSV, SQL-Dump, ETL-Tools)
- Schrittweise Migration (z.B. Shadow-DB, Parallelbetrieb, schrittweises Umschalten)

**Empfehlung:**
- Migrationen immer testen und dokumentieren (Testdatenbank, Backups!)
- Automatisierte Migrationsskripte nutzen, keine manuellen Einzeländerungen
- Nach Migration: Validierung der Daten und Funktionstests durchführen
---

## Notiz: Multi-Datenbank-Strategien für unterschiedliche Medientypen (26.03.2026)

**Ansatz:**
Es ist möglich, in einer Anwendung mehrere Datenbanken parallel zu betreiben – z.B. eine SQLite-DB für Items, eine weitere für komplexe Medienobjekte (DVDs, Bücher, etc.), oder sogar verschiedene DB-Typen (z.B. SQLite + PostgreSQL/GraphDB).

**Vorteile:**
- Trennung der Datenmodelle nach Medientyp (z.B. Audio, Video, Bücher, Sammlungen)
- Optimierung der jeweiligen DB-Struktur und Abfragen für den konkreten Anwendungsfall
- Unabhängige Skalierung und Wartung der einzelnen Datenbanken

**Nachteile:**
- Komplexere Verwaltung und Synchronisation zwischen den Datenbanken
- Höherer Entwicklungs- und Wartungsaufwand

**Empfehlung:**
- Für einfache Szenarien reicht meist eine zentrale DB mit klaren Tabellen für die verschiedenen Typen.
- Bei sehr unterschiedlichen Anforderungen (z.B. klassische Items vs. komplexe Sammlungsobjekte) kann eine Multi-DB-Strategie sinnvoll sein.
- Wichtig: Klare Schnittstellen und Synchronisationsmechanismen zwischen den Datenbanken definieren.
---

## Notiz: SQLite-Limits und Skalierbarkeit für Item-Verwaltung (26.03.2026)

**Aktuelle Definition:**
Die Item-Verwaltung nutzt SQLite als Datenbank.

**Wie viele Items können verwaltet werden?**
- SQLite kann theoretisch bis zu ca. 140 Terabyte pro Datenbankdatei speichern (praktisch meist durch das Dateisystem limitiert).
- Einzelne Tabellen können bis zu 2^64 Zeilen enthalten.
- Die maximale Zeilengröße beträgt standardmäßig 1 GB (kann kompiliert werden).
- Die Anzahl gleichzeitiger Schreibzugriffe ist begrenzt, da SQLite keine echte Mehrbenutzer-DB ist.

**Fazit:**
Für Einzelplatz- und kleine Mehrbenutzeranwendungen ist SQLite für sehr große Item-Mengen (Millionen Datensätze) geeignet. Bei massiv parallelem Zugriff oder extremen Datenmengen empfiehlt sich ein Umstieg auf PostgreSQL/MySQL.
---

## Logbuch: Datenbankstrategie für Item- und Objektverwaltung (26.03.2026)

### Ausgangslage
Im System gibt es aktuell zwei zentrale Begriffe:
- **Item:** Einzelnes Medium (z.B. Musikstück, Track), aktuell mit SQLite verwaltet.
- **Objekt:** Übergeordnete Medienobjekte (z.B. DVD, Buch, Sammlung), die komplexere Metadaten, Cover, Scraper-Informationen etc. benötigen.

### Optionen für die zentrale Medienverwaltung

**1. SQLite (klassisch, wie bei Items):**
- Einfach, schnell, für kleine/mittlere Datenmengen geeignet.
- Relationale Struktur, aber wenig Komfort bei komplexen Beziehungen und Migrationen.

**2. SQLAlchemy (ORM für relationale DBs):**
- Abstraktionsschicht für verschiedene relationale Datenbanken (SQLite, PostgreSQL, MySQL).
- Komfortable Modellierung von Objekten, Beziehungen, Migrationen und Abfragen.
- Ideal für strukturierte Medienverwaltung mit vielen Feldern (Titel, Jahr, Cover, Scraper-Metadaten, etc.).
- Unterstützt flexible Erweiterung und spätere Migration auf größere DB-Systeme.

**3. Graphdatenbanken (z.B. Neo4j):**
- Speziell für sehr komplexe, dynamische Beziehungsnetze (z.B. Serien, Editionen, Autoren, Empfehlungen).
- Abfragen nach Verbindungen/Netzwerken sind sehr effizient.
- Für klassische Listen/Tabellen weniger geeignet.

### Speicherstruktur für Medienobjekte
- Medienobjekte (z.B. DVD-Images, Cover) können nach logischer Struktur im Dateisystem abgelegt werden:
  - Beispiel: `/Medien/DVDs/Titel (Jahr)/Titel CD2.iso`, `/Medien/DVDs/Titel (Jahr)/cover.jpg`
- Die Datenbank (z.B. via SQLAlchemy) speichert Pfade, Metadaten und Verknüpfungen.
- Diese Struktur erleichtert das Parsen, Scrapen und die spätere Automatisierung.

### Empfehlung
- Für Items kann SQLite bestehen bleiben.
- Für komplexere Medienobjekte und zentrale Verwaltung ist SQLAlchemy (mit SQLite oder PostgreSQL) ideal.
- Graphdatenbanken nur bei Bedarf an hochkomplexen Beziehungen.
- Medienobjekte und Cover sollten nach klarer Ordnerstruktur abgelegt werden, Pfade und Metadaten in der DB.

**Stichwort:** DVD-Objekte mit .iso und Cover nach Schema `Titel (Jahr)` im Ordner, um Parser und Scraper zu unterstützen.
---

## Entscheidungsnotiz: Datenbankstrategie für zentrale Medienverwaltung (26.03.2026)

**Ziel:**
Alle CDs, DVDs, Bücher und weitere Medientypen sowie deren Metadaten (inkl. diverser Coverbilder) sollen zentral erfasst und verwaltet werden.

**Option 1: SQLAlchemy (relationale DB, z.B. SQLite/PostgreSQL)**
- Sehr gut geeignet für strukturierte Medienverwaltung mit klaren Tabellen (Medien, Autoren, Cover, Kategorien etc.).
- ORM-Komfort, Migrationen, flexible Abfragen, große Community.
- SQLite für kleine/mittlere Projekte ausreichend, für größere Datenmengen/Mehrbenutzerbetrieb besser PostgreSQL.
- Speicherung von Metadaten und Coverpfaden/Binärdaten problemlos möglich.

**Option 2: Graphdatenbank (z.B. Neo4j)**
- Sinnvoll bei sehr komplexen, dynamischen Beziehungen (z.B. Netzwerke, Empfehlungen, Serien, Editionen, Vererbungen).
- Ideal für verschachtelte Sammlungen und Beziehungsabfragen, aber weniger für klassische Listen/Tabellen.

**Empfehlung:**
- SQLAlchemy mit relationaler DB ist für die meisten Medienverwaltungen ausreichend, wartbar und flexibel.
- Graphdatenbank nur bei sehr komplexen, dynamischen Beziehungsnetzen nötig.
- Bestehende SQLite-DB für Items kann weiter genutzt werden, zentrale Medienverwaltung kann auf SQLAlchemy umgestellt werden.

**Hinweis zu Coverbildern:**
- Speicherung als Datei (mit Pfad in der DB) ist meist effizienter als als BLOB.

**Fazit:**
SQLAlchemy ist für das Ziel sehr gut geeignet und flexibel erweiterbar. Graphdatenbank nur bei Bedarf an hochkomplexen Beziehungen.
---

## Anleitung: Unterreiter "Bibliothek" in der Bibliotheksansicht erstellen (26.03.2026)

Um den Unterreiter "Bibliothek" in der Bibliotheksansicht zu erstellen, sind folgende Schritte im Frontend (z.B. in web/app.html) notwendig:

1. **Tab-Button ergänzen:**
  Im Tab-Bereich der Bibliothek einen neuen Button hinzufügen:
  ```html
  <button id="library-tab-bibliothek" onclick="switchLibrarySubTab('bibliothek')">Bibliothek</button>
  ```

2. **Container für die Ansicht erstellen:**
  ```html
  <div id="lib-view-bibliothek" class="lib-view" style="display:none;">
    <!-- Hier werden alle Medien gelistet -->
  </div>
  ```

3. **switchLibrarySubTab anpassen:**
  In der Funktion `switchLibrarySubTab` die Logik ergänzen, um den neuen Unterreiter anzuzeigen:
  ```js
  function switchLibrarySubTab(tab) {
    // ...existing code...
    document.getElementById('lib-view-bibliothek').style.display = (tab === 'bibliothek') ? '' : 'none';
    // ...existing code...
  }
  ```

4. **Rendering der Medienliste:**
  Die Medienliste im neuen Container per JS dynamisch rendern.

Optional: Ein vollständiger Code-Snippet für app.html oder die JS-Logik kann auf Wunsch bereitgestellt werden.
---

## Geplant: Unterreiter "Bibliothek" in der Bibliothek (26.03.2026)

Ein neuer Unterreiter "Bibliothek" wird im Bibliotheksbereich eingeführt. Dieser dient als zentrale Übersicht aller Medien, unabhängig von Typ oder Status.

### Features
- Gesamtliste aller Medien (Audio, Video, Bilder etc.)
- Einheitliche Such- und Filterfunktionen
- Direkter Zugriff auf Medieninfos, Aktionen und Status
- Grundlage für weitere Unterreiter wie "Videos", "Datenbank" etc.

### Nächste Schritte
- UI-Integration des "Bibliothek"-Tabs
- Backend-Anpassung für vollständige Medienabfrage
- Verknüpfung mit bestehenden und geplanten Unterreitern
---

## Geplant: Sortierung, Statusanzeige & Ordneransicht in der Bibliothek (26.03.2026)

### Ziel
Die Bibliothek erhält erweiterte Sortieroptionen, eine Statusanzeige für Medien (z.B. gescrappt, analysiert, fehlerhaft) und eine Ordneransicht zur besseren Navigation durch die Medienstruktur.

### Features
- Sortierung nach Name, Datum, Typ, Status etc.
- Filter- und Suchoptionen für gezielte Medienauswahl
- Status-Icons oder Badges für Medien (z.B. "neu", "fehlerhaft", "vollständig")
- Ordneransicht: Anzeige der Medien nach Verzeichnisstruktur, inkl. Auf- und Zuklappen

### Nächste Schritte
- UI-Design für Sortier- und Filterfunktionen
- Implementierung der Statusanzeige und Badges
- Integration der Ordneransicht in die Bibliothek
- Backend-Anpassungen für Status- und Verzeichnisabfragen
---

## Geplant: Unterreiter "Datenbank" in der Bibliothek (26.03.2026)

Ein neuer Unterreiter "Datenbank" wird in der Bibliothek eingeführt. Dieser dient als zentraler Ort, um Medien zu scrappen, Metadaten zu erfassen und Datenbankoperationen durchzuführen.

### Features
- Übersicht aller gescrappten Medien und Metadaten
- Buttons/Tools zum Anstoßen von Scraping- und Analyseprozessen
- Möglichkeit, Medien manuell zu aktualisieren oder zu taggen
- Zentrale Verwaltung und Monitoring von Datenbank-Operationen

### Nächste Schritte
- UI-Design und Integration des "Datenbank"-Tabs in die Bibliothek
- Backend-Anbindung für Scraping- und Analysefunktionen
- Dokumentation und Testfälle für die neuen Workflows
---

## Implementation Plan: Video Library & Persistence (26.03.2026)

### Ziel
Eine dedizierte Video-Bibliothek mit Hover-to-Play und persistenter Wiedergabeposition.

### Geplante Änderungen

**Datenbank (Python):**
- `init_db()` um die Spalten `playback_position` (REAL) und `last_played` (TEXT) in der `media`-Tabelle erweitern.
- Funktionen `update_playback_position(path, position)` und `get_playback_position(path)` implementieren.

**Backend (Python):**
- In `main.py` die beiden Funktionen via Eel bereitstellen.
- Sicherstellen, dass der `/direct/`-Route auch für Hover-Previews funktioniert.

**Frontend (HTML/JS/CSS):**
- "Videos"-Sub-Tab in der Bibliothek ergänzen.
- Container `lib-view-video-grid` für Video-Karten anlegen.
- Video-Grid mit CSS Flexbox/Grid umsetzen.
- JS-Listener für `mouseenter`/`mouseleave` auf Video-Karten implementieren (Hover-to-Play).
- Dynamisch ein <video>-Element für die Vorschau einfügen/entfernen.
- Beim timeupdate/pause im Player via eel.update_playback_position speichern (throttled).
- Beim Starten eines Videos gespeicherte Position abfragen und dorthin springen.

### Verifikationsplan

**Automatisierte Tests:**
- `tests/unit/core/test_persistence.py` zur Überprüfung der DB-Positionsspeicherung.

**Manuelle Verifikation:**
- Bibliothek → Videos-Tab: Hover über Video-Karte startet Vorschau.
- Video im Hauptplayer abspielen, zu 50% springen, schließen/neu laden.
- Video erneut öffnen: Startet an gespeicherter Position.
---

## Fortschritt: Video-Bibliothek mit Hover-to-Play, Video-Grid & Positions-Persistenz (26.03.2026)

### Backend
- API für update_playback_position und get_playback_position via Eel in main.py bereitgestellt.
- Datenbankspalten für Positionsspeicherung angelegt.

### Frontend
- Analyse der renderLibrary-Funktion in app.html zur Integration des Video-Tabs und der neuen Video-Grid-Ansicht.
- Planung und Ergänzung von CSS-Styles für .media-grid und Video-Card-Hover-Preview.
- switchLibrarySubTab und lib-view-grid analysiert, um die Einbindung der Video-Grid-Komponente vorzubereiten.

### Nächste Schritte
- Video-Grid-Komponente mit Hover-to-Play-Logik implementieren.
- Playback-Position beim Mouseout/Ende speichern und beim erneuten Abspielen wiederherstellen.
- UI- und Funktionstests für verschiedene Videoszenarien durchführen.
---

## Video-Bibliothek: Eigene Ansicht, Hover-to-Play & Positions-Persistenz (26.03.2026)

### Ziel
Eine dedizierte Bibliotheksansicht mit Video-Unterreiter, in dem alle Videos gelistet werden. Beim Überfahren eines Videos mit der Maus startet die Wiedergabe automatisch (Hover-to-Play). Die zuletzt gesehene Position wird gespeichert und beim erneuten Abspielen wiederhergestellt.

### Umsetzungsschritte
- **Frontend:**
  - Neuer Unterreiter "Videos" in der Bibliothek, der alle Video-Items anzeigt.
  - Hover-to-Play: Mouseover auf ein Video-Thumbnail startet die Vorschau im Player.
  - Nach Wiedergabeende oder Tab-Wechsel wird die aktuelle Position gespeichert.
  - Beim erneuten Abspielen springt der Player zur letzten Position.
- **Backend:**
  - Datenbankmigration: Spalten `playback_position` und `last_played` zur `media`-Tabelle hinzugefügt.
  - Erweiterung der Retrieval-Funktionen (`get_all_media`, `get_media_by_name`, `get_media_by_id`, `get_media_by_path`) um die neuen Felder.
- **Verifikation:**
  - UI-Tests: Hover-to-Play und Positionsspeicherung für verschiedene Videoszenarien testen.
  - Datenbank-Checks: Sicherstellen, dass Positionen korrekt gespeichert und geladen werden.

### Status
Migration und Retrieval-Logik im Backend umgesetzt. Frontend-Implementierung und UI-Tests in Arbeit.
---

## Top-Priorität: Video Player Debugging, Tab-Optimierung & File Routing (26.03.2026)

### Fokusbereiche
- **Video Player Debugging:**
  - Systematische Analyse und Behebung von Rendering- und Playback-Problemen im Video-Tab.
  - Überprüfung der Engine-Auswahl und Kontrollelemente (Seeking, PiP, etc.).
- **Tab-Optimierung:**
  - Sicherstellen, dass Tab-Wechsel (Audio/Video) für alle Medienkategorien korrekt funktionieren.
  - Visuelles Feedback und Persistenz der aktiven Tabs verbessern.
- **File Routing:**
  - Testen und Validieren der Routing-Logik für verschiedene Endpunkte (/direct/, /media-raw/, /video-stream/).
  - Fehlerquellen bei Pfadauflösung und Backend-Kommunikation identifizieren und beheben.
- **Systematisches Testen verschiedener Item-Kategorien:**
  - Für jede Medienkategorie (Film, Serie, ISO/Image, Musikvideo, Audio, etc.) gezielte Testszenarien anlegen.
  - Sicherstellen, dass Routing, Tab-Switching und Playback für alle Typen robust funktionieren.

### Vorgehen
- Schrittweise Debugging- und Testzyklen für jede Kategorie durchführen.
- Ergebnisse und gefundene Bugs direkt im Logbuch und in den Test-Suites dokumentieren.
- Enges Zusammenspiel zwischen UI-Optimierung und Backend-Logik sicherstellen.
---

## Fixes: White/Empty Video Player Tab & Routing (26.03.2026)

- **DOM Structure Fix:** Überzählige schließende Tags entfernt, sodass der Video Player Container nicht mehr zu früh geschlossen wird. Der Tab rendert jetzt wieder korrekt.
- **Chrome Native als Default:** "Chrome Native" ist jetzt Standard-Engine beim App-Start und wird korrekt gestylt.
- **Seeking & PiP:** Slider, Control-Buttons (Stop, Shuffle, Repeat, Speed, EQ) und der Picture-in-Picture-Button sind vorhanden und mit dem Orchestrator verknüpft.
- **Routing Fix:** Klick auf ein Video-Item im Audio Player löst jetzt korrekt den Sprung zum Video Player Tab aus.

Alle Details sind im walkthrough.md dokumentiert.
---

# Walkthrough: Video Player UI Cleanup and Test Suite Reorganization (26.03.2026)

## Video Player UI Cleanup

Der Video Player bietet jetzt ein aufgeräumtes, vollflächiges Layout ohne die vorherigen horizontalen Split-Elemente.

**Änderungen in web/app.html:**
- DOM-Struktur korrigiert: Überzählige schließende Tags entfernt, wodurch der Video-Tab wieder korrekt angezeigt wird.
- Default Engine: "Chrome Native" als Standard-Engine beim App-Start gesetzt.
- vlc-info Panel entfernt: Log-Feed und Status-Badge für VLC aus der Player-Ansicht entfernt.
- active-engine-status-strip entfernt: Die dunkle Statusleiste über den Controls entfällt, maximale Video-Fläche.
- vlc-extern-fallback-bar entfernt: Sekundäre Fallback-Controls am unteren Rand entfernt.

## Test Suite Reorganization

Nicht-Produktivskripte und Test-Artefakte wurden aus src/core und dem Root-Verzeichnis in eine strukturierte tests/-Hierarchie verschoben.

**Neue Struktur:**
- tests/scr/: Utilities, Maintenance- und Hilfsskripte
- tests/unit/core/: Unit-Tests für Core-Logik

**Verschobene Dateien:**
| Ursprünglich                | Neu                                 | Beschreibung                       |
|----------------------------|-------------------------------------|-------------------------------------|
| src/core/test_media_factory.py | tests/unit/core/test_media_factory.py | Core-Media-Generierungstest         |
| src/core/curate_logbuch*.py    | tests/scr/                            | Logbuch-Kurationstools              |
| src/core/fix_logbuch_numbers*.py| tests/scr/                            | Logbuch-Nummerierungsfixes          |
| src/core/reorganize_logbuch.py  | tests/scr/                            | Logbuch-Struktur-Tool               |
| src/core/foundational_restoration.py | tests/scr/                        | Projekt-Restaurierungsskript         |
| src/core/final_history_fix.py   | tests/scr/                            | History-Repair-Tool                 |
| inspect_db.py (Root)            | tests/scr/inspect_db.py               | DB-Inspektionsutility                |
| scripts/gui_validator.py        | tests/scr/gui_validator.py            | UI-Structural-Validator              |

**Technische Anpassungen:**
- PROJECT_ROOT in tests/scr/inspect_db.py angepasst, damit Importe aus src.core weiterhin funktionieren.

## Verifikation

- UI-Stabilität: Video-Tab rendert mit dem neuen, vereinfachten Layout korrekt.
- File-Integrity: Alle verschobenen Dateien sind am neuen Ort vorhanden, src/core ist jetzt aufgeräumt und enthält nur noch essentielle Logik.
# Walkthrough: Video Player Scaling & Layout Optimization

**Datum:** 25. März 2026

## Key Accomplishments

### 1. Video Player Scaling Fix
- **Removed CSS Constraints:**
  - Eliminated flex-box and aspect-ratio constraints that caused the video container to collapse to 88px.
- **Fluid Playback:**
  - Configured Video.js to use `fluid: true` and a 16:9 aspect ratio, allowing it to automatically expand to the available width and height while maintaining correct proportions.
- **Visibility Enforcement:**
  - Added explicit visibility and display checks during Video.js initialization to prevent the "black screen" issue.

### 2. Full-Width Video Experience
- **Sidebar Toggle:**
  - Enabled the playlist sidebar to be toggleable.
- **Default 100% Width:**
  - Set the default width of the playlist sidebar in the 'Video' tab to 0, providing a full-width experience out of the box while keeping the sidebar accessible.

### 3. Playlist Synchronization & Bug Fixes
- **Duplicate ID Resolved:**
  - Renamed duplicate `player-queue-pane` IDs to `video-queue-pane` to prevent DOM selection conflicts.
- **Dual-Playlist Support:**
  - Implemented `updateSidebarPlaylists()` to synchronize all playlist views (sidebars and main tab) across different tabs.
- **Playlist Logic Repair:**
  - Fixed JavaScript logic for `loadLibrary`, `renderPlaylist`, and playlist management functions (reorder, remove) to ensure consistent UI state.

## Verification Results

### Layout Verification
- The video player now correctly fills its container and respects the 16:9 aspect ratio without being squashed.

### Sidebar Functionality
- The playlist sidebar in the 'Video' tab and 'Player' tab stays in sync with the active queue when items are added, removed, or reordered.

### Video Scaling Fix
- The video player now scales correctly to fill the available space.

### Playlist Synchronization
- The playlist sidebar is correctly populated and synchronized.

### MP4 Routing Fix
- **Robust Video Detection (`web/app.html`):**
  - The `play()` function now correctly identifies video files even if the `item.extension` property is missing, by inspecting the filename or URL path.
- **Path Resolution Fallback (`web/app.html`):**
  - The `playVideo()` function now falls back to the provided media path if the `item.relpath` or `item.path` properties are undefined. This ensures that the backend analysis (`eel.analyze_media`) always receives a valid path to process.
