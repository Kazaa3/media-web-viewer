# Walkthrough – Fragment Lifecycle Matrix & Localized Diagnostics (v1.41.160)

## Zusammenfassung
Das granularisierte "Will Spawn / Has Spawned"-Testsystem ist erfolgreich implementiert. Jede UI-Komponente wird jetzt zentral im Lifecycle-Registry getrackt und kann gezielt auf Integrität geprüft werden.

---

## 1. Granular Spawning Registry
- **ui_core.js:**
  - Einführung von `window.__fragment_lifecycle_registry`.
  - `auditFragmentHydration` erfasst für jede Komponente: will_spawn, loading, success/error.
  - Jeder Eintrag ist mit der physischen Target-ID (Container) verknüpft.

## 2. Lifecycle Hooks
- **fragment_loader.js:**
  - Registry-Hooks sind in die Ladepipeline integriert.
  - `injectLocalizedIntegrityTest(targetId)` schreibt ein Testmuster gezielt in einen Split-Viewport.

## 3. Forensic Matrix UI
- **diagnostics_sidebar.html:**
  - "FRAGMENT LIFECYCLE MATRIX" im HYD-Tab.
  - Jede Zeile repräsentiert ein HTML-Fragment und zeigt den Status (Gelb = Pending, Grün = Ready, Rot = Error).
  - Jede Zeile hat einen eigenen "TEST"-Button.

---

## Nutzung zur Black-Screen-Fehlersuche
1. **Diagnostics Sidebar öffnen** (rotes Herzschlag-Icon).
2. **HYD-Tab wählen** (mittleres Icon).
3. **FRAGMENT LIFECYCLE MATRIX prüfen:**
   - Steht ein Fragment auf WILL SPAWN (gelb), ist der Fetch nicht abgeschlossen.
4. **Lokaler Integritäts-Check:**
   - TEST-Button neben einem Fragment klicken (z.B. player_queue).
   - Ergebnis: "LOCAL INTEGRITY OK" erscheint nur in diesem Sub-Viewport.
   - Wenn sichtbar, ist das Viewport-Rendering intakt, nur das Fragment-Content-Laden schlägt fehl.

---

## Ergebnis
- Die Matrix aktualisiert sich in Echtzeit beim Kategorie-Wechsel (z.B. Music Player → Library Browser).
- Black-Screen-Ursachen können jetzt gezielt und fragmentgenau diagnostiziert werden.

---

**Weitere Forensik- oder Diagnosetools können direkt folgen.**
