<!-- Category: Planning -->
<!-- Title_DE: Meilenstein 2 – Medienbibliothek (Branch: milestone/2-medienbibliothek) -->
<!-- Title_EN: Milestone 2 – Media Library (Branch: milestone/2-medienbibliothek) -->
<!-- Summary_DE: Einführung einer dedizierten Tags-Tabelle in SQLite und Aufbau der vollständigen Medienbibliothek-Infrastruktur. -->
<!-- Summary_EN: Introduction of a dedicated tags table in SQLite and build-out of the full media library infrastructure. -->
<!-- Status: ACTIVE -->

# Meilenstein 2 – Medienbibliothek

**Version:** 1.3.4  
**Datum:** 9. März 2026  
**Status:** 🟡 ACTIVE  
**Branch:** `milestone/2-medienbibliothek`

## Kontext: Meilenstein-Übersicht

Das Projekt ist in drei klar getrennte Entwicklungsmeilensteine aufgeteilt, die jeweils in einem eigenen Branch entwickelt werden:

| Meilenstein | Name              | Branch                          | Status       |
|-------------|-------------------|---------------------------------|--------------|
| M1          | AudioPlayer       | `main`                          | ✅ Released  |
| M2          | Medienbibliothek  | `milestone/2-medienbibliothek`  | 🟡 Aktiv     |
| M3          | Neue GUI          | `milestone/3-neue-gui`          | 📋 Geplant   |

---

## Meilenstein 1 – AudioPlayer (`main`)

Der erste Meilenstein umfasst den funktionalen Audio- und Videoplayer mit:
- Vollständiger Metadaten-Unterstützung (Mutagen, pymediainfo, FFmpeg)
- HTML5-Playeroberfläche (Glassmorphism-Design)
- Mutiplattform-Builds (Debian `.deb`, Windows `.exe`)
- CI/CD-Pipeline (GitHub Actions)
- Versions- und Release-Automatisierung

**Aktueller Stand:** In `main` gemergt, als `v1.3.3` getaggt und veröffentlicht.

---

## Meilenstein 2 – Medienbibliothek (`milestone/2-medienbibliothek`)

Ziel dieses Meilensteins ist der Aufbau einer robusten, abfragbaren Medienbibliothek auf Basis einer
vollständig relationalen Datenbank. Die bisherige Speicherung von Tags als JSON-Blob im Feld
`media.tags` wird durch eine dedizierte relationale Tabelle ersetzt.

### Kernänderungen in v1.3.4

#### 1. Dedizierte `tags`-Tabelle (EAV-Schema)

```sql
CREATE TABLE tags (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id  INTEGER NOT NULL,
    key       TEXT    NOT NULL,
    value     TEXT,
    FOREIGN KEY(media_id) REFERENCES media(id) ON DELETE CASCADE,
    UNIQUE(media_id, key)
);
CREATE INDEX idx_tags_media_id ON tags(media_id);
CREATE INDEX idx_tags_key      ON tags(key);
```

**Vorteile gegenüber JSON-Blob:**
- Einzelne Tags effizient abfragbar (`WHERE key = 'artist'`)
- Indizes auf `media_id` und `key` → schnelle Suche
- Kaskadierendes Löschen bei Medienentfernung
- Vollständig normalisiertes Schema

#### 2. Einmalige Datenmigration

`init_db()` ruft `_migrate_json_tags_to_table()` auf – idempotent per `INSERT OR IGNORE`.
Bestehende Datenbanken werden beim nächsten Start automatisch migriert; es ist kein manueller Eingriff nötig.

#### 3. Neue öffentliche API (`db.py`)

| Funktion | Beschreibung |
|---|---|
| `get_media_tags(name)` | Tags eines einzelnen Medien-Items per Name abrufen |
| `get_tags_by_key(key)` | Alle Medien-Items mit einem bestimmten Tag-Schlüssel abfragen |

```python
# Alle Titel eines bestimmten Künstlers finden
results = db.get_tags_by_key("artist")
# [{"name": "song.mp3", "value": "Portishead"}, ...]
```

#### 4. Abwärtskompatibilität

Das JSON-Blob in `media.tags` bleibt erhalten und wird bei jeder Tag-Änderung synchron gehalten.
Bestehende Integrations-Tests und externe Clients bleiben ohne Anpassung lauffähig.

---

### Geplante weitere Aufgaben (M2 Backlog)

- [ ] Volltext-Suche über Tags (SQLite FTS5-Extension oder LIKE-Abfragen)
- [ ] Tag-Filter in der Frontend-Bibliotheksansicht
- [ ] Playlist-Tags und Beschreibungsfelder
- [ ] Bulk-Tag-Bearbeitung (mehrere Dateien gleichzeitig)
- [ ] Export der Bibliothek als JSON/CSV

---

## Meilenstein 3 – Neue GUI (`milestone/3-neue-gui`) *(geplant)*

Der dritte Meilenstein wird die Benutzeroberfläche auf ein moderneres Frontend-Framework migrieren.
Konkrete Technologie und Umfang werden zu Beginn des Meilensteins festgelegt.

