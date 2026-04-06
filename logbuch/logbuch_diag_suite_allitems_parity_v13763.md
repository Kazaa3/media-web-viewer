# Logbuch v1.37.63 – Diagnostic Suite: All-Items Expansion & Parity

**Datum:** 2026-04-06

## Stabilisierung & Erweiterungen

### 1. Hybrid Hydration (M/R/B-Toggles)
- **Both-Modus:** App merged 541 echte DB-Items mit 3 legalen Mock-Diagnose-Items (gesamt: 544 Assets).
- **Mock-Assets:** Sine-Wave-MP3s in /media/mock/ mit exakten Längen (Megaloh: 215s, Benjie: 198s, Beginner: 242s).

### 2. Category Consolidation & "All"-Selection
- **All-Items Expansion:** Backend-Resolver akzeptiert jetzt das "all"-Keyword und inkludiert explizit alle internen Labels/Aliase aus dem Master Category Map. Kein Item-Drop mehr bei "Alle"-Auswahl.
- **Multimedia → Video:** "multimedia" entfernt, Legacy-Items werden automatisch auf "video" gemappt.
- **Registry:** displayed_categories in config_master.py enthält jetzt alle unterstützten Typen (all, audio, video, pictures, documents, ...).

### 3. Technical Footer HUD
- **Sync Audit:** Footer zeigt Live-Datenparität [DB: 544 | GUI: 544].
- **Diagnostic Controls:** M/R/B-Toggle und GUI-Refresh-Button für sofortige UI-Rehydrierung integriert.

### 4. Library Explorer Enhancements
- **Filter Parity:** "Bilder" und "Dokumente" als Hauptfilter in der Sidebar wiederhergestellt, Routing-Logik aktualisiert.

## Verifikation
- **Hydration:** _apply_library_filters dropt keine echten Items mehr bei "All" (Kept: 541, Dropped: 0).
- **Paths:** Frontend löst media/mock/*.mp3 korrekt über Eel-Server auf.
- **Filter:** Klick auf "All", "Bilder" oder "Dokumente" triggert die jeweilige Filterung.
- **Status:** "Green LED" – absolute Parität zwischen SQLite-Backend und Chromium-Frontend.

---
**Status:** Diagnostic Suite: All-Items Expansion & Parity erfolgreich implementiert (v1.37.63)
