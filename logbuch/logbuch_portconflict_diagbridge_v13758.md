# Logbuch v1.37.58 – Port Conflict & Diagnostic Bridge Repair

**Datum:** 2026-04-06

## Ziel
Behebung des Port-8345-Konflikts, Reparatur der Audit Bridge ("undefined or null"-Fehler) und Sicherstellung der Sichtbarkeit der Hydration-Toggles im Footer.

## Maßnahmen & Änderungen

### 1. Process Management
- **Port-Freigabe:**
  - Zombie-Prozesse auf Port 8345 werden mit einem Kill-Command entfernt, damit die App fehlerfrei starten kann.

### 2. Frontend (UI Restoration & Visibility)
- **app.html**
  - Relocation: hud-hydr-Diagnosegruppe im Footer neu positioniert, damit sie nicht von anderen Elementen überdeckt wird.
  - Visual Stubs: M, R, B-Buttons erhalten kontrastreiche Styles für bessere Sichtbarkeit und Bedienbarkeit.

### 3. Backend (Diagnostic Bridges)
- **main.py**
  - Robustheit: `get_library_forensics` und `get_library_stats` liefern immer ein valides JSON, auch bei leerer oder im Umbau befindlicher DB. "Cannot convert undefined or null to object"-Fehler wird so behoben.

## Verifikation
- **Manuell:**
  - Boot: App startet ohne OSError: [Errno 98].
  - Footer: [DB: -- | GUI: --] zeigt echte Zahlen, keine leeren Felder mehr.
  - Toggle: [M | R | B] Buttons sind sichtbar und funktionieren.

---
**Status:** Port-Konflikt und Diagnostic Bridge erfolgreich behoben (v1.37.58)