**Hinweis:** M3 startet erst, wenn M2 abgeschlossen und in `main` gemergt ist.

---

## Branch-Strategie

```
main (M1 – AudioPlayer, released)
└── milestone/2-medienbibliothek  ← diese Arbeit
    └── milestone/3-neue-gui      ← geplant, baut auf M2 auf
```

- Jeder Meilenstein lebt in einem eigenen Branch.
- Feature-Branches werden von dem jeweiligen Meilenstein-Branch abgezweigt und nach Abschluss in diesen gemergt.
- Nach Fertigstellung wird der Meilenstein-Branch in `main` gemergt und mit einem Versions-Tag versehen.

---

## Verwandte Einträge

- [01_Features.md](01_Features.md) – Geplante Features
- [53_Version_Synchronization_System.md](53_Version_Synchronization_System.md) – Versions-Sync-System
- [55_Release_Pipeline_Integration.md](55_Release_Pipeline_Integration.md) – Release-Pipeline

<!-- lang-split -->

# Milestone 2 – Media Library

**Version:** 1.3.4  
**Date:** March 9, 2026  
**Status:** 🟡 ACTIVE  
**Branch:** `milestone/2-medienbibliothek`

## Context: Milestone Overview

The project is divided into three clearly separated development milestones, each developed in its own branch:

| Milestone | Name              | Branch                          | Status       |
|-----------|-------------------|---------------------------------|--------------|
| M1        | AudioPlayer       | `main`                          | ✅ Released  |
| M2        | Media Library     | `milestone/2-medienbibliothek`  | 🟡 Active    |
| M3        | New GUI           | `milestone/3-neue-gui`          | 📋 Planned   |

---

## Milestone 1 – AudioPlayer (`main`)

The first milestone encompasses the functional audio and video player with:
- Full metadata support (Mutagen, pymediainfo, FFmpeg)
- HTML5 player interface (Glassmorphism design)
- Multi-platform builds (Debian `.deb`, Windows `.exe`)
- CI/CD pipeline (GitHub Actions)
- Version and release automation

**Current state:** Merged into `main`, tagged and published as `v1.3.3`.

---

## Milestone 2 – Media Library (`milestone/2-medienbibliothek`)

The goal of this milestone is to build a robust, queryable media library backed by a fully relational
database. The previous storage of tags as a JSON blob in `media.tags` is replaced by a dedicated
relational table.

### Core changes in v1.3.4

#### 1. Dedicated `tags` table (EAV schema)

```sql
CREATE TABLE tags (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id  INTEGER NOT NULL,
    key       TEXT    NOT NULL,
    value     TEXT,
    FOREIGN KEY(media_id) REFERENCES media(id) ON DELETE CASCADE,
    UNIQUE(media_id, key)
);
CREATE INDEX idx_tags_media_id ON tags(media_id);
CREATE INDEX idx_tags_key      ON tags(key);
```

**Advantages over JSON blob:**
- Individual tags can be queried efficiently (`WHERE key = 'artist'`)
- Indices on `media_id` and `key` → fast lookups
- Cascading delete when media is removed
- Fully normalized schema

#### 2. One-time data migration

`init_db()` calls `_migrate_json_tags_to_table()` — idempotent via `INSERT OR IGNORE`.
Existing databases are automatically migrated on next startup; no manual intervention required.

#### 3. New public API (`db.py`)

| Function | Description |
|---|---|
| `get_media_tags(name)` | Retrieve tags for a single media item by name |
| `get_tags_by_key(key)` | Query all media items that have a specific tag key |

```python
# Find all titles by a specific artist
results = db.get_tags_by_key("artist")
# [{"name": "song.mp3", "value": "Portishead"}, ...]
```

#### 4. Backward compatibility

The JSON blob in `media.tags` is retained and kept in sync on every tag change.
Existing integration tests and external clients continue to work without modification.

---

### Planned further tasks (M2 Backlog)

- [ ] Full-text search across tags (SQLite FTS5 extension or LIKE queries)
- [ ] Tag filter in the frontend library view
- [ ] Playlist tags and description fields
- [ ] Bulk tag editing (multiple files simultaneously)
- [ ] Library export as JSON/CSV

---

## Milestone 3 – New GUI (`milestone/3-neue-gui`) *(planned)*

The third milestone will migrate the user interface to a more modern frontend framework.
The specific technology and scope will be decided at the start of the milestone.

**Note:** M3 starts only after M2 is complete and merged into `main`.

---

## Branch Strategy

```
main (M1 – AudioPlayer, released)
└── milestone/2-medienbibliothek  ← this work
    └── milestone/3-neue-gui      ← planned, builds on M2
```

- Each milestone lives in its own branch.
- Feature branches are forked from their respective milestone branch and merged back when complete.
- After completion, the milestone branch is merged into `main` and tagged with a version number.

---

## Related Entries

- [01_Features.md](01_Features.md) – Planned features
- [53_Version_Synchronization_System.md](53_Version_Synchronization_System.md) – Version sync system
- [55_Release_Pipeline_Integration.md](55_Release_Pipeline_Integration.md) – Release pipeline
