# Beschreibung: JSON-Konfigurationsdateien im Projekt

## Zweck und Einsatz
- Die JSON-Konfigurationsdateien in `web/` steuern das Verhalten und die Features der Web-Oberfläche und des Backends.
- Sie werden beim Start geladen und bestimmen z.B. Debug-Modus, Feature-Flags, Kategorien, API-Timeouts und mehr.

## Wichtige Dateien
- **config.json**: Hauptkonfiguration für Entwicklung (debug=true, viele Kategorien, Feature-Flags aktiv)
- **config.main.json**: Produktionseinstellungen (debug=false, weniger Kategorien, Feature-Flags meist deaktiviert)
- **config.develop.json**: Entwicklungs-/Testkonfiguration (ähnlich wie config.json, für spezielle Entwicklungszwecke)

## Typische Felder
- `debug`: true/false – Debug-Modus
- `log_level`: z.B. "DEBUG", "INFO"
- `start_page`: Startseite der UI
- `browse_default_dir`, `library_dir`, `additional_library_dirs`: Verzeichnisse für Medien
- `feature_flags`: Dict mit Schaltern für experimentelle Features
- `api`: Dict mit Timeout und Retry-Einstellungen
- `indexed_categories`, `displayed_categories`: Listen der Medienkategorien
- `env`: Umgebung (z.B. "production")

## Beispiel (Ausschnitt)
```json
{
    "debug": true,
    "log_level": "DEBUG",
    "feature_flags": {
        "experimental_transcoding": true,
        "verbose_parsing": true
    },
    "api": {
        "timeout": 30,
        "retries": 5
    },
    "indexed_categories": ["audio", "video", ...]
}
```

## Hinweise
- Die Konfigurationsdateien werden als dict geladen (`json.load()`), in der App als dict verwendet und ggf. wieder als JSON gespeichert.
- Änderungen an den Konfigs wirken sich direkt auf das UI- und Backend-Verhalten aus.
- Für verschiedene Umgebungen (Entwicklung, Produktion) gibt es unterschiedliche Konfigurationsdateien.

---

**Siehe auch:**
- web/config.json, web/config.main.json, web/config.develop.json
- Logbuch: JSONs Beschreibung
- src/core/main.py, web/
