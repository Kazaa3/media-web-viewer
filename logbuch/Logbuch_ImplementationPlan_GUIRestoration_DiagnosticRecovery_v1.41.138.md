# Implementation Plan – GUI Restoration & Diagnostic Recovery

## Ziel
Behebung des "Black GUI"-Problems durch dedizierte Reparatur von ui_nav_helpers.js und Wiederherstellung der Mock-Diagnosefunktionen für Testzwecke.

---

## 1. Critical Logic Repair
- **[MODIFY] ui_nav_helpers.js**
  - Deduplication: Entferne doppelte `initForensicUI`- und `renderHydrationMatrix`-Blöcke am Dateiende.
  - Syntax Correction: Korrigiere den Block `window.addEventListener('load', ...)`, sodass die Initialisierung (State-Sync, UI-Refresh, Player-Submenu) korrekt abläuft.
  - Registry Alignment: Stelle sicher, dass das neue 14-Kategorien-`SUB_NAV_REGISTRY`-Objekt erhalten bleibt und korrekt verwendet wird.

## 2. Diagnostic Restoration
- **[MODIFY] gui_diagnostics.js**
  - Sorge dafür, dass `forceHydrationTest()` sowohl `allLibraryItems` als auch `currentPlaylist` mit dem "Elite Mock Pack" befüllt.
- **[MODIFY] diagnostics_sidebar.html**
  - Stelle sicher, dass im HYD-Tab der Diagnostics Sidebar ein sichtbarer Button "FORCE HYDRATION TEST" existiert.

---

## Verification Plan
- **Automated Tests:**
  - Führe `node -c web/js/ui_nav_helpers.js` aus, um Syntaxfehler auszuschließen.
- **Manual Verification:**
  - Starte die GUI, prüfe, ob der "Black Screen" verschwunden ist und Header/Sidebar sichtbar sind.
  - Öffne Diagnostics (Logbuch oder Dashboard), gehe zum HYD-Tab, klicke auf "FORCE HYDRATION TEST" und prüfe, ob Player Queue und Library mit Mock-Items (z.B. Cyberpunk_Nocturne) gefüllt werden.

---

**Review erforderlich nach Umsetzung!**
