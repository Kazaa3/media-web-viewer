# Implementation Plan – Emergency GUI Visibility Restoration (v1.41.141)

## Ziel
Sofortige Sichtbarkeitswiederherstellung der Media Viewer GUI im "Black Hole"-Zustand durch forensische Hard-Write-Maßnahmen und manuelle Recovery-Tools.

---

## 1. EMERGENCY LIFE-SIGN (Hard-Write)
- **[MODIFY] app.html**
  - Emergency Overlay: Füge ein `<div id="emergency-life-sign">` ein, das standardmäßig versteckt ist, aber per minimalistischer `<script>`-Logik sichtbar gemacht wird, falls die Hydration fehlschlägt.
  - Force Life Button: Platziere einen auffälligen "FLASH"-Button im Header, der `window.forceLife()` aufruft.

## 2. BRUTE-FORCE RECOVERY
- **[MODIFY] ui_nav_helpers.js**
  - `window.forceLife()`: Implementiere eine Funktion, die:
    - Alle `mwv-hide-*`-Klassen vom Body entfernt.
    - `opacity: 1` auf alle `.loading-fragment`-Elemente setzt.
    - "LIFE DETECTED"-Text manuell ins Viewport injiziert.
    - `switchTab('status')` triggert, um die Diagnoseansicht zu erzwingen.

## 3. LOADER AUDIT
- **[MODIFY] fragment_loader.js**
  - Stall Logging: Füge `performance.now()`-Logging zu jedem Fragment-Request hinzu.
  - Fail-Safe Reveal: Wenn ein Fragment >2s zum Laden braucht, zeige eine Fehlermeldung anstelle eines schwarzen Bildschirms.

## 4. Backend-Bypass (optional)
- Notfalls kann der Emergency Life-Sign auch den Backend-Handshake (Eel) umgehen, um Sichtbarkeit zu garantieren.

---

## Verification Plan
- **Manual Verification:**
  - Visual Life Sign: Nach dem Refresh muss ein roter "LIFE"-Indikator erscheinen, falls die UI hängt.
  - Flash Recovery: Der "FLASH"-Button im Header muss die Diagnoseansicht oder einen Life-Sign-Text erzwingen und den "Black Hole"-Zustand beenden.

---

**Review erforderlich vor Umsetzung!**
