# Implementation Plan – Startup UI Audit Integration (v1.34)

## Ziel
Automatisierte UI-Audits werden beim Start mit --debug-Flag ausgeführt, um die Integrität aller Haupt-Tabs und Fragmente zu prüfen. Die Ergebnisse werden im Backend-Log und als Markdown-Report dokumentiert.

---

## Proposed Changes

### [Scripts] Audit Logic Synchronization

**[MODIFY] app_audit_playwright.py**
- **ID Alignment:**
  - Aktualisiere `tabs_to_audit` auf die neuen v1.34-IDs:
    - player → #player-tab-split-container
    - library → #lib-split-container
    - video → #player-main-content-pane
    - debug → #diagnostics-suite-fragment
    - logbuch → #logbook-fragment
    - reporting → #reporting-main-split-container
- **Dynamic Session Support:**
  - Füge ein `--url` Argument hinzu, um den laufenden Dev-Server zu prüfen (statt managed_session.py zu starten).

---

### [Backend] Startup Orchestration

**[MODIFY] main.py**
- **Audit Detached Thread:**
  - Implemetiere einen Hintergrund-Thread in `start_app()`, der:
    - Auf `spawn_event` wartet (Frontend bereit).
    - `python scripts/app_audit_playwright.py --url http://localhost:8345/app.html` aufruft.
    - Die Audit-Ausgabe an den Backend-Logger weiterleitet (`[System-Audit]`).

---

## Verification Plan

### Automated Verification
- **Launch:** `python3 src/core/main.py --debug`
- **Logs:** Terminalausgaben prüfen:
  - `[System-Audit] Launching Playwright UI Audit...`
  - `[System-Audit] [PASS] Tab: player`
  - `[System-Audit] Audit complete. Report: scripts/audit_reports/audit_report.md`

### Manual Verification
- **Markdown-Report:** `scripts/audit_reports/audit_report.md` inspizieren.
- **Screenshots:** `scripts/audit_reports/screenshots/` prüfen (Duo-View Layout sichtbar).

---

**User Review Required:**
- Das Audit läuft im Hintergrund und blockiert den App-Start nicht.
- Fehlende playwright-Installation wird geloggt, aber führt nicht zum Abbruch.
- Ergebnisse werden im Backend-Log und als Markdown-Report dokumentiert.
