# Branch-Aware Build Bridge & Identity Restoration (v1.45.200)

## Zielsetzung
Die festen Entwicklungszweige (media, library, database) werden technisch mit dem Build-Prozess verknüpft. Die architektonische Identität (BRANCH_MAP) wird als SSOT-konforme Registry wiederhergestellt.

---

## Änderungen & Komponenten

**[Component] CONFIG: BUILD & IDENTITY SSOT**
- **config_master.py**
    - Einführung von `BRANCH_IDENTITY_REGISTRY`: Verknüpft Branch-IDs mit Klarnamen und Build-IDs.
    - Einführung von `BUILD_ORCHESTRATION`: Logik zur Ermittlung des Build-Links (z.B. ./dist/MWV-{{BRANCH_NAME}}.exe).

**[Component] MODELS: IDENTITY BRIDGE**
- **models.py**
    - Re-Implementierung von BRANCH_MAP als abgeleitete Property aus config_master.py.
    - Jede Logik, die den Klarnamen eines Branches benötigt (z.B. für Build-Skripte oder UI), nutzt diese zentrale Registry.

**[Component] CORE: PLAYLIST DIVERSIFICATION**
- **main.py**
    - Sicherstellen, dass _apply_library_filters für den library-Branch (Multimedia) gemischte Playlisten (Audio/Video) erlaubt.
    - Im database-Branch werden Playlisten auf video_iso und epub fokussiert.

---

## Entscheidungsnotiz
- "Build Link" wird sowohl als technische Mapping (für Build-Skripte) als auch als Metadatenfeld für die UI implementiert.

---

## Verifikationsplan
- **Automatisierte Tests:**
    - Branch Identity Check: models.get_branch_label('media') liefert die korrekte Identität (z.B. "AUDIO").
    - Build Link Resolution: Der Build-Pfad wird für jeden Branch korrekt generiert.
- **Manuelle Prüfung:**
    - BOOT-Tab/HUD zeigt die neue Branch-Identität korrekt an.

---

**Status:**
- Version: v1.45.200 (Planung)
- Warten auf Freigabe der Build-Integration.
