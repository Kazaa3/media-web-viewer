<!-- Category: Documentation -->
<!-- Title_DE: Datenbank & Persistenz (SQLite) -->
<!-- Title_EN: Database & Persistence (SQLite) -->
<!-- Summary_DE: Die Persistenzschicht von "dict": SQLite-Schema, Datenbank-Isolation pro Umgebung und Bibliotheksverwaltung. -->
<!-- Summary_EN: The persistence layer of "dict": SQLite schema, database isolation per environment and library management. -->
<!-- Status: ACTIVE -->

# Datenbank & Persistenz (SQLite)

## Warum SQLite?
Für eine Desktop-Anwendung wie **dict** ist SQLite die ideale Wahl. Es ist dateibasiert, benötigt keinen separaten Serverprozess und bietet dennoch volle SQL-Power für komplexe Filterungen der Medienbibliothek.

## Die Architektur der Bibliothek
Die Datenbank (`library.db`) speichert nicht nur Pfade, sondern ein reichhaltiges Set an Metadaten:
- **MediaItems:** Die zentrale Tabelle für Audio- und Video-Files.
- **Kategorisierung:** Logik zur Unterscheidung zwischen Musik, Hörbüchern, Filmen und Serien.
- **Transcoding-Status:** Information darüber, ob ein Item bereits im Cache vorliegt.

### Schema-Flexibilität
Obwohl SQLite ein festes Schema erzwingt, nutzen wir für "exotische" Metadaten oft JSON-Blobs innerhalb von Textfeldern. Dies harmoniert perfekt mit unserer **Namensphilosophie (dict)** und erlaubt es, beliebig viele Zusatzinfos (z. B. aus Scrapern) zu speichern, ohne ständig das Schema migrieren zu müssen.

## Umgebung-Isolation & Sicherheit
Ein wichtiger Meilenstein war die **Isolation der Datenbanken**:
- **Produktion:** Nutzt die Standard-DB im Nutzerverzeichnis.
- **Testing:** Jede Testumgebung (`testbed`, `selenium`) erhält eine eigene, temporäre Datenbank. Dies verhindert, dass Testdaten die echte Bibliothek korrumpieren.
- **Cleanup:** Automatisierte Routinen bereinigen verwaiste Einträge, wenn Dateien auf der Festplatte gelöscht oder verschoben wurden.

## Performance-Optimierung
Durch gezielte Indizierung auf Pfaden und Metadaten-Feldern (Artist, Album) erreicht dict auch bei Bibliotheken mit zehntausenden Einträgen blitzschnelle Suchzeiten. Die Kombination aus In-Memory Caching (via Python Dictionaries) und permanenter SQLite-Speicherung bietet das Beste aus beiden Welten.

*Die Datenbank ist das Gedächtnis von dict – robust, isoliert und jederzeit bereit für komplexe Abfragen.*

<!-- lang-split -->

# Database & Persistence (SQLite)

## Why SQLite?
For a desktop application like **dict**, SQLite is the ideal choice. It is file-based, requires no separate server process, and still offers full SQL power for complex filtering of the media library.

## The Architecture of the Library
The database (`library.db`) stores not only paths, but a rich set of metadata:
- **MediaItems:** The central table for audio and video files.
- **Categorization:** Logic for distinguishing between music, audiobooks, movies, and series.
- **Transcoding Status:** Information about whether an item is already in the cache.

### Schema Flexibility
Although SQLite enforces a fixed schema, we often use JSON blobs within text fields for "exotic" metadata. This harmonizes perfectly with our **naming philosophy (dict)** and allow us to store any number of additional info (e.g., from scrapers) without having to constantly migrate the schema.

## Environment Isolation & Security
An important milestone was the **isolation of the databases**:
- **Production:** Uses the standard DB in the user directory.
- **Testing:** Each test environment (`testbed`, `selenium`) receives its own temporary database. This prevents test data from corrupting the real library.
- **Cleanup:** Automated routines clean up orphaned entries when files have been deleted or moved on the hard drive.

## Performance Optimization
Through targeted indexing on paths and metadata fields (Artist, Album), dict achieves lightning-fast search times even with libraries with tens of thousands of entries. The combination of in-memory caching (via Python dictionaries) and permanent SQLite storage offers the best of both worlds.

*The database is the memory of dict – robust, isolated and ready for complex queries at any time.*
