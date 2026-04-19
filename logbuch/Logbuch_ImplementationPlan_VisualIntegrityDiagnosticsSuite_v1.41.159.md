# Implementation Plan – Visual Integrity Diagnostics Suite (v1.41.159)

## Ziel
Ein robuster Visual Integrity Test wird implementiert, um die Ursache von "Black Screen"-Fehlern eindeutig zu diagnostizieren. Ein High-Priority-Overlay wird direkt auf die DOM-Root geschrieben und beweist, ob das Problem im Logik- oder Rendering-Bereich liegt.

---

## 1. DIAGNOSTICS LOGIC (JS)
- **[MODIFY] diagnostics_helpers.js**
  - Neue Funktion: `runVisualIntegrityTest()`
    - Erstellt ein DIV auf `document.body`-Ebene mit `z-index: 99999`.
    - Overlay zeigt: großen Status-Text ("MWV INTEGRITY OK"), Forensic Version, aktuelle Systemzeit.
    - Enthält einen "Close Test"-Button zum Entfernen des Overlays.

## 2. DIAGNOSTICS UI (HTML)
- **[MODIFY] diagnostics_sidebar.html** (falls vorhanden) oder **app.html**
  - Add Button: Neuer Button im Bereich "System Health" oder "Recovery" des Diagnostics-Panels, der den Test auslöst.

---

## Hinweise
- Der Test ist "destruktiv" (überdeckt die UI), aber 100% temporär und reversibel.
- Kein Auto-Trigger: Test wird nur manuell ausgelöst, um die Entwicklung nicht zu stören.

---

## Verification Plan
- **Manual Verification:**
  - Stress Test: Test wird manuell aus der Konsole ausgelöst, Overlay erscheint korrekt.
  - Cleanup Test: "Close"-Button entfernt das Overlay und stellt die Sichtbarkeit wieder her.

---

**Review erforderlich vor Umsetzung!**
