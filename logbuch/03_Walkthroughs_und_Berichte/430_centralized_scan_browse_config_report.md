# Centralizing Configuration for Scan and Browse Paths

**Datum:** 14.03.2026
**Autor:** Copilot

---

## Ziel

Die Konfiguration der Standardpfade für Medien-Scan (SCAN_MEDIA_DIR) und den Datei-Browser (BROWSER_DEFAULT_DIR) wird zentralisiert. Beide Pfade werden künftig ausschließlich über das zentrale Konfigurationsobjekt (PARSER_CONFIG) verwaltet und synchronisiert.

---

## Vorgehen

1. **Identifikation der zentralen Config:**
   - Das Objekt `PARSER_CONFIG` in main.py ist die zentrale Konfigurationsquelle.
   - scan_dirs und weitere Einstellungen werden bereits dort verwaltet.

2. **Zentralisierung:**
   - SCAN_MEDIA_DIR und BROWSER_DEFAULT_DIR werden als eigene Keys in PARSER_CONFIG (z.B. unter parser_settings) abgelegt.
   - Alle Zugriffe im Code werden so angepasst, dass sie immer aus PARSER_CONFIG lesen/schreiben.

3. **Synchronisation:**
   - Änderungen an den Default-Pfaden werden automatisch in der zentralen Config gespeichert und stehen allen Komponenten konsistent zur Verfügung.

4. **Dokumentation:**
   - Die neuen Config-Keys und ihre Defaultwerte werden dokumentiert.

---

## Ergebnis

- Die Verwaltung der Scan- und Browse-Pfade ist zentral, konsistent und leicht wartbar.
- Künftige Änderungen an den Pfaden erfordern nur noch Anpassungen in der zentralen Config.
- Die Codebasis ist von doppelten oder inkonsistenten Pfaddefinitionen befreit.

---

**Details siehe:**
- [main.py](/src/core/main.py)
- [walkthrough.md](walkthrough.md)
