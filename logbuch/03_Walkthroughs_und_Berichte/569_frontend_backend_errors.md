# Logbuch: Fehleranalyse – Log Level, cats, showToast

## Datum
16. März 2026

## Übersicht
Dieser Logbuch-Eintrag dokumentiert die Analyse und Lösungsvorschläge für die aktuellen Fehler im Frontend und Backend.

Hinweis: Der Modus "hybrid" in der GUI soll künftig exakt benannt werden, z.B. "ffmpeg mit cvlc", "mkvmerge mit cvlc" usw., damit die Backend-Kombination transparent und nachvollziehbar ist.

---

## Fehler & Lösungen

### 1. Log Level im Optionen-Tab
- Problem: Nur 2 von 4 Log-Level-Stufen funktionieren.
- Analyse: Backend und Frontend unterstützen DEBUG, INFO, WARNING, ERROR. Handler-Update oder Level-Mismatch möglich.
- Lösung: Handler-Update prüfen, ggf. weitere Level (z.B. CRITICAL) ergänzen.
- Test: Alle Log-Level im Dropdown auswählen und Log-Ausgabe prüfen.

### 2. cats is not defined (Startup)
- Problem: cats wird im Frontend referenziert, ist aber nicht initialisiert.
- Lösung: cats vor Nutzung definieren oder Default-Wert setzen.
- Test: App neu laden, kein Popup-Fehler zu cats.

### 3. VLC pipe: showToast is not defined
- Problem: showToast wird aufgerufen, ist aber nicht global definiert.
- Lösung: showToast global definieren oder Existenz prüfen (typeof showToast === 'function').
- Test: VLC pipe Fallback auslösen, Toast erscheint ohne Fehler.

---

## Tests
- Log-Level: Dropdown-Test, Log-Ausgabe prüfen.
- cats: App-Reload, kein Fehler.
- showToast: VLC pipe Fallback, Toast erscheint.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe walkthrough.md für vollständige Details und Proof of Work.*
