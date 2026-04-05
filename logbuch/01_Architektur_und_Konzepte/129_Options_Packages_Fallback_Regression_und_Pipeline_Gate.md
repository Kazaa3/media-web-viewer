# 91 Options Packages Fallback Regression und Pipeline-Gate

**Datum:** 09.03.2026  
**Bereich:** Environment UI / Build-Pipeline / Regression-Schutz  
**Status:** ✅ umgesetzt

## Ausgangslage
Im Options-Tab trat weiterhin der Zustand "No packages found" auf, obwohl eine aktive Umgebung vorhanden war.

## Ursache
`get_environment_info()` verließ sich primär auf `pip list --format=json`. Bei Fehlern/inkonsistentem Verhalten konnte die Paketliste leer bleiben, was in der GUI direkt als "No packages found" sichtbar wurde.

## Umsetzung
1. **Backend-Härtung (`main.py`)**
   - Nach `_get_installed_packages()` wurde ein finaler Safety-Fallback ergänzt:
     - wenn Ergebnis leer ist → `_get_packages_fallback()`

2. **Neuer Regressionstest**
   - Datei: `tests/test_environment_packages_fallback.py`
   - Simuliert `pip list` mit non-zero Rückgabe
   - Erzwingt Fallback über `importlib.metadata.distributions()`
   - Erwartet nicht-leere `installed_packages` + korrekten `package_count`

3. **In Build-Gates/Pipeline eingebaut**
   - `build_system.py` (`BUILD_TEST_GATE`)
   - `build_deb.sh` (Shell-Gate)
   - `build.py` (Standalone Build-Gate)

## Ergebnis
- Der bekannte "No packages found"-Regressionspfad ist nun testbar abgesichert.
- Pipeline/Gates brechen künftig bei erneuter Regression früh ab.
