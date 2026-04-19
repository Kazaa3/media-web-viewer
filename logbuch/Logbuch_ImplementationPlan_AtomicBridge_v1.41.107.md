# Implementation Plan – v1.41.107 Atomic Bridge

## Ziel
Synchronisierung der neuen Atomic Shell Architektur mit der bestehenden JavaScript-Logik durch Behebung von ID-Mismatches und Aktualisierung des Boot-Handshakes.

---

## Phase 1: Logic Synchronization
- **[MODIFY] app_core.js**
  - Re-register Window Manager: Passe die `shellId`-Werte für Player, Library, Editor und Database an die neuen Atomic Shell IDs (z.B. `player-panel-container`) an.
  - HUD Update: Aktualisiere die Startup-Info-Logik, sodass sie auf `#diag-pid`, `#diag-boot` und `#diag-up` statt auf das alte `#sync-status` zielt.

## Phase 2: UI Handshake
- **[MODIFY] shell_master.html**
  - Bootstrap Trigger: Füge ein minimales Inline-Skript hinzu, das `updateGlobalSubNav()` aufruft, sobald die UI-Engine bereit ist.
  - Structural Integrity: Stelle sicher, dass Platzhalter für Modal und Kontextmenü vorhanden sind.

## Phase 3: Aesthetic Refinement
- **[MODIFY] shell_master.css**
  - Pulse Animation: Füge eine dezente Pulse-Animation für "Initializing..."-Zustände hinzu.
  - Transition Smoothness: Definiere CSS-Transitions für Sub-Nav-Pills.

---

## Verification Plan
- **Hydration Check:** Prüfen, dass die "INITIALIZING..."-Nachricht verschwindet und durch das Player-UI ersetzt wird.
- **Nav Check:** Verifizieren, dass die Sub-Nav-Bar korrekt "Queue", "Playlist" usw. anzeigt.
- **HUD Check:** Sicherstellen, dass "PID:", "BOOT:" und "UP:" mit echten Backend-Daten befüllt werden.

---

**Review erforderlich nach Umsetzung!**
