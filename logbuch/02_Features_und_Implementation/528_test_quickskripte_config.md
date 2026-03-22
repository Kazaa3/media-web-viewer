# Test- und Quick-Skripte zum Setzen der Config on the Fly

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert, wie Test- und Quick-Skripte genutzt werden können, um Konfigurationen (z.B. Debug-Flags, Log-Level, Feature-Flags) zur Laufzeit gezielt zu setzen oder zu überschreiben.

---

## 1. Testskripte
- Im Verzeichnis `tests/` existieren zahlreiche Tests, die gezielt Konfigurationswerte setzen oder überschreiben können.
- Beispiele:
  - `test_change_log_level_console.py`: Testet das Setzen verschiedener Log-Level.
  - `test_debug_flags.py`: Testet das Aktivieren/Deaktivieren von Debug-Flags.
  - `test_options_configuration.py`: Testet das Setzen und Übernehmen von Konfigurationsoptionen.
- Viele Tests nutzen Fixtures oder Helper, um Configs temporär zu patchen (z.B. mit `monkeypatch`, `tmp_path`, eigenen Test-Configs).

---

## 2. Quick-Skripte & Hilfs-Tools
- Im Verzeichnis `scripts/` können eigene Quick-Skripte angelegt werden, um Konfigurationsdateien (z.B. `web/config.json`) on the fly zu ändern.
- Beispiel für ein Quick-Skript (Python):
  ```python
  import json
  from pathlib import Path

  config_path = Path('web/config.json')
  config = json.loads(config_path.read_text(encoding='utf-8'))
  config['log_level'] = 'DEBUG'
  config['feature_flags']['verbose_parsing'] = True
  config_path.write_text(json.dumps(config, indent=2), encoding='utf-8')
  print('Config angepasst!')
  ```
- Solche Skripte können beliebig erweitert werden (z.B. Kommandozeilen-Argumente, verschiedene Profile, etc.).

---

## 3. Hinweise
- Änderungen an der Config wirken sich meist erst nach Neustart des Backends aus.
- Für temporäre Test-Configs empfiehlt sich die Nutzung von Kopien oder das Rücksetzen nach dem Test.
- Viele Tests und Skripte sind bereits vorhanden und können als Vorlage genutzt werden.

---

**Siehe auch:**
- [Debug-Log-Level & Parser-Logging – Status & offene Fragen](2026-03-15_debug_log_level_status.md)
- [requirements.txt-Anzeige ohne Prüfung – Logbuch](2026-03-15_requirements_anzeige_ohne_pruefung.md)
