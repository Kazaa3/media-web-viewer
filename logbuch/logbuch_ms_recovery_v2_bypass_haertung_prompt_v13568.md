# Logbuch Meilenstein: Recovery v2 – Bypass-Härtung & Aktions-Prompt (v1.35.68)

## Ziel
Finale Härtung des Recovery- und Diagnose-Systems, um den „Schwarzen-Loch-Schutz“ auf die Warteschlange (Queue) auszuweiten und die Wiederherstellung der echten Datenbank zu automatisieren.

## Maßnahmen & geplante Änderungen

### 1. Bypass-Modus-Härtung (BYPS)
- Sicherstellung, dass die Test-Mocks immer erscheinen, wenn BYPS aktiv ist – unabhängig vom Zustand der echten Datenbank.
- Die GUI bleibt so jederzeit testbar, auch bei leerer DB.

### 2. Aktions-Audit für RAW
- Wenn RAW aktiviert wird und 0 Ergebnisse erscheinen, zeigt die Warnbox jetzt einen direkten „SCAN STARTEN“-Button.
- Damit kann der User sofort einen neuen Deep-Scan anstoßen, um die 541 Titel aus ./media zurückzuholen.

### 3. Persistenz der Diagnose-Einstellungen
- Alle Diagnose-Toggles (RAW, BYPS, NATV) bleiben nach einem Refresh erhalten.
- Erhöht die Effizienz beim Debugging und Testen.

## Ergebnis
- BYPS funktioniert als „Proof of Health“ für die GUI-Engine.
- Die Recovery-Logik ist maximal robust und benutzerfreundlich.
- Die Wiederherstellung der 541 Titel aus ./media ist mit einem Klick möglich.

---

**Freigabe zur Umsetzung: Recovery v2 – Bypass-Härtung & Aktions-Prompt.**
