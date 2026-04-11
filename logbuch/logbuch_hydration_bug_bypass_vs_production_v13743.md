# Logbuch v1.37.43 – Hydration Bug: Bypass vs. Production

**Datum:** 2026-04-06

## Problemstellung
Die Mediathek zeigt Medien nur im "Bypass"-Modus an, nicht aber im Standard-Produktivmodus. Verdacht: Sonderzeichen wie # und ' in Pfaden/Filenames sowie Kategorie-Mapping-Fehler.

## Analyse
- **Bypass funktioniert:** DB und Eel-Bridge sind intakt, Problem liegt in Filter-/Pfadlogik der Produktion.
- **Filter-Logik:** `_apply_library_filters` nutzt `allowed_internal_cats` aus `displayed_categories`. Items mit Kategorie "unknown"/"unbekannt" werden ggf. ausgeschlossen.
- **Pfad-Handling:** Projektpfad enthält #: `/home/xc/#Coding/gui_media_web_viewer`. Unsachgemäße Behandlung als URL kann zu Fragmentierungsfehlern führen. Auch einfache Anführungszeichen (') können SQL/JSON-Probleme verursachen.

## Umsetzung & Maßnahmen
1. **Backend-Logik-Audit**
   - `_apply_library_filters` robuster machen, Drop-Gründe klar loggen.
   - `resolve_media_path` prüft und behandelt # und ' korrekt.
   - Safety-Check für # in Rückgabedaten von `get_library`.
2. **Model-Update**
   - `category_alias_table` in `models.py` um explizite Mappings für "unknown"/"unbekannt" erweitern.
   - `MediaItem` normalisiert Kategorien auf Kleinbuchstaben.
3. **DB-Parität**
   - Alle Kategorien per `LOWER(category)` vereinheitlichen.
   - Diagnostikfunktion für # und ' in DB-Einträgen.
4. **Verifikation**
   - `get_library(force_raw=True)` ausführen, Kategorien prüfen.
   - Umschalten zwischen Bypass/Normal, [BD-AUDIT]-Logs auswerten.
   - Test: Datei mit # oder ' im Pfad abspielen.

## Offene Fragen
- Sollen "unknown"/"unbekannt"-Kategorien immer in "Alle" angezeigt werden?
- Gibt es konkrete Dateien mit ' im Namen, die fehlen?

## Lessons Learned
- Sonderzeichen in Pfaden und Kategorien müssen überall konsistent behandelt werden.
- Filter- und Mapping-Logik muss robust und transparent sein.
- Forensische Protokollierung ist essenziell für nachhaltige Fehlerdiagnose.

---
**Status:** Hydration-Bug erkannt, Maßnahmen zur Behebung eingeleitet (v1.37.43)
