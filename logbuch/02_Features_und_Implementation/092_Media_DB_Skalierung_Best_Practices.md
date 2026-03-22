# Große Datenbank für Media-Library (1 Mio.+ Dateien)

## SQLite – Optimiertes Schema
- PRAGMA journal_mode=WAL für parallele Writes
- Indizes auf Pfad, Typ, Cover, Tags
- JSON-Feld für Metadaten (mutagen/MusicBrainz)
- Viele-zu-viele Tags mit media_tags
- Bulk-Insert mit executemany

### Beispiel (schema.sql)
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 1000000;
PRAGMA page_size = 4096;
PRAGMA temp_store = MEMORY;
PRAGMA analysis_limit = 400;

CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    full_path TEXT UNIQUE,
    file_type TEXT,
    duration REAL,
    size INTEGER,
    cover_thumb TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE media ADD COLUMN metadata JSON;
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);
CREATE TABLE media_tags (
    media_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY(media_id) REFERENCES media(id),
    PRIMARY KEY(media_id, tag_id)
);
CREATE INDEX idx_path ON media(full_path);
CREATE INDEX idx_type ON media(file_type);
CREATE INDEX idx_tags ON media_tags(media_id);
CREATE INDEX idx_cover ON media(cover_thumb);
```

### Python Setup
```python
import sqlite3

def connect_db(db_path='media_library.db'):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA cache_size=1000000')
    return conn

def bulk_insert_media(items):
    conn = connect_db()
    cur = conn.cursor()
    cur.executemany("INSERT OR REPLACE INTO media (filename, full_path, ...) VALUES(?, ?, ...)", items)
    conn.commit()
    conn.close()
```

## Postgres – Skalierbarer
- Für komplexe Queries/Concurrency
- SQLAlchemy für ORM
- Docker für schnellen Start

### Beispiel
```python
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    full_path = Column(String, unique=True)
    metadata = Column(JSON)
    cover_thumb = Column(String)
    __table_args__ = (Index('idx_path', 'full_path'),)

engine = create_engine('postgresql://user:pass@localhost/medialib')
Base.metadata.create_all(engine)
```

## Multiprocessing + DB
- WAL-Modus in SQLite erlaubt parallele Inserts
- Pool mit safe_insert

### Beispiel
```python
def safe_insert(args):
    path, metadata, thumb = args
    conn = connect_db()
    try:
        conn.execute("INSERT INTO media (full_path, metadata, cover_thumb) VALUES (?, ?, ?)",
                     (path, json.dumps(metadata), thumb))
        conn.commit()
    finally:
        conn.close()

with mp.Pool(8) as pool:
    pool.map(safe_insert, file_args)
```

## Vergleich
| DB      | Größe (1M Files) | Speed         | Setup         |
|---------|------------------|--------------|--------------|
| SQLite  | 5-20GB           | 100k Inserts/h| Lokal, einfach|
| Postgres| Unbegrenzt       | 500k+/h      | Docker/Server |
| DuckDB  | Kolumnar, Analytics| Super Queries| pip install duckdb|

## Best Practices
- Start mit SQLite (MX Linux, lokal)
- PRAGMAs für Performance
- Indizes für schnelle Queries
- Bulk-Insert, Multiprocessing
- Migration zu Postgres bei Bedarf

---
*Letzte Aktualisierung: 10. März 2026*
