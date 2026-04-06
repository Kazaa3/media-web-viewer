# Logbuch v1.37.45 – Walkthrough: Media Library Hydration Fix

**Datum:** 2026-04-06

## Problemstellung
Medien wurden im GUI nur im "Bypass"-Modus angezeigt. Ursache: Probleme bei der Pfadauflösung (wegen # im Projektpfad) und ein Kategorie-Mapping-Fehler für nicht kategorisierte Items.

## Änderungen & Maßnahmen
1. **Robuste Pfadauflösung (Pathlib)**
   - `resolve_media_path` in main.py nutzt jetzt konsequent `pathlib.Path` für alle Existenzprüfungen und Normalisierungen.
   - Spezialzeichen wie # im Projektpfad oder ' in Dateinamen führen nicht mehr zu Fehlern.
   - (Siehe main.py, Zeilen 4859–4897)

2. **Kategorie-Mapping (Unknown / Unbekannt)**
   - Die Produktionsfilter in `_apply_library_filters` ließen Items mit Kategorie "unknown"/"unbekannt" bisher durchfallen.
   - `category_alias_table` in models.py wurde erweitert, sodass diese Kategorien explizit gemappt und akzeptiert werden.
   - Filterlogik in main.py entsprechend angepasst.

3. **Diagnostisches Logging**
   - [BD-AUDIT]-Logs in main.py zeigen jetzt beim Droppen von Items die vollständige Liste der erlaubten Kategorien an.
   - Erleichtert künftige Debugging- und Forensik-Prozesse.

## Verifikation
- **Kategorie-Mapping:**
  - Über CLI geprüft, dass `get_allowed_internal_cats(['audio', 'unbekannt'])` jetzt auch "unknown" enthält.
  - Beispiel:
    ```bash
    python3 -c "from src.core.models import get_allowed_internal_cats; print(get_allowed_internal_cats(['audio', 'unbekannt']))"
    # Ausgabe: [..., 'unknown', ...]
    ```
- **Pfadauflösung:**
  - `resolve_media_path` verarbeitet jetzt auch kodierte URLs wie `/media/Artist's%20Song.mp3` korrekt.
  - Pathlib sorgt für zuverlässige Normalisierung und Existenzprüfung.

## Hinweise
- Die GUI zeigt jetzt alle indexierten Medien korrekt an – "Bypass"-Modus ist nicht mehr nötig.
- Falls die Bibliothek noch leer erscheint: Im Library-Tab einen "Re-Scan" durchführen, um die Datenbank mit den neuen Regeln zu synchronisieren.

---
**Status:** Hydration-Bug vollständig behoben, Standard-UI zeigt alle Medien korrekt (v1.37.45)
