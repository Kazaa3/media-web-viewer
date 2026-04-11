# Library Hydration & "0-Item" Bug Resolution (v1.37.07)

## Problem Statement
Persistent "0-item" bug traced to fragmented category-mapping (models.py) and a logic error in main.py preventing RAW mode from bypassing filters when search is active.

## Solution Overview
Introduce a robust, multi-stage Hydration Pipeline:
- Centralize all category mappings into a case-insensitive Single Source of Truth (SSOT).
- Add Multi-Stage Diagnostics for RAW and Bypass modes.

---

## Implementation Plan

### 1. Data Models (SSOT Consolidation)
- **models.py**
  - Unify `EXTENSION_REGISTRY` and `MASTER_CAT_MAP` into a `CategoryOrchestrator`.
  - All category keys/values strictly lowercased.
  - German/human-readable categories (e.g., Musik, Filme) mapped to internal English keys at runtime.
  - Update all lookup and aliasing logic to be case-insensitive and comprehensive.

### 2. Backend Filtering & Multi-Stage Hydration
- **main.py**
  - Fix RAW mode: `force_raw` now truly bypasses category filters, even with search/genre/year.
  - Implement multi-stage hydration in `get_library`:
    - **Stage 0:** DB-RAW (literal SQL rows)
    - **Stage 1:** SSOT-NORM (normalized categories)
    - **Stage 2:** CAT-FILTER (filtered by displayed categories)
    - **Stage 3:** FULL-FILTER (production output: search, genre, year)
  - Add `[BD-AUDIT]` logs for each stage, showing item counts and drop reasons.

### 3. Frontend Diagnostics & DOM Debugging
- **js/diagnostics_helpers.js**
  - Add sidebar toggle for Hydration Stages (RAW, NORM, VIEW).
  - Implement DOM Integrity Auditor to check for hidden nodes (e.g., via CSS).
  - Visualize dropped reasons for each stage side-by-side.

---

## Warnings & Behavior Changes
- **Category SSOT Migration:** All internal category names are now strictly lowercase English. Displayed/alias categories (e.g., Musik, Filme) are mapped at runtime. This avoids mismatches from capitalization or language.
- **RAW Mode:** Now truly bypasses category filtering, even if a search term is present. Searching in a "0-item" state will show raw DB matches.

---

## Verification Plan

### Automated Tests
- Stage-by-stage: Stage 1 count ≥ Stage 2.
- RAW mode: `get_library(force_raw=True, search="...")` returns all items if search is empty, or only name matches if not, ignoring categories.
- Casing: Both `audio`, `AUDIO`, and `Musik` in DB hydrate correctly.

### Manual
- Use Diagnostics Sidebar to toggle stages and confirm HUD shows correct filtered counts.
- Run DOM Auditor to verify the media grid node count matches expectations.

---

## Open Question
Should rehydration concepts from the logbuch be moved to `docs/architecture/` for permanence, or remain in the date-stamped logbuch?

_Recommendation: Move finalized concepts to `docs/architecture/` for long-term reference; keep iterative notes in logbuch._
# Walkthrough: Supercharged Diagnostics Sidebar v1.37.05

## Overview
This release finalizes the Global Diagnostics Sidebar and the Footer Navigation Cluster, delivering a comprehensive observability suite to address the persistent "0 item" library bug and provide deep system insight.

---

## Key Features

### 1. Unified Diagnostic Sidebar (Left Overlay)
- **Design:** Semi-transparent glass overlay (`rgba(12, 16, 24, 0.68)`) on the left.
- **Contents:** All technical controls are consolidated here.
- **Internal Navigation:**
  - **Übersicht:** Real-time database overview and category breakdown.
  - **Tests & Benchmarks:** Latency profiling and backend ping tests.
  - **Video Health:** Codec and pipeline diagnostics.
  - **System-Check:** Automated 10-point integrity audit.
  - **Konsole Logs:** Live system logbuch mirroring.
  - **Recovery:** Stage-based nuclear restoration options.

### 2. System Flag Toggles
- **Dedicated toggle buttons** for backend behavior flags:
  - **DIAG:** Activate nuclear recovery visibility.
  - **NATV:** Force native HTML5 playback (bypass transcoding).
  - **HIDB:** Test GUI behavior with empty database mocks.
  - **RAW:** Bypass category mapping for raw file discovery.

### 3. Action Center
- **Immediate recovery commands** available in the sidebar:
  - **MANUAL SYNC:** Trigger a library re-hydration.
  - **DEEP SCAN:** Force a filesystem re-index.
  - **DATA FLOW PROBE:** Trace items through the backend pipeline.

