<!-- Category: UI -->
<!-- Title_DE: Internationalisierung abgeschlossen -->
<!-- Title_EN: Internationalization completed -->
<!-- Summary_DE: Vollständige i18n-Abdeckung in UI und JavaScript mit Deep-Scan- und Cardinality-Validierung erreicht. -->
<!-- Summary_EN: Full i18n coverage in UI and JavaScript achieved with deep-scan and cardinality validation. -->
<!-- Status: COMPLETED -->

# Internationalisierung abgeschlossen

## Stand
Die Internationalisierung ist für UI-Markup und relevante JavaScript-Ausgaben vollständig umgesetzt.

## Umgesetzt
- Hardcoded Texte in HTML und JS durch `data-i18n` und `t('...')` ersetzt.
- Fehlende Key-Paare in `web/i18n.json` ergänzt (DE/EN-Parität gehalten).
- Lade-/Fehlertexte, Dialoge, VLC-Statusmeldungen, Environment-Leerzustände und Test-Dialoge auf i18n gemappt.
- Footer-/Status-Attribute (inkl. `title`) auf deklarative i18n-Bindungen umgestellt.

## Test-Validierung
- `tests/test_i18n_completeness.py`: **9/9 passed**
- `tests/test_i18n_deep_scan.py`: **8/8 passed**
	- inkl. **Type Cardinality**: `text 95/95`, `placeholder 0/0`, `title 0/0`, `alt 0/0`

## Kennzahlen
- i18n-Keys: **305 DE / 305 EN**
- Valide `data-i18n` Referenzen: **130**
- Valide `t()` Referenzen: **111**

## Ergebnis
Die App ist i18n-seitig konsistent, regressionsgeprüft und dokumentiert.

<!-- lang-split -->

# Internationalization completed

## Status
Internationalization is fully implemented for UI markup and relevant JavaScript output paths.

## Implemented
- Replaced hardcoded UI/JS strings with `data-i18n` and `t('...')` bindings.
- Added missing DE/EN key pairs in `web/i18n.json` while preserving parity.
- Mapped loading/error messages, dialogs, VLC status messages, environment empty states, and test dialogs to i18n keys.
- Converted footer/status attributes (including `title`) to declarative i18n bindings.

## Test validation
- `tests/test_i18n_completeness.py`: **9/9 passed**
- `tests/test_i18n_deep_scan.py`: **8/8 passed**
	- incl. **Type Cardinality**: `text 95/95`, `placeholder 0/0`, `title 0/0`, `alt 0/0`

## Metrics
- i18n keys: **305 DE / 305 EN**
- Valid `data-i18n` references: **130**
- Valid `t()` references: **111**

## Result
The application is i18n-consistent, regression-validated, and documented.
