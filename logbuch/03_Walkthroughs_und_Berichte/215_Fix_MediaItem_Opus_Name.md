# Logbuch: Fix für .opus im MediaItem-Namen

**Datum:** 11. März 2026

---

## Problem
MediaItems zeigen im Namensstring die Dateiendung (.opus) an, z.B. "song.opus" statt nur "song". Ursache: Der Name wird beim Erstellen des MediaItem-Objekts direkt vom Dateinamen übernommen (Path(path).name), wodurch die Endung enthalten bleibt.

---

## Analyse
- Der Name wird im Backend (models.py, main.py, media_parser.py) als vollständiger Dateiname inklusive Endung gespeichert und weitergegeben.
- Die Endung stammt aus Path(path).name oder filename.
- Im UI und Backend wird dieser Name ohne weitere Verarbeitung angezeigt.

---

## Fix-Strategie
- Beim Anzeigen oder Speichern des Namensstrings die Endung entfernen, wenn sie nicht gewünscht ist (z.B. mit Path(name).stem).
- Alternativ: Im UI oder Backend explizit den „reinen“ Namen ohne Endung verwenden.
- Optional: Konfigurierbar machen, ob Endung angezeigt werden soll.

---

## Beispiel-Fix (Python)
```python
from pathlib import Path
name = Path(filename).stem  # Entfernt die Endung
```

---

**TODO:**
- Fix im Backend und/oder UI implementieren.
- Logbuch-Eintrag nach Umsetzung aktualisieren.
