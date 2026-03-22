# Default-Konfigurationen im Projekt

## Zweck
- Default-Konfigurationen stellen sicher, dass das System auch ohne explizite Konfigurationsdatei mit sinnvollen Einstellungen startet.
- Sie dienen als Fallback, wenn keine oder eine fehlerhafte config.json vorhanden ist.

## Wo definiert?
- Im Code (z.B. in `main.py` oder einem eigenen config-Modul) als Python-dict
- Beispiel:
  ```python
  DEFAULT_CONFIG = {
      "debug": False,
      "log_level": "INFO",
      "start_page": "player",
      "browse_default_dir": "~/index",
      "library_dir": "media",
      "additional_library_dirs": [],
      "feature_flags": {
          "experimental_transcoding": False,
          "verbose_parsing": False,
          "show_test_tab": False
      },
      "api": {
          "timeout": 10,
          "retries": 2
      },
      "indexed_categories": ["audio"],
      "displayed_categories": ["audio"],
      "env": "production"
  }
  ```

## Mechanismus
- Beim Start wird versucht, die Konfigurationsdatei zu laden.
- Falls das Laden fehlschlägt, wird auf DEFAULT_CONFIG zurückgegriffen.
- Beispiel:
  ```python
  import json
  try:
      with open("web/config.json") as f:
          config = json.load(f)
  except Exception:
      config = DEFAULT_CONFIG
  ```

## Vorteile
- System bleibt lauffähig, auch wenn Konfigurationsdateien fehlen oder fehlerhaft sind
- Klare, dokumentierte Basiseinstellungen
- Erleichtert Entwicklung und Test

## Hinweise
- Die Default-Konfiguration sollte regelmäßig mit den tatsächlichen Konfigurationsdateien abgeglichen werden
- Änderungen an den Defaults wirken sich auf alle Umgebungen aus, die keine eigene config.json haben

---

**Siehe auch:**
- web/config.main.json, web/config.json
- src/core/main.py, config-Module
- Logbuch: JSON-Konfigs Beschreibung
