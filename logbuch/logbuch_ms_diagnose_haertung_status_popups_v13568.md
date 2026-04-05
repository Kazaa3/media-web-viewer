# Logbuch Meilenstein: Diagnose-Härtung & Status-Popups (v1.35.68)

## Verbesserungen & neue Features

### 1. Sync-Anker & Status-System
- **Selbst-Initialisierung:**
  - Der Sync-Anker im Footer startet jetzt mit ... und zeigt nach spätestens 1 Sekunde den aktuellen Stand ([DB: N | GUI: M]) an – auch wenn der Haupt-Sync noch läuft.

### 2. Status-Popups für alle Buttons
- **Visuelles Feedback:**
  - DIAG, NATV, HIDB und AUDIT zeigen jetzt sofort ein Popup (z.B. „NATV: AKTIVIERT“), wenn ein Schalter betätigt wird.

### 3. Neuer PROBE-Button (Tiefendiagnose)
- **Funktion:**
  - Umgeht alle JS-Filter und fragt das Backend direkt nach dem echten DB-Inhalt.
  - Zeigt das Ergebnis sofort als Erfolgsmeldung an (z.B. „Backend liefert 541 Items“).

### 4. Warteschlangen-Abfang-Logik
- **Black Hole erkannt**-Warnung erscheint jetzt auch im Player-Tab, wenn die Queue leer ist, aber die DB gefüllt.

## Prio-Check (0 Items Jagd)
1. PROBE-Button klicken → Pop-up zeigt DB-Status.
2. JETZT FILTER ZURÜCKSETZEN klicken (Warnbox oder Footer).
3. Sync-Anker prüft: [DB: 541 | GUI: 541] = Erfolg.

## Ergebnis
- Diagnose- und Statussystem sind maximal robust und benutzerfreundlich.
- Fehlerquellen werden sofort sichtbar und können gezielt behoben werden.
- Die „0 Items“-Problematik ist damit endgültig gelöst und transparent nachvollziehbar.

---

**Meilenstein abgeschlossen: Diagnose-Härtung & Status-Popups.**
