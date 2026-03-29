---

# Logbuch-Eintrag: ISBN-Scan & Media Object Refactoring

## Ziel

Refaktorierung der Mediathek zur klaren Unterscheidung zwischen einzelnen Dateien (Items) und Sammlungen (Objects/Container) sowie Integration eines automatisierten ISBN-Scans für Metadaten.

---

## 1. Core Models & Datenbank


### models.py
**Trennung zwischen Item und Objekt:**
- **Item:**
  - Repräsentiert eine einzelne Datei (Python Path-Objekt)
  - Felder: `id`, `parent_id` (Verweis auf Objekt), `file_type`, `media_type="file"`, Pfad, technische Attribute
- **Objekt (Container):**
  - Repräsentiert eine Sammlung/Gruppe (z.B. Album, Film, Serie, Box)
  - Felder: `id`, `media_type="container"`, `subtype` (z.B. album, serie, film, box)
  - Metadaten: `isbns` (Liste, optional), `imdb` (optional, für Filme/Serien), `tmdb` (optional), `discogs` (optional, meist für CDs/Alben), `amazon_cover` (optional)
  - **Nicht alle Objekte haben alle Felder!**

### db.py
- Zwei Tabellen oder ein flexibles Schema:
  - Items: Einzeldateien, verweisen auf Objekt über `parent_id`
  - Objekte: Container mit Metadaten
- Felder für Objekte: `isbns`, `imdb`, `tmdb`, `discogs`, `amazon_cover`, `subtype`, `media_type`
- Felder für Items: `file_type`, `media_type`, Pfad, technische Attribute
- Anpassung von `insert_media` und `get_all_media` für die neue Trennung und optionale Felder

---

## 2. Logik & Scanning

- **main.py**
  - Gruppierungslogik: `scan_media` gruppiert Items zu Objekten (z.B. Alben, Serien, Boxen)
  - ISBN-Scan-API: `api_scan_isbn(isbn)` implementiert
  - Hilfsfunktionen: `normalize_isbn`, Metadaten-Fetch (Platzhalter für externe APIs)
  - DVD/Blu-Ray-Erkennung nutzt Subtypes und Remote-IDs (z.B. imdb, tmdb, isbns)
- **format_utils.py**
  - Erweiterung von `detect_file_format` und Extension-Mappings für neue Kategorien (Single, Klassik, Soundtrack, ...)

---

## 3. Frontend UI

- **app.html**
  - "Scan ISBN"-Button ergänzt
  - JS-Logik: Aufruf von `api_scan_isbn`, Anzeige der Ergebnisse
  - Media Cards zeigen neue Badges und Remote-ID-Links

---

## 4. Verification Plan

- **Automatisierte Tests**
  - Bestehende Tests laufen lassen (Playback, Scanning)
  - Neuer Test: `tests/test_isbn_logic.py` für ISBN-Normalisierung und Metadaten-Mock
- **Manuelle Verifikation**
  - Bibliotheksscan: Prüfen, ob Alben/Filme korrekt gruppiert werden
  - "Scan ISBN"-Feature mit Test-ISBN prüfen
  - Remote-ID-Links (IMDb, etc.) in der UI testen

---

## Hinweise

- Dieses Refactoring trennt klar zwischen Items (Dateien, Python Path-Objekt) und Objekten (Container mit Metadaten wie isbns, imdb, tmdb, discogs, amazon_cover). Nicht alle Objekte haben alle Felder; discogs ist meist für CDs relevant. blu_ray_forum entfällt vorerst.
- Bestehende Einträge werden migriert und neue Metadatenfelder eingeführt.
- Review und Freigabe vor Umsetzung empfohlen!
