# Milestone 2 – Implementation Plan (2026-03-14)

## Ausgangslage
- Meilenstein 1 (v1.34) ist abgeschlossen, gereinigt und produktionsbereit.
- Die Repository-Struktur, Dokumentation und Build-Pipeline sind auf dem neuesten Stand.

## Nächste Schritte: Milestone 2 (Medienbibliothek & Tagging)

### 1. Erweiterte Metadaten-Datenbank
- Einführung eines flexiblen Tag-Systems (Genre, Besetzung, freie Tags)
- Anpassung des Datenbankschemas für relationale Tag-Zuordnung
- Migration bestehender Medieneinträge auf das neue Schema

### 2. UI-Erweiterung
- Filter- und Suchfunktionen auf Basis der neuen Metadaten
- Grid-Ansicht (Cover-Arts, Thumbnails) für eine moderne Medienbibliothek
- Erweiterung der Detailansicht um Tag- und Personeninformationen

### 3. Asset-Management
- Automatisierte Extraktion und Zuordnung von Cover-Arts/Thumbnails
- Unterstützung für verschiedene Medienformate (Audio, Video, E-Books)
- Caching-Strategie für Vorschaubilder

### 4. Multi-Sprach-Support
- Ausbau der i18n.json für weitere Sprachen
- Dynamische Umschaltung der Sprache im Frontend
- Übersetzungs-Workflows für neue UI-Elemente

### 5. Build- und Teststrategie
- Erweiterung der Test-Suite für Tagging, Suche und Grid-UI
- Sicherstellung der Rückwärtskompatibilität und Migrationspfade
- Automatisierte Validierung der neuen Features in der CI/CD-Pipeline

---

## 6. Erweiterungen für Milestone 2

### Videoplayer
- Integration eines modernen Videoplayers mit Unterstützung für verschiedene Formate (mp4, mkv, avi, etc.)
- Features: Play/Pause, Seek, Lautstärke, Vollbild, Untertitel
- Unterstützung für Playlist- und Serienwiedergabe
- Fortschrittsanzeige und Resume-Funktion

### Diagnostics Tab
- Erweiterung des Diagnostics-Tabs um detaillierte System- und Fehlerdiagnosen
- Live-Loganzeige (z.B. debug.log, error.log)
- Anzeige von aktiven Debug-Flags und deren Status
- Health-Checks für Backend, Datenbank und Medienparser
- Exportfunktion für Diagnosedaten (z.B. für Support)

### Datenbank Tab
- Übersicht über alle Medieneinträge und deren Metadaten
- Tag- und Genre-Statistiken (z.B. Anzahl pro Kategorie)
- Such- und Filterfunktionen direkt auf der Datenbank
- Möglichkeit, einzelne Einträge zu inspizieren, zu bearbeiten oder zu löschen
- Anzeige von Datenbank-Status, Größe und Integrität

### Weitere Features

#### Download der JSON-Konfiguration
- Möglichkeit, die aktuelle parser_config.json direkt aus dem UI (z.B. Diagnostics Tab) herunterzuladen
- Exportfunktion für Konfigurations-Backups und Support

#### Debug-Level dynamisch änderbar
- UI-Element (z.B. Dropdown oder Schieberegler) zur Laufzeit im Diagnostics Tab
- Änderung des Debug-Levels wirkt sofort auf Backend und Log-Ausgabe
- Persistenz: Änderungen werden in parser_config.json gespeichert

---

## Empfehlung
- Nach erfolgreichem Merge von M1 nach main: Umsetzung der oben genannten Architektur und Features in Milestone 2 beginnen.
- Optional: Finalen Deployment-Test von v1.34 durchführen, um die Build-Integrität zu bestätigen.

Letzte Aktualisierung: 14.03.2026
