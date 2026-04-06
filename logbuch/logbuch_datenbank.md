# Logbuch: Media-Library Datenbank – Struktur, Features & Best Practices

## Ziel
Dokumentation der Datenbankstruktur, wichtigsten Felder, Beziehungen und Best Practices für die Media-Library. Fokus: Flexibilität, Erweiterbarkeit, Hierarchien (parent_id), Typisierung und Integration mit Media-Workflows.

---

## 1. Datenbankschema – Übersicht
- **Tabelle:** `media`
- **Wichtige Felder:**
  - `id` (INTEGER, Primary Key)
  - `name`, `path`, `type`, `category`, `duration`
  - `media_type`, `subtype`, `file_type`
  - `tags`, `full_tags` (JSON)
  - `extension`, `container`, `tag_type`, `codec`
  - `has_artwork`, `art_path`
  - `isbn`, `imdb`, `tmdb`, `discogs`, `amazon_cover`
  - `parent_id` (INTEGER, Hierarchie/Verknüpfung)
  - `group_id` (optional, Gruppierung)
  - `is_mock`, `mock_stage` (Testdaten)

---

## 2. Beziehungen & Hierarchien
- **parent_id:**
  - Abbildung von Album→Track, Boxset→Disc, Image→Einzelbild, Sammlungen
  - Ermöglicht rekursive Abfragen und UI-Baumstrukturen
- **group_id:**
  - Optionale Gruppierung für komplexe Sets (z.B. Multi-Album-Boxsets)

---

## 3. Typisierung & Kategorien
- **media_type, subtype, file_type, category, type:**
  - Siehe [logbuch_parent_id.md](logbuch_parent_id.md) für vollständige Typenliste
  - Erlaubt gezielte Filter, UI-Darstellung und Workflow-Steuerung

---

## 4. Metadaten & IDs
- **tags, full_tags:**
  - Speicherung von kompakten und vollständigen Metadaten als JSON
- **Remote-IDs:**
  - ISBN, IMDB, TMDB, Discogs, Amazon – für externe Datenanreicherung

---

## 5. Besonderheiten & Best Practices
- **Flexibles Schema:**
  - Neue Felder können einfach ergänzt werden (z.B. für neue Medientypen)
- **JSON-Felder:**
  - Für komplexe, variable Metadaten
- **Fehlerbehandlung:**
  - Bei Integritätsverletzungen (z.B. Duplikate) wird None zurückgegeben
- **Mock-Unterstützung:**
  - is_mock, mock_stage für Testdaten und Debugging
- **Migration:**
  - Schema-Updates via Migrationsskripte oder beim App-Start prüfen

---

## 6. Beispiel: Insert eines Medien-Items
```python
def insert_media(item_dict):
    ...
    cursor.execute("""
        INSERT INTO media (..., parent_id, ...)
        VALUES (..., item_dict.get('parent_id'), ...)
    """)
    ...
```

---

## 7. Integration & Workflows
- **Scan/Import:**
  - Medien werden mit allen Metadaten und Hierarchien in die DB eingefügt
- **Abfragen:**
  - Filter nach Typ, Kategorie, Jahr, Genre, parent_id etc.
- **Update/Tagging:**
  - Tags und Metadaten können nachträglich aktualisiert werden
- **Löschvorgänge:**
  - Kindobjekte (parent_id) werden mitbehandelt

---

## 8. Ausblick & Erweiterungen
- **Versionierung:**
  - Historie von Änderungen an Medienobjekten
- **User/ACL:**
  - Multi-User-Support, Rechteverwaltung
- **Performance:**
  - Indizes auf häufig genutzte Felder (z.B. name, parent_id, media_type)

---

## Fazit
Die Media-Library-Datenbank ist flexibel, hierarchisch und für alle gängigen Medientypen und Workflows ausgelegt. Sie bildet das Rückgrat für Import, Verwaltung, Suche und Erweiterung der gesamten Media-App.
