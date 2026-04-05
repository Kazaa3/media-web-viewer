<!-- Category: bug -->
<!-- Title_DE: GUI-Refresh-Fix für Installed Packages -->
<!-- Title_EN: GUI Refresh Fix for Installed Packages -->
<!-- Summary_DE: Behebt den dauerhaften Loading-Zustand im Options-Block „Installed Packages“ und ergänzt Testabdeckung -->
<!-- Summary_EN: Fixes persistent loading state in Options block “Installed Packages” and adds test coverage -->
<!-- Status: completed -->
<!-- Date: 2026-03-09 -->

# GUI-Refresh-Fix für Installed Packages

## Problem
Im Bereich **Options → Environment → Installed Packages** blieb die Anzeige teilweise dauerhaft auf:

- `Installed Packages`
- `Search packages...`
- `Loading...`

Der Refresh lief nicht sauber durch, obwohl bereits ein UI-Test für den Block existierte.

## Ursache
`loadEnvironmentInfo()` konnte bei fehlerhafter oder verzögerter Backend-Antwort ohne robusten Fallback enden.
Dadurch blieb der Initialzustand (`Loading...`) sichtbar.

## Umsetzung
In `web/app.html` wurde `loadEnvironmentInfo()` gehärtet:

- Timeout-Schutz mit `Promise.race(...)`
- Validierung auf ungültige Response (`!info || typeof info !== 'object'`)
- Einheitlicher Fehler-Fallback für alle Environment-Listen
- Packages-Block fällt sauber auf „keine Daten“ statt „Loading...“ zurück
- Such-Listener wird nur einmal gebunden (`dataset.bound`), um Mehrfach-Bindungen zu vermeiden

## Testabdeckung
Der bestehende Test wurde erweitert:

- Datei: `tests/test_installed_packages_ui.py`
- Neuer Test: `test_js_load_environment_info_has_timeout_and_error_fallback`
- Erwartet explizit Timeout-/Fallback-Snippets in der UI-Logik

Ergebnis lokal:

- `pytest -q tests/test_installed_packages_ui.py`
- **6 passed**

## Ergebnis
✅ Der Bereich bleibt nicht mehr im Loading-Zustand hängen.

✅ Fehlerfälle werden sichtbar und konsistent dargestellt.

✅ Testabdeckung deckt den GUI-Refresh-Fix nun direkt mit ab.

## Referenz
- Commit: `4af9a48`

<!-- lang-split -->

# GUI Refresh Fix for Installed Packages

## Problem
In **Options → Environment → Installed Packages**, the UI could remain stuck at:

- `Installed Packages`
- `Search packages...`
- `Loading...`

Refresh behavior did not complete reliably, even though a UI test already existed.

## Root Cause
`loadEnvironmentInfo()` lacked a robust fallback path when backend responses were invalid or delayed.
This could leave the initial loading state visible.

## Implementation
`loadEnvironmentInfo()` in `web/app.html` was hardened:

- Timeout guard via `Promise.race(...)`
- Invalid response validation (`!info || typeof info !== 'object'`)
- Consistent error fallback for all environment lists
- Packages section falls back to “no data” instead of “Loading...”
- Search listener bound only once (`dataset.bound`) to avoid duplicate handlers

## Test Coverage
Existing test was extended:

- File: `tests/test_installed_packages_ui.py`
- New test: `test_js_load_environment_info_has_timeout_and_error_fallback`
- Verifies timeout/fallback snippets in UI logic

Local result:

- `pytest -q tests/test_installed_packages_ui.py`
- **6 passed**

## Result
✅ Section no longer gets stuck in loading state.

✅ Error scenarios are rendered consistently.

✅ Test coverage now explicitly guards the GUI refresh fix.

## Reference
- Commit: `4af9a48`
