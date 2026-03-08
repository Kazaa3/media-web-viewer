# Logbuch 57 — UI Testing

**Datum:** 08.03.2026  
**Bereich:** Qualitätssicherung / UI Testing / Dokumentation

## Ziel
Die komplette Test-Dokumentation wurde aus dem Testordner entfernt und vollständig in diesen UI-Logbucheintrag überführt.

## Test-Übersicht
Aktueller Stand: **3 Test-Suites** mit **25 Tests insgesamt**.

| Test-Suite | Tests | Status | Beschreibung |
|---|---:|---|---|
| `tests/test_i18n_completeness.py` | 8/8 | ✅ PASSED | i18n Basis-Validierung |
| `tests/test_i18n_deep_scan.py` | 6/7 | ⚠️ WARN | i18n Deep Scan |
| `tests/test_ui_events.py` | 10/10 | ✅ PASSED | UI Events & Interaktionen |

**Gesamt:** 24/25 Tests bestanden (**96% Pass Rate**)

## Ausführung

### Alle Tests
```bash
./tests/run_all_tests.sh
```

### Einzeln
```bash
python tests/test_i18n_completeness.py
python tests/test_i18n_deep_scan.py
python tests/test_ui_events.py
```

## Test-Suites im Detail

### 1) i18n Completeness (`tests/test_i18n_completeness.py`)
**8 Tests | Status: ✅ alle bestanden**

- JSON-Struktur korrekt
- Key-Parität DE/EN korrekt (238 Keys je Sprache)
- Required Keys vorhanden
- Keine hardcoded Strings
- Nur `t()` (keine veralteten `i18n()` Aufrufe)
- `@eel.expose` Dekoratoren validiert
- `data-i18n` Attribute valide (96)
- `t()` Calls valide (70)

**Nutzen:** Verhindert i18n-Breaks auf Infrastruktur-Ebene.

### 2) i18n Deep Scan (`tests/test_i18n_deep_scan.py`)
**7 Tests | Status: ⚠️ 6/7 bestanden**

- ⚠️ HTML Static Text: 23 technische Labels (akzeptabel)
- ✅ `alert()/confirm()` bereinigt
- ✅ `innerHTML/innerText` bereinigt
- ⚠️ 18 JS-String-Literals als Warnungen
- ✅ Buttons/Labels internationalisiert
- ✅ `placeholder/title` internationalisiert
- ✅ `console.log` ohne kritische Funde

**Nutzen:** Findet übersehene Texte außerhalb klassischer i18n-Prüfungen.

### 3) UI Events (`tests/test_ui_events.py`)
**10 Tests | Status: ✅ alle bestanden**

- 45 Buttons mit Event-Handlern
- 11 Inputs validiert
- 45 registrierte Event-Handler (u. a. `click` 14×)
- Kritische Buttons (`scan`, `save`, `cancel`) vorhanden
- Links/Selects validiert
- Keyboard: `Escape`, `Enter` erkannt
- 53 `eel.*` Aufrufe (42 unique)
- Modal-/Form-Checks erfolgreich

**Nutzen:** Schützt vor toten UI-Elementen und Interaktions-Regressionen.

## Kennzahlen
- **i18n Keys:** 238 DE + 238 EN
- **Event-Abdeckung:** 45 Buttons validiert
- **i18n-Referenzen:** 96 `data-i18n`, 70 `t()` Calls
- **Backend-Integration:** 53 `eel.*` Aufrufe
- **Gesamtqualität:** 96% Pass Rate

## CI/CD Integration

### GitHub Actions (Beispiel)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          python -m pip install -r requirements.txt
          ./tests/run_all_tests.sh
```

### Pre-Commit Hook (Beispiel)
```bash
#!/bin/bash
./tests/run_all_tests.sh
if [ $? -ne 0 ]; then
  echo "Tests failed! Commit aborted."
  exit 1
fi
```

## Typische Fehlerbilder

### i18n Completeness
- Fehlende Keys in `web/i18n.json`
- Veraltete `i18n()` Aufrufe statt `t()`
- Hardcoded Text in HTML/JS

### i18n Deep Scan
- Texte direkt in `innerHTML`/`innerText`
- Attributtexte ohne `data-i18n` Mapping

### UI Events
- Buttons ohne `onclick`/`addEventListener`
- Inputs ohne `change`/`input` Handler
- Links mit `href="#"` ohne Handler

## Ergebnis
- Test-Dokumentation ist nun **vollständig im UI-Logbuch** geführt.
- Der Testordner enthält **keine separate README** mehr.
- Der Stand ist reproduzierbar, versionssicher und release-fähig dokumentiert.
