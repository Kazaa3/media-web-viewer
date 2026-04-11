# Logbuch Meilenstein: Erweiterter Stabilisierungs-Plan & VS Code Optik (v1.35.68)

## Geplante Maßnahmen

### 1. VS Code Dark JSON-Style
- Der „Python Dict (Details)“-Viewer erhält echtes Syntax-Highlighting:
  - Blaue Keys, grüne Strings, orange Zahlen
  - Tiefschwarzer Hintergrund für maximale Lesbarkeit

### 2. Player „Zwangs-Hydrierung“
- Im RAW-Modus ignoriert der Player alle internen Filter
- 541 Titel in der DB = 541 Titel in der Queue (keine Verluste mehr möglich)
- .mp3-Dateien werden immer als Audio erkannt, unabhängig vom DB-Eintrag

### 3. Eigener „Diag Flow“-Tab
- Neuer Tab im Optionen-Panel (Zahnrad)
- Zeigt den Live-Status von RAW, BYPS und NATV an
- Kein Öffnen des Modals mehr nötig, um den Diagnose-Status zu sehen

### 4. TEST-Button-Upgrade
- Erweiterung: Zeigt jetzt explizit „Player Queue Integrity: PASS (541/541)“
- Sofortige Rückmeldung über die Integrität der Player-Queue

## Ziel
- „Schwarzes Loch“ im Player und der Queue endgültig schließen
- Modernes, klares UI im VS Code-Stil
- Maximale Transparenz und Kontrolle über alle Diagnose- und Recovery-Mechanismen

---

**Freigabe zur gleichzeitigen Umsetzung: VS Code Optik, Player-Zwangs-Hydrierung & Diag Flow Tab.**
