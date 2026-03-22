# 04 Frontend Orchestration: Events & i18n

**Datum:** 13.03.2026
**Kategorie:** Frontend, Architektur
**Status:** ARCHIVED

---

## UI-Event-Loop & Tab-Management

Das Frontend von "dict" ist mehr als nur ein schönes Gesicht. Es ist ein dynamischer Orchestrator, der komplexe Zustände zwischen Backend und Browser synchronisiert.

### Kern-Mechanismen
1.  **UI-Event-Loop:** Alle Aktionen im UI (Play, Pause, Scan, Search) werden über ein zentrales Event-Handling-System geleitet, anstatt über verstreute Funktionen.
2.  **Tab-Management:** Der `switchTab` Mechanismus ermöglicht einen nahtlosen Wechsel zwischen Video, Logbuch und Tests, während der Player im Hintergrund (Bottle) weiterläuft.
3.  **UI Trace & Telemetrie:** Wir haben `ui_trace` direkt in das Frontend integriert, um jeden JS-Fehler sofort an das Python-Backend zu melden.

### Internationalisierung (i18n)
Wir haben ein flexibles Lokalisierungs-System implementiert, das Metadaten und UI-Labels übersetzt, ohne das JS-Domanalyse-System zu brechen. Dies ermöglicht es uns, die gesamte Anwendung zweisprachig (DE/EN) anzubieten.

---

**Kommentar:**
Dieses tabulierte Event-System sorgt für die "Desktop-App" Haptik, obwohl "dict" eigentlich eine Browser-App ist.
