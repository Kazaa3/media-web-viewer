<!-- Category: Database -->
<!-- Title_DE: Daten-Persistenz: Von JSON zu SQLite EAV -->
<!-- Title_EN: Data Persistence: From JSON to SQLite EAV -->
<!-- Summary_DE: Evolution der Speicherstrategie für Medien-Metadaten. -->
<!-- Summary_EN: Evolution of the storage strategy for media metadata. -->
<!-- Status: COMPLETED -->

# Daten-Persistenz: Von JSON zu SQLite EAV

Die Verwaltung tausender Mediendateien erfordert eine performante und flexible Speicherlösung. Der *Media Web Viewer* hat hier eine signifikante Evolution durchlaufen.

### Die Anfänge: JSON-Blobs
Ursprünglich wurden Metadaten (Tags) als flache JSON-Objekte direkt in einer Textspalte der Datenbank gespeichert. Dies war einfach zu implementieren, erschwerte jedoch komplexe Abfragen (z.B. "Zeige alle Titel mit dem Genre 'Jazz'").

### Der neue SQL-Ansatz (v1.3.4+)
Mit Version 1.3.4 wurde ein relationaleres **EAV-Modell (Entity-Attribute-Value)** eingeführt:
- **`media` Tabelle:** Speichert Kerninformationen (Pfad, Basisname, Zeitstempel).
- **`tags` Tabelle:** Speichert jedes Metadatum als separaten Key-Value-Eintrag (`media_id`, `key`, `value`).

### Vorteile
1. **Performance:** Datenbank-Indizes wirken nun auf einzelne Tags, was die Suche und Filterung massiv beschleunigt.
2. **Extensibilität:** Neue Tag-Typen können hinzugefügt werden, ohne das Datenbankschema ändern zu müssen.
3. **Migration:** Ein integriertes Migrationssystem sorgt dafür, dass alte JSON-Daten beim ersten Start automatisch in das neue Tabellenformat überführt werden.

Dieser Wechsel stellt sicher, dass die Anwendung auch bei sehr großen Mediensammlungen (50.000+ Items) flüssig bleibt.

<!-- lang-split -->

# Data Persistence: From JSON to SQLite EAV

Managing thousands of media files requires a high-performance and flexible storage solution. The *Media Web Viewer* has undergone a significant evolution here.

### The Beginnings: JSON Blobs
Originally, metadata (tags) were stored as flat JSON objects directly in a text column of the database. This was easy to implement but made complex queries difficult (e.g., "Show all tracks with the genre 'Jazz'").

### The New SQL Approach (v1.3.4+)
With version 1.3.4, a more relational **EAV model (Entity-Attribute-Value)** was introduced:
- **`media` table:** Stores core information (path, basename, timestamps).
- **`tags` table:** Stores each metadata item as a separate key-value entry (`media_id`, `key`, `value`).

### Advantages
1. **Performance:** Database indices now act on individual tags, which massively speeds up searching and filtering.
2. **Extensibility:** New tag types can be added without having to change the database schema.
3. **Migration:** An integrated migration system ensures that old JSON data is automatically transferred to the new table format upon first start.

This switch ensures that the application remains fluid even with very large media collections (50,000+ items).
