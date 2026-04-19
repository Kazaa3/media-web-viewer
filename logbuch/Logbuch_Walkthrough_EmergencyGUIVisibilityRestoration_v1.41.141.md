# Walkthrough – Emergency GUI Visibility Restoration (v1.41.141)

## Zusammenfassung
Die Emergency Forensic Restoration (v1.41.141) wurde erfolgreich in "kleinsten Schritten" umgesetzt. Die GUI ist jetzt gegen "Black Hole"-Zustände gehärtet und kann im Notfall manuell wieder sichtbar gemacht werden.

---

## 1. Hard-Wired Life Sign & Recovery Button
- **[FLASH] Button:**
  - Minimalistischer [FLASH]-Button im Header, der `window.forceLife()` triggert.
- **emergency-life-sign:**
  - Rotes Overlay-Band am oberen Rand der GUI, das im Fehlerfall sichtbar gemacht wird.

## 2. Brute-Force forceLife() Engine
- **window.forceLife():**
  - Entfernt alle `mwv-hide-*`-Klassen vom Body.
  - Setzt `opacity: 1` auf `.loading-fragment`-Elemente.
  - Injiziert "LIFE DETECTED"-Text direkt ins Viewport.
  - Erzwingt per `switchTab('status')` die Anzeige der Diagnoseansicht.

## 3. Fragment Loader Hardening
- **Timeout-Mechanismus:**
  - Jeder Fragment-Request wird mit `performance.now()` geloggt.
  - Nach 3,5s ohne Erfolg wird ein Fehlerpanel angezeigt (statt Black Screen) und ein CRITICAL TIMEOUT geloggt.

## 4. Orchestrator Resilience
- **ui_core.js:**
  - Die Visibility Matrix hat jetzt immer eine sichere Fallback-Konfiguration, selbst wenn der Backend-Handshake (Eel) fehlschlägt.

---

## Verification Steps
1. **Header Check:**
   - Der pulsiert rote [FLASH]-Button ist im Header sichtbar.
2. **Trigger Recovery:**
   - Bei Black Screen: [FLASH] klicken → GUI wird sofort sichtbar, "Life Detected"-Meldung erscheint.
3. **Console Audit:**
   - Mit `dumpNavRegistry()` im Dev-Console (F12) kann der aktuelle Level 2 Registry-Zustand geprüft werden.

---

**Warnung:**
Der [FLASH]-Button ist ein Notfall-Tool. Bei normal funktionierender GUI ist er nicht nötig, bleibt aber als "Hard-Wired"-Sicherheitsanker dauerhaft verfügbar.

---

**Alle Blackout- und Fragment-Ladeprobleme sind jetzt forensisch abfangbar.**
