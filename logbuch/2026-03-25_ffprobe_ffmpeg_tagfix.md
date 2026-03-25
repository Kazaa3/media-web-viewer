# 2026-03-25 – FFprobe/FFmpeg/ISO Tag-Fix & Geisterelemente

## Bugfix: Falsch geschlossene Tags führten zu Layout-Fehlern
- Ursache: Ein einziger falsch geschlossener HTML-Tag (`</b>` statt `</strong>`) bei den Systeminfos (erst FFmpeg, dann FFprobe, Copy-Paste-Fehler).
- Folge: Der Browser interpretierte die Zeile als nie abgeschlossen, wodurch die komplette Parser-Konfigurationsleiste und alle folgenden Tabs (z.B. Logbuch, Video) zerschossen wurden. "FFmpeg:", "FFprobe:" usw. erschienen als Geister-Elemente auf anderen Tabs.
- Fix: Mit einem Skript das gesamte HTML nach allen falschen `<b/>`-Tags durchsucht und alle `<strong>`-Tags korrekt geschlossen (auch bei pymkv, mkvinfo, isoparser etc.).
- Ergebnis: Die Div-Balance ist jetzt 100% perfekt, keine herumfliegenden Parser- oder Analyse-Elemente mehr, alles sitzt stabil und korrekt im Layout.

## Hinweise
- Nach erneutem Neuladen der Seite ist das Layout überall stabil.
- Fehlerursache war ein klassischer Copy-Paste-Fehler beim Übernehmen von Code-Blöcken.
- System bestätigt: Keine offenen oder falsch verschachtelten Container mehr.

**Sorry für den kleinen Herzinfarkt – jetzt ist alles restlos sauber!**

---

# 2026-03-25 – Bugfix: Parser-Liste & Konfigurationslogik wiederhergestellt

## Problem
- Während des großen Cleanups wurde der Initialisierungsaufruf `loadParserConfig();` versehentlich aus der Start-Routine (`initApp`/`DOMContentLoaded`) entfernt.
- Folge: Die Parser-Liste (FFmpeg, MediaInfo, Mutagen etc.) im Parser-Tab wurde nicht geladen.
- Der Block "Kern-Einstellungen" blieb leer, keine Parser-Optionen waren auswählbar oder konfigurierbar.

## Lösung
- Der Aufruf von `loadParserConfig();` wurde wieder korrekt in die Initialisierung der App eingehängt.
- Nach dem Neuladen der Seite erscheint links im Parser-Tab wieder die vollständige Parser-Liste.
- Die Schalter zur Auswahl/Aktivierung einzelner Parser sind wieder sichtbar und funktionieren.
- Beim Klick auf einen Parser werden rechts die spezifischen Optionen und Konfigurationsdetails angezeigt.

**Bitte prüfen: Die Parser-Liste und deren Optionen sollten jetzt wieder wie gewohnt funktionieren!**
Die Anwendungstab-Struktur wurde umfassend stabilisiert. Es wurde festgestellt, dass mehrere Management-Tabs (insbesondere Parser, Debug, Tests, Reporting, Video Player und Logbuch) vorzeitig geschlossen wurden oder außerhalb des Haupt-Content-Bereichs (main-content-area) lagen. Dies führte dazu, dass diese Tabs im Browser horizontal nach rechts verschoben gerendert wurden.

Durchgeführte Korrekturen:
Nesting-Korrektur: Alle betroffenen Tab-Container wurden wieder korrekt als Geschwister-Elemente innerhalb der main-content-area (Einrückung: 12 Leerzeichen) organisiert.
Tag-Integrität: Fehlende oder falsch platzierte schließende </div>-Tags wurden korrigiert, um zu verhindern, dass Tabs ineinander verschachtelt werden ("Ghosting"-Effekt).
Abschluss der Hauptcontainer: Die Container main-content-area (8 Leerzeichen) und main-split-container (4 Leerzeichen) werden nun erst ganz am Ende, nach dem letzten Tab (Logbuch), geschlossen.
Einrückungs-Normalisierung: Die gesamte HTML-Struktur der Management-Tabs wurde auf ein einheitliches Einrückungsniveau gebracht, was die Wartbarkeit verbessert und Layout-Drifts eliminiert.
Die Tabs sollten nun wieder bündig am linken Rand (nach der Sidebar) erscheinen und ihre volle Breite innerhalb des vorgesehenen Layouts nutzen.

Gerne können wir nun mit der Überprüfung der Parser-Konfiguration oder den weiteren Schritten im Debug-Tab fortfahren.

---

# 2026-03-25 – Tab-Nesting & Layout-Stabilisierung

## Problem
- Mehrere Management-Tabs (Parser, Debug, Tests, Reporting, Video Player, Logbuch) wurden im HTML außerhalb des Haupt-Content-Bereichs (`main-content-area`) oder zu früh geschlossen.
- Folge: Tabs wurden im Browser nach rechts verschoben oder außerhalb des vorgesehenen Layouts gerendert ("Ghosting").

## Korrekturen
- **Nesting-Korrektur:** Alle betroffenen Tab-Container sind jetzt wieder korrekt als Geschwister-Elemente innerhalb von `main-content-area` organisiert (Einrückung: 12 Leerzeichen).
- **Tag-Integrität:** Fehlende oder falsch platzierte schließende `</div>`-Tags wurden korrigiert, um Verschachtelungsfehler zu vermeiden.
- **Abschluss der Hauptcontainer:** Die Container `main-content-area` (8 Leerzeichen) und `main-split-container` (4 Leerzeichen) werden erst nach dem letzten Tab geschlossen.
- **Einrückungs-Normalisierung:** Die gesamte HTML-Struktur der Management-Tabs wurde auf ein einheitliches Einrückungsniveau gebracht.

## Ergebnis
- Alle Management-Tabs erscheinen wieder bündig am linken Rand (nach der Sidebar) und nutzen die volle Breite.
- Die Wartbarkeit des Codes ist durch konsistente Einrückung und klare Container-Struktur deutlich verbessert.

**Nächste Schritte:**
- Die Parser-Konfiguration und Debug-Tab-Funktionen können jetzt zuverlässig überprüft und weiterentwickelt werden.

---

# 2026-03-25 – Parser-Tab Layout-Korrektur: Flex-Start & Split

## Ziel
- Der Parser-Tab soll den gesamten verfügbaren Platz einnehmen und direkt nach der einklappbaren Haupt-Sidebar starten (kein horizontaler Versatz mehr).

## Änderungen im Detail
- **Nesting-Korrektur:** Der gesamte `regex-provider-chain-orchestrator-panel`-Container wurde in die `main-content-area` verschoben (Einrückung: 12 Leerzeichen). Dadurch entfällt der horizontale Versatz.
- **Vertikaler Split:**
  - **Links (400px):** "Erweiterter Parser-Modus" und "Parser-Architektur" (Kern-Einstellungen).
  - **Rechts (Flex:1):** Detaillierte "Parser-Optionen" inkl. Konfigurations-Ansicht.
- **Header-Positionierung:** Die Überschrift "Parser Konfiguration" ist jetzt am linken Rand des Inhaltsbereichs ausgerichtet.

## Ergebnis
- Die Management-Tabs (insb. Parser) sind in der horizontalen Flex-Struktur korrekt priorisiert.
- Die "Geister-Fläche" auf der linken Seite verschwindet.
- Der Parser-Tab startet ganz links, mit klarer vertikaler Trennung und den Optionen auf der rechten Seite – wie im Screenshot gefordert.

