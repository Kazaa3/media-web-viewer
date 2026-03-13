<!-- Category: Database -->
<!-- Title_DE: 07 Persistenz: Von flüchtigen Daten zu SQLite -->
<!-- Title_EN: 07 Persistence: From Volatile Data to SQLite -->
<!-- Summary_DE: Einführung einer robusten Datenbank für Medien-Metadaten und Performance. -->
<!-- Summary_EN: Introduction of a robust database for media metadata and performance. -->
<!-- Status: COMPLETED -->

# 07 Persistenz: Von flüchtigen Daten zu SQLite

Mit steigender Anzahl der unterstützten Formate und Metadaten wurde klar: Jedes Mal beim App-Start Tausende von Dateien neu zu scannen, ist nicht praktikabel.

### Die Lösung: SQLite
Um die Ladezeiten zu minimieren, wurde **SQLite** als lokale Datenbank integriert. 
- **Caching:** Einmal gescannte Metadaten werden persistent gespeichert.
- **Speed:** Beim nächsten Start muss die App nur noch prüfen, ob sich Dateien geändert haben (`mtime`-Check).
- **Evolution:** Ursprünglich als einfacher JSON-Blob-Speicher konzipiert, entwickelte sich das Schema bis hin zum hochperformanten **EAV-Modell (Entity-Attribute-Value)** in Version 1.3.4, das blitzschnelle Filterungen über Tags erlaubt.

### Meilenstein-Bedeutung
Die Datenbank ist das Gehirn des *Media Web Viewer*. Ohne diese persistente Schicht wären Features wie globale Suche oder komplexe Sortierungen unmöglich. Sie markiert den Übergang von einem reinen Player zu einem echten **Medien-Bibliotheksverwalter**.

<!-- lang-split -->

# 07 Persistence: From Volatile Data to SQLite

As the number of supported formats and metadata increased, it became clear: rescanning thousands of files every time the app starts is not practical.

### The Solution: SQLite
To minimize loading times, **SQLite** was integrated as a local database. 
- **Caching:** Once scanned, metadata is stored persistently.
- **Speed:** On the next start, the app only needs to check if files have changed (`mtime` check).
- **Evolution:** Originally designed as a simple JSON blob store, the schema evolved into the high-performance **EAV model (Entity-Attribute-Value)** in version 1.3.4, allowing lightning-fast filtering across tags.

### Milestone Meaning
The database is the brain of the *Media Web Viewer*. Without this persistent layer, features like global search or complex sorting would be impossible. It marks the transition from a simple player to a true **media library manager**.
