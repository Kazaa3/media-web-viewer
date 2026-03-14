# Hardcoded Path Audit & Centralization Plan

**Datum:** 14.03.2026
**Autor:** Copilot

---

## Ziel

Alle hartkodierten Pfade im Projekt werden identifiziert und in eine zentrale Konfiguration überführt, um maximale Flexibilität und Wartbarkeit zu gewährleisten.

---

## Analyse (Stand 14.03.2026)

Gefundene hartkodierte Pfade (Beispiele):
- PROJECT_ROOT, SRC_DIR, MEDIA_DIR, CACHE_DIR, test_dir, app_file, logs/ui_trace_environment_info.log
- VENV-Namen (.venv_core, .venv_run, etc.) in VENV_STRATEGY
- SCAN_MEDIA_DIR und BROWSER_DEFAULT_DIR: bereits aus PARSER_CONFIG, aber mit Fallbacks auf Path(__file__).parent/"media" bzw. Path.home()

---

## Maßnahmen

1. **Zentralisierung:**
   - Alle Defaultwerte (media, logs, web, tests, etc.) werden in die zentrale Config (z.B. PARSER_CONFIG oder eigene config.json) aufgenommen.
   - Fallbacks im Code werden durch Config-Keys ersetzt.
   - VENV-Namen werden in der Config dokumentiert und ggf. zentralisiert.

2. **Code-Anpassung:**
   - Alle Stellen, die bisher Pfade direkt berechnen, lesen diese künftig aus der zentralen Config.

3. **Dokumentation:**
   - Die neuen Config-Keys und deren Defaultwerte werden dokumentiert.

---

## Ergebnis

- Keine hartkodierten Pfade mehr im Code.
- Alle Pfade sind konfigurierbar und zentral dokumentiert.
- Die Codebasis ist maximal flexibel und zukunftssicher.

---

**Details siehe:**
- [main.py](/src/core/main.py)
- [walkthrough.md](walkthrough.md)
