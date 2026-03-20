# Data Transformation Flow: Media Item Journey

Dieses Dokument beschreibt den Weg eines Media-Items durch das System – von der Rohdatei bis zur fertigen JSON-Antwort im Frontend.

---

## 1. Raw Extraction (Parser Layer)
- **Input:** Rohdatei auf Disk (z.B. `.mp3`, `.mp4`)
- **Tools:** mutagen, pymediainfo, ffprobe
- **Transformation:** Tool-spezifische Metadatenobjekte werden in ein Standard-Python-`dict` überführt
- **Datentyp:**
  ```python
  {'title': 'Song', 'artist': 'Artist', ...}
  ```

## 2. Internal Normalization (Core Layer)
- **Transformation:** Ergebnisse mehrerer Parser werden zu einem "Media Object" zusammengeführt
- **Datentyp:**
  ```python
  {'name': '...', 'path': '...', 'category': '...', 'tags': {'album': '...'}, ...}
  ```
- **Nesting:** `tags` und `full_tags` sind verschachtelte Dicts

## 3. Database Storage (Persistence Layer)
- **Transformation:** Das normalisierte Dict wird für SQL-Storage "geflacht"
- **Serialisierung:** Verschachtelte Dicts (`tags`, `full_tags`) werden mit `json.dumps()` zu Strings
- **SQL:**
  ```sql
  INSERT INTO media (...) VALUES (?, ?, ...)
  ```
- **Datentyp:** SQL-Row (Text, Integer, JSON-String)

## 4. Collection Retrieval (API Layer)
- **Transformation:** `SELECT * FROM media` holt Rows
- **Deserialisierung:** JSON-Strings werden mit `json.loads()` zurück in Dicts gewandelt
- **Aggregation:** Mehrere Items werden zu einer Liste zusammengefasst
- **Datentyp:**
  ```python
  [{'name': 'A'}, {'name': 'B'}, ...]
  ```

## 5. WebSocket Transmission (Transport Layer)
- **Transformation:** Eel (bzw. gevent-websocket) serialisiert die Antwort zu einem JSON-String
- **Encoding:** Der JSON-String wird als UTF-8-Bytes über den WebSocket gesendet
- **Datentyp:** JSON-String (serialisiertes Python-Dict)

## 6. Frontend Consumption (UI Layer)
- **Transformation:** Der Browser empfängt UTF-8-Bytes, dekodiert sie zu String und parst das JSON
- **Datentyp:** Javascript-Objekt (automatisch aus JSON gemappt)

---

**Hinweis:**
Jede Schicht ist für eine klar definierte Transformation und Serialisierung/Deserialisierung verantwortlich. Fehlerquellen lassen sich so gezielt eingrenzen (z.B. JSON-Fehler, SQL-Serialisierung, Parser-Output).
