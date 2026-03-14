# 92 Release Prep – Package Display Robustness and Gates

**Datum:** 09.03.2026  
**Bereich:** Release-Vorbereitung / Regressionstests / Robustheit  
**Status:** ✅ umgesetzt

## Ziel
Vor Release sicherstellen, dass die Paketanzeige im Options-Tab stabil ist und Regressionen zuverlässig durch Pipeline/Gates erkannt werden.

## Problem
In Einzelfällen blieb die Paketliste im Options-Tab leer (`No packages found`), obwohl eine aktive Umgebung vorhanden war.

## Technische Maßnahmen

### 1) Safety Fallback im Backend (`main.py`)
`get_environment_info()` nutzt jetzt eine robuste Mehrstufen-Strategie für `installed_packages`:
1. `pip list --format=json`
2. Fallback: `pip list --format=columns` + Parser
3. Fallback: `importlib.metadata` / `pkg_resources`
4. Finaler Safety-Step: wenn weiterhin leer, erneut Fallback erzwingen

Zusätzlich wird `installed_packages_source` zur Diagnose zurückgegeben.

### 2) Safety Retry im Frontend (`web/app.html`)
`loadEnvironmentInfo()` führt bei initial leerer Paketliste automatisch einen zweiten Abruf mit `get_environment_info(true)` aus (Force-Refresh), um temporäre/Cache-bedingte Leerzustände zu vermeiden.

### 3) Regressionstest ergänzt
Neue Datei: `tests/test_environment_packages_fallback.py`
- simuliert `pip list` Fehler
- prüft, dass über Fallback trotzdem Pakete zurückkommen
- setzt Environment-Cache im Test sauber zurück (keine Test-Kontamination)

### 4) Pipeline / Gates erweitert
Neuer Test ist in allen relevanten Gates enthalten:
- `build_system.py` (`BUILD_TEST_GATE`)
- `build_deb.sh`
- `build.py`

## Validierung
Gezielter Gate-Lauf:
- `tests/test_environment_packages_fallback.py`
- `tests/test_performance_probes.py`
- `tests/test_installed_packages_ui.py`
- `tests/test_ui_session_stability.py`

Ergebnis: **20 passed**

## Release-Relevanz
Damit ist der bekannte Paketanzeigen-Fehler gegen den kritischen Ausfallpfad abgesichert und Teil der verpflichtenden Build-Gates.
