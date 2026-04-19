# Implementation Plan – Navigation Integrity & DOM Forensics (v1.41.140.0)

## Ziel
Behebung des "Empty Level 2"-Problems und finale GUI-Restaurierung durch Härtung der Navigationsorchestrierung und Bereitstellung von DOM-basierten Forensik-Tools.

---

## 1. UI Navigation Orchestrator
- **[MODIFY] ui_nav_helpers.js**
  - Startup Sync: Passe den `window.addEventListener('load', ...)`-Block an, sodass `updateGlobalSubNav(savedCategory)` (aus localStorage) statt eines hartkodierten Werts aufgerufen wird.
  - Safety Guard: Ergänze einen Fallback in `updateGlobalSubNav`, der bei leerem Container nach einem Kategorie-Switch erneut triggert.
  - DOM Diagnostic: Implementiere `window.dumpNavDom()`, um die aktuell registrierten Level 2 Pills tabellarisch in der Konsole auszugeben.

## 2. Diagnostic Sidebar
- **[MODIFY] diagnostics_sidebar.html**
  - Ergänze im HLT (Health)-Tab eine Prüfung auf "Sub-Nav Integrity" (Level 2 Pill Count).

---

## Verification Plan
- **Automated Tests:**
  - Führe `node -c web/js/ui_nav_helpers.js` aus, um Syntaxfehler auszuschließen.
  - Grep-Audit: Überprüfe die 14 Kategorie-Keys gegen das `SUB_NAV_REGISTRY`.
- **Manual Verification:**
  - Klicke durch die Sidebar-Kategorien und beobachte die Level 2 Bar (`sub-nav-container`).
  - Nutze `dumpNavDom()` in der Dev-Konsole, um den Registry-Zustand zu prüfen.

---

**Review erforderlich nach Umsetzung!**
