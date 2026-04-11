# Logbuch v1.37.59 – System Repairs: Port Conflict & Diagnostic Bridge

**Datum:** 2026-04-06

## Zusammenfassung der Reparaturen

### 1. Port Conflict Resolution
- Stale-Prozesse auf Port 8345 wurden entfernt.
- Die Anwendung startet jetzt fehlerfrei, kein OSError (Greenlet failure) mehr.

### 2. Diagnostic Bridge Restoration
- Fehlende Backend-Funktionen (`get_debug_stats`, `get_startup_info`) in main.py implementiert.
- `get_library_forensics` liefert jetzt das vollständige Objekt für die UI.
- Ergebnis: Die Status-Pill [DB: X | GUI: Y] im Footer zeigt jetzt Echtzeit-Zahlen.

### 3. Hydration Toggle Visibility
- Die [M | R | B]-Buttons wurden in den Hauptfooter (neben das DB-Statuslicht) verschoben und sind jetzt sofort sichtbar.
- Hoher Kontrast für Labels sorgt für Lesbarkeit auf dem Glassmorph-Hintergrund.

## Nutzung der neuen Diagnostics
- **Footer:** M, R oder B klicken, um sofort den Hydrationsmodus zu wechseln.
- **Sidebar:** "Health" oder "Debug" öffnen – kein "Audit Bridge Fault" mehr.
- **Pill Audit:** Mittlere Footer-Pill zeigt Live-Zahl der indexierten Items vs. UI-Rendering.

---
**Status:** System synchronisiert, Port-Konflikt und Diagnostic Bridge vollständig behoben (v1.37.59)
