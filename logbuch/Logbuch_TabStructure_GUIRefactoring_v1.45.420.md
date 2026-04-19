# Fixing Tab Structure and Refactoring GUI Tests (v1.45.420)

## Zielsetzung
Behebung der strukturellen Fehler nach dem Parser-Tab, Bereinigung der Sub-Tabs/Modals und Einführung modularer GUI-Tests für nachhaltige UI-Qualität.

---

## Proposed Changes

### 1. HTML Structural Fix (app.html)
- Fehlendes </div> für den inner wrapper von options-environment-view (Zeile 3485) ergänzt.
- Überflüssiges </div> entfernt (vermutlich in Parser oder Reporting).
- Klare Anchor-Kommentare für alle Hauptbereiche und Sub-Tabs eingefügt.

### 2. Options & Reporting Refactoring
- Sub-Tab-Navigation für Options und Reporting standardisiert.
- "Architektur" (Environment) Sub-View zeigt das Sub-Menü immer korrekt an.
- Modals am Dateiende gruppiert, sauber getrennt und kommentiert.

### 3. i18n Audit
- i18n.json geprüft: Alle Nav-Tags und Tab-Titel sind konsistent mit den nav_ Keys.

### 4. Modular GUI Tests
- Neues Verzeichnis tests/gui/ für modulare Tests angelegt.
- tests/gui/test_tabs.py: Testet Haupt-Tab-Switching.
- tests/gui/test_subtabs.py: Testet Sub-Tab-Switching (Options, Reporting).
- tests/gui/test_modals.py: Testet Modal-Logik und Sichtbarkeit.

---

## Verification Plan
- **Automatisierte Tests:**
    - Neue GUI-Tests mit pytest/unittest ausführen.
    - scripts/gui_validator.py nutzen, um finalen DIV-Stack-Size=0 zu validieren.
- **Manuelle Prüfung:**
    - Sichtprüfung: Parser, Debug, Tests und Video Player Tabs sind sichtbar und funktionieren.
    - Sub-Tab-Switching in Options und Reporting testen.
    - Modal-Verhalten prüfen.

---

**Status:**
- Tab-Struktur und Sub-Tabs sind bereinigt, Modals sauber getrennt, GUI-Tests modularisiert.
- Architektur ist bereit für nachhaltige UI-Qualitätssicherung.
