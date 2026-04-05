# Logbuch Meilenstein: Hide DB Toggle & Fehler-Abfang-Logik (v1.35.68)

## Geplante Features

### 1. "Hide DB"-Toggle (HIDB)
- Neuer Button im Footer Admin-Cluster.
- Ermöglicht das Aus- und Einblenden der echten Datenbank-Einträge.
- Ziel: Testen, ob die GUI korrekt mit Mocks/virtuellen Items umgehen kann, wenn die DB ausgeblendet ist.

### 2. Fehler-Abfang-Logik ("Abfangen")
- Intelligente Diagnose-Warnung anstelle von "Keine Medien gefunden".
- Wenn z.B. 541 Items im Speicher sind, aber 0 angezeigt werden, erscheint:
  - "Achtung: Es sind 541 Medien geladen, aber sie werden durch Filter blockiert. Klicke auf RESET FILTERS."
- Ziel: Sofortige Sichtbarkeit, ob Filter die Anzeige verhindern.

### 3. Audit-Sync
- Der "Hide DB"-Toggle ist direkt mit dem Sync-Anker ([DB: N | GUI: M]) verknüpft.
- Statusänderungen werden sofort im Anker angezeigt.

## Umsetzung
- Anpassungen in app.html, diagnostics_helpers.js und bibliothek.js geplant.
- Ziel: Maximale Transparenz und schnelle Fehlerdiagnose im UI.

---

**Freigabe zur Umsetzung: Hide DB Toggle & Fehler-Abfang-Logik.**
