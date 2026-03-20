# Data Transformation Flow

This document describes the journey of a media item's data through the system, from raw file extraction to the final JSON response sent to the frontend.

---

## 1. Raw Extraction (Parser Layer)
- **Input:** Raw file on disk (.mp3, .mp4, etc.).
- **Tools:** mutagen, pymediainfo, ffprobe.
- **Transformation:** Tool-specific metadata objects are converted into a standard Python dict.
- **Data Type:** dict (e.g., {'title': 'Song', 'artist': 'Artist', ...}).

## 2. Internal Normalization (Core Layer)
- **Transformation:** Multiple parser results are merged into a single "Media Object".
- **Data Type:** dict with standardized keys (e.g., name, path, category, tags).
- **Nesting:** tags and full_tags are nested dicts.
- **Data Type:** dict of dict (e.g., {'name': '...', 'tags': {'album': '...'}}).

## 3. Database Storage (Persistence Layer)
- **Transformation:** The normalized dict is flattened for SQL storage.
- **Serialization:** Nested dictionaries (tags, full_tags) are converted to JSON strings using json.dumps().
- **SQL Execution:** INSERT INTO media (...) VALUES (?, ?, ...).
- **Data Type:** SQL Row (Text, Integer, JSON-string).

## 4. Collection Retrieval (API Layer)
- **Transformation:** SELECT * FROM media fetches rows.
- **Deserialization:** JSON strings are converted back into Python dicts using json.loads().
- **Aggregation:** Multiple items are gathered into a list.
- **Data Type:** list of dicts (e.g., [{'name': 'A'}, {'name': 'B'}, ...]).

## 5. WebSocket Transmission (Transport Layer)
- **Transformation:** Eel (and underlying gevent-websocket) serializes the response to a JSON string.
- **Encoding:** The JSON string is encoded to UTF-8 bytes for transmission over the WebSocket.
- **Data Type:** JSON String (serialized Python dict).

## 6. Frontend Consumption (UI Layer)
- **Transformation:** The browser receives valid UTF-8 bytes, decodes them to a string, and parses the JSON.
- **Data Type:** Javascript Object (automatically mapped from JSON).

---

**Hinweis:**
Jede Schicht ist für eine klar definierte Transformation und Serialisierung/Deserialisierung verantwortlich. Fehlerquellen lassen sich so gezielt eingrenzen (z.B. JSON-Fehler, SQL-Serialisierung, Parser-Output).
