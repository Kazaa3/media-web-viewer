# Logbuch v1.37.50 – Multi-Stage Bypass & Category Refactor

**Datum:** 2026-04-06

## Ziel
Implementierung eines 4-stufigen Bypass-(Mock)-Systems, Abschluss des multimedia→video-Refactors und Stabilisierung der Umgebung (Port-Freigabe).

## Maßnahmen & Änderungen

### 1. Model & Data Refactor (SSOT)
- **models.py**
  - MASTER_CAT_MAP und BRANCH_MAP: "multimedia" durch "video" ersetzt.
  - Alias-Logik: "multimedia" ist jetzt reiner App-Mode, nicht mehr Kategorie-Mapping.
- **db.py**
  - Migration: Alle "multimedia"-Kategorien in der DB werden zu "video" umbenannt.
  - API: `get_library = get_all_media` für Kompatibilität.

### 2. Multi-Stage Bypass System
- **main.py**
  - `get_library_forensics`: Diagnostik-Bridge wiederhergestellt, Overlay-Fehler behoben.
  - `get_library`-Stages:
    - **Stage 1 (Hardcoded):** 3 Minimal-Mocks für Connectivity-Test.
    - **Stage 2 (Playable):** Mocks mit echten Pfaden aus ./media, um Playback-Engine ohne DB zu testen.
    - **Stage 3 (Realistic):** Vollständig normalisierte Mock-Objekte (inkl. Artwork) für UI-Layout-Tests.
  - Settings: Konfigurierbare Umschaltung zwischen den Stages im Bypass-Modus.

### 3. UI Alignment & Fixes
- **audioplayer.js**
  - "Liste leeren": clearQueue repariert, Queue wird zuverlässig geleert.
  - Video-Logik: Filter auf neues "video"-Label abgestimmt.

### 4. Environment Stabilization
- **Port-Freigabe:** "Super Kill" für Port 8345, um Startprobleme zu vermeiden.

## Offene Frage
- Sollen für Stage 2 (Playable Mocks) automatisch die ersten drei verfügbaren Dateien aus ./media gewählt werden, unabhängig vom Format? (**Vorschlag:** Ja, für maximale Testabdeckung.)

## Verifikation
- **Automatisiert:**
  - eel.get_library(audit_stage=X) liefert für Stages 1–3 die erwarteten Mock-Strukturen.
- **Manuell:**
  - Diagnostics Overlay zeigt korrekten DB-Status und Mock-Stage.
  - "Liste leeren" leert die Player-Queue zuverlässig.

---
**Status:** Multi-Stage-Bypass, Kategorie-Refactor und Port-Stabilisierung dokumentiert (v1.37.50)
