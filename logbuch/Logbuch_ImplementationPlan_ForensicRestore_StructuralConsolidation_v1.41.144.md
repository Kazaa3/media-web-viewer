# Implementation Plan – Forensic Restore & Structural Consolidation (v1.41.144)

## Ziel
Übergang von der "Nuclear Recovery"-Phase zur gezielten Reparatur und Konsolidierung der GUI. Die Diagnostik-Suite wird wiederhergestellt, doppelte Header entfernt und die Workstation-Ästhetik wiederhergestellt.

---

## 1. LOGIC REPAIR (JS)
- **[MODIFY] diagnostics_helpers.js**
  - Restore `renderLogicAuditSummary`: Funktion neu implementieren, um die `logic_audit`-Metriken im Diagnostics-Panel anzuzeigen (behebt ReferenceError).
  - Deduplicate Exports: Alle window-Exports korrekt auf existierende Funktionen mappen.
- **[MODIFY] gui_diagnostics.js**
  - Implementiere `getState()`: Neue Methode im `MWV_Diagnostics`-Modul, die den aktuellen Monitoring-Status zurückgibt (behebt TypeError im Console-Log).

## 2. STRUCTURAL INTEGRITY (DOM)
- **[MODIFY] app.html**
  - Header Deduplication: Die beiden `primary-cluster`-Blöcke zu einem einzigen zusammenführen.
  - Logo Cleanup: Redundante `header-center-title` und überlappende Logos entfernen, um das Layout zu bereinigen.
  - Recovery Integration: [FLASH] und [RECOVER] Buttons elegant in die neue, einheitliche `primary-cluster` integrieren.

---

## 3. Forensic Console
- Die Forensic Console bleibt nach dem Fix togglable über den [RECOVER]-Button.

---

## Verification Plan
- **Manual Verification (Browser):**
  - Console Check: Nach dem Refresh ist die Forensic Console leer (keine roten Fehler).
  - Sub-Nav Check: Das Level 2 Menü (Status-Tabs: Gesundheit, Boot Log, etc.) ist sichtbar und befüllt.
  - Layout Check: Der Header ist eine einzige, saubere Leiste ohne überlappende Texte oder Logos.

---

**Review erforderlich vor Umsetzung!**
