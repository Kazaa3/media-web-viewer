# Implementation Plan – Fragment-Level Spawning Registry & Localized Diagnostics (v1.41.160)

## Ziel
Die "Black Screen"-Fehlerdiagnose wird von einem globalen Integrity-Test auf fragment-spezifische, lokalisierte Diagnostik erweitert. Jeder Split-View-Container erhält eigene Lifecycle-Hooks und einen individuellen "Force Write"-Test.

---

## 1. FRAGMENT ENGINE (JS)
- **[MODIFY] fragment_loader.js**
  - Lifecycle Hooks: Sende `WILL_SPAWN` vor dem Laden und `DID_SPAWN` nach DOM-Injektion eines Fragments.
  - Neue Methode: `FragmentLoader.injectLocalizedIntegrityTest(targetId)` – injiziert ein Testmuster nur in das angegebene Sub-Viewport-Element.
  - Targeting: Fragmentpfad wird automatisch abgeleitet, um die Pipeline für den jeweiligen Container zu prüfen.

## 2. CENTRAL BOOT REGISTRY (JS)
- **[MODIFY] ui_core.js**
  - Registry Implementation: Implementiere `window.auditFragmentHydration`, um den globalen State aller Fragment-Lifecycles zu pflegen.
  - Status Persistence: UI zeigt "Fetched", "Loading" und "Hydrated"-Status für jedes Fragment im Matrix-Panel an.

## 3. DIAGNOSTICS UI (HTML)
- **[MODIFY] diagnostics_sidebar.html**
  - Neuer Bereich: "FRAGMENT LIFECYCLE MATRIX" im HYD-Tab.
  - Dynamische Zeilen: Liste aller Fragments mit jeweils eigenem "Test"-Button für lokalen Force-Write.

---

## Hinweise
- Local Test: Schreibt ein farbiges DIV + Text in das Ziel-Fragment (kein externes HTML-File, maximale Zuverlässigkeit).

---

## Verification Plan
- **Manual Verification:**
  - Stress Test: Kategorien wechseln und prüfen, ob die Fragment-Matrix-LEDs im Sidebar-Panel von gelb (pending) auf grün (ready) wechseln.
  - Localized Test: "Test"-Button für ein verstecktes Fragment klicken und prüfen, ob nur dort ein Testmuster erscheint.

---

**Review erforderlich vor Umsetzung!**