### 4. Footer Console Cluster
- **Diagnostics Toggle:** Heartbeat-styled button in the bottom-right for instant access to the technical overlay.
- **Theme Switcher:** Preserved and aligned next to the diagnostics toggle.

---

## Technical Details
- **Persistence:** Sidebar visibility and active tab are stored in `localStorage`.
- **Sync:** Real-time counts (DB vs GUI) are synchronized across the footer and sidebar status cards.

---

## Troubleshooting: "0-item" Problem
To diagnose the "0-item" issue:
1. Open the Diagnostics Sidebar.
2. Use the **DATA FLOW PROBE**.
3. The probe will highlight how many items were dropped and which filter (Category, Exists, etc.) caused the drop.

---

## Related Diffs
- `web/app.html`: Sidebar and footer cluster markup.
- `web/js/ui_nav_helpers.js`: Navigation logic and state persistence.
- `web/js/diagnostics_helpers.js`: Diagnostics logic, probes, and flag toggles.
- `web/css/main.css`: Styling for sidebar, overlays, and footer cluster.

---

**Version:** 1.37.05
**Date:** 2026-04-06
# Logbuch: Media Viewer Footer UI & Diagnostics Toggle Finalization (v1.37.05)

## Overview
Die Footer-Oberfläche von Media Viewer v1.37.05 wurde finalisiert. Der rechte Footer-Cluster entspricht jetzt der gewünschten visuellen Reihenfolge und integriert den neuen Diagnosezugang für die Analyse des "0-item"-Bibliotheksproblems.

## Finalisierte Footer UI (Right Cluster)
**Referenzdatei:** [web/app.html](web/app.html)

Die Bedienelemente im rechten Cluster wurden in der finalen Anordnung umgesetzt:
- `Theme Toggle` (Sun Icon) bleibt am Anfang des Clusters für Hell-/Dunkelmodus.
- `Program Menu` als runder Hamburger-Button im restaurierten v1.34-Stil.
- `Main Sidebar` / Split-View-Toggle für die Standardnavigation.
- `System Diagnostics` mit Pulse-Icon als schneller Zugang zur technischen Overlay-Diagnostik.

Damit ist der Diagnosezugang direkt im Footer verankert und optisch an die bestehende UI angepasst.

## Neue Diagnosefunktion für das "0-item"-Problem
**Betroffene Bereiche:** [web/app.html](web/app.html), [web/js/ui_nav_helpers.js](web/js/ui_nav_helpers.js), [web/js/diagnostics_helpers.js](web/js/diagnostics_helpers.js), [web/css/main.css](web/css/main.css)

Der neue Pulse-Button öffnet die mehrstufige Diagnostics-Overlay-Ansicht. Diese dient als primäres Werkzeug zur Analyse des Hydration- und Filterproblems in der Bibliothek.

### Enthaltene Debug-Werkzeuge
- **Data Flow Probes**
  - Zeigt, an welcher Stelle Medienobjekte aus der Pipeline herausfallen.
- **Action Center**
  - `Manual Sync` zur Rehydrierung der Bibliothek.
  - `Deep Scan` für einen vollständigen Re-Index des Dateisystems.
- **Observability Parity**
  - Live-Abgleich zwischen Datenbankzeilen und tatsächlich im GUI sichtbaren Einträgen.

## Ergebnis
Die Footer-Navigation ist nun nicht nur optisch finalisiert, sondern auch funktional auf schnelle Diagnose ausgelegt. Der neue Diagnose-Toggle verbessert die Erreichbarkeit der technischen Werkzeuge erheblich und verkürzt den Weg zur Ursachenanalyse des Bibliotheksfehlers.

## Empfohlener Debug-Flow
1. Pulse-Button im Footer anklicken.
2. Diagnostics Overlay öffnen.
3. `Data Flow Probe` ausführen.
4. `Database` vs. `GUI` im Observability-Bereich vergleichen.
5. Falls nötig `Manual Sync` oder `Deep Scan` starten.

## Dokumentationsstatus
- Footer UI v1.37.05 dokumentiert.
- Diagnosezugang im Footer dokumentiert.
- Bezug zur "0-item"-Analyse festgehalten.
- Ergänzend siehe [logbuch/walkthrough_supercharged_diagnostics_sidebar_v13705.md](logbuch/walkthrough_supercharged_diagnostics_sidebar_v13705.md).
