# Walkthrough - Forensic Window Tracking System (v1.37.52)

## Zusammenfassung
Ein umfassendes, forensisches Window Tracking System (v1.37.52) wurde implementiert. Damit werden alle Anwendungs-Views (insbesondere der Audio Player) korrekt gespawnt, hydriert und überwacht. Dies erfüllt die Anforderung eines "clean rebuild" mit vollständigem Window-Tracking.

---

## 1. Forensic Window Manager (WM)
- **Zentraler Orchestrator:** `web/js/window_manager.js` verwaltet den gesamten Lebenszyklus aller UI-"Inner Windows".
- **State Registry:** Jede Hauptansicht (Player, Library, Editor, Database) ist mit eigenem Shell- und Fragment-Target registriert.
- **Hydration Guard:** Der WM stellt sicher, dass ein Fragment vollständig geladen und als "gesund" bestätigt ist, bevor das Fenster sichtbar wird.
- **Geometry Enforcement:** Automatische Neuberechnung von Höhe und Breite beim Aktivieren eines Fensters verhindert "Black Screen" durch 0px-Container.

## 2. Standardized Boot Orchestration
- **Startup-Refactoring:** Der App-Start in `app_core.js` nutzt jetzt die neue WM-Infrastruktur.
- **Audio Player Registration:** Der Audio Player ist das erste getrackte Fenster, inkl. Initialisierungshooks (`renderPlaylist`).
- **Audited Activation:** 2-stufiger Verifizierungsprozess (Hydration → Activation) für den Start-Tab.
- **Forensic Handshake:** Jede Fensteraktivierung wird an die `auditFragmentHydration`-Bridge gemeldet und ist in der Diagnostics Sidebar (HYD-Tab) sichtbar.

## 3. Navigation Hardening
- **switchTab:** Die globale Funktion in `ui_nav_helpers.js` wurde komplett neu gebaut:
  - **Delegated Authority:** Alle Layout-Transitions werden an den WindowManager delegiert.
  - **Performance Tracking:** Zeitmessung, wie lange ein Fenster zum "Healthy"-Status braucht – für schnelle Fehlerdiagnose.
  - **Locking & Safety:** Verhindert Race Conditions durch globales Navigations-Lock, das erst nach erfolgreicher Ausführung durch den WM freigegeben wird.

---

## Summary of Changes
- **Neu:** `web/js/window_manager.js` – Kern für UI-State-Tracking
- **Geändert:** `web/app.html` – WM-Script in das Master-Shell integriert
- **Geändert:** `web/js/app_core.js` – Boot-Sequenz auf WM-Registry umgestellt
- **Geändert:** `web/js/ui_nav_helpers.js` – Tab-Switching nutzt jetzt das forensische Activation-Engine

---

Das System ist jetzt "aware" über den Zustand jedes Fensters. Die Health-States von Audio Player und Co. sind in Echtzeit im HYD-Tab der Diagnostics Sidebar einsehbar.
