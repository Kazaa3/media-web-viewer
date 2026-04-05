# Logbuch Meilenstein: Recovery – Autonomous Sync-Audit & Self-Test (v1.35.68)

## Ziel
Ablösung schwergewichtiger Selenium/Playwright-Tests durch eine interne, autonome Self-Test-Suite, die mit dem Sync-Anker sofort die Datenintegrität prüft und Black Holes erkennt.

## Maßnahmen & geplante Änderungen

### 1. Self-Audit Button (TEST)
- Neuer Button TEST im Footer.
- Führt einen 7-Punkte-Integritätscheck des lokalen Datenflusses durch:
  1. Parity Audit (DB-Count vs. GUI-Count)
  2. Category Audit (Kategorien korrekt gemappt?)
  3. Path Audit (Alle Items mit gültigem Pfad?)
  4. Bypass Switch Audit (Zeigt BYPS die Mocks?)
  5-7. (Platz für weitere Checks, z.B. Filter, Playback, Queue)
- Popup zeigt das Ergebnis (z.B. PASS: 4/4 Checks).

### 2. Sync Watchdog
- Hintergrundprozess prüft alle 30 Sekunden die Parität [DB: X | GUI: X].
- Bei Black Hole (z.B. DB: 541 | GUI: 0) wird die Sync-Light im Footer rot und eine Warnung ausgegeben.

### 3. Maintenance Tool (scripts/seed_test_data.py)
- Neues Skript, das die DB mit 541 Dummy-Items befüllt, falls sie leer ist.
- Erlaubt permanente Tests ohne echten Medienscan.

## Verifikation
- TEST-Button klicken → Popup zeigt Integritätsstatus.
- RAW toggeln → TEST-Ergebnis aktualisiert sich.
- DB leeren → Watchdog erkennt Black Hole, Footer-Light wird rot.
- TEST erklärt [DB: 0 | GUI: 0] Zustand verständlich.

## Ergebnis
- Permanente, autonome Integritätsprüfung ohne externe Test-Frameworks.
- Black Holes werden sofort erkannt und erklärt.
- Datenfluss und Diagnose sind maximal robust und transparent.

---

**Meilenstein abgeschlossen: Recovery – Autonomous Sync-Audit & Self-Test.**
