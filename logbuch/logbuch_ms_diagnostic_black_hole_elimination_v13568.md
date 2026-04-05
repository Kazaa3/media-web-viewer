# Logbuch Meilenstein: Diagnostic – Black Hole Elimination (Library Recovery)

## Ziel
Lückenlose Nachverfolgung und Eliminierung von "Black Holes" zwischen Datenbank und GUI, um Medienverluste und Stalls im Library-Flow sichtbar und behebbar zu machen.

## Analyse & Problemstellung
- Medien verschwinden zwischen SQLite-DB und GUI (z.B. DB: 541, GUI: 0).
- Ursache: Eel-Calls können bei instabiler Verbindung oder fehlender Browser-Response hängen bleiben (Stall).
- Filter- und Mapping-Fehler führen zu "Black Holes" im Medienfluss.

## Maßnahmen & Änderungen

### Backend Core (src/core/main.py)
- **Explizites Filter-Logging:** Jede Kategorie-Ablehnung beim Library-Fetch wird geloggt.
- **Payload Audit:** Das exakte JSON-Objekt, das an das Frontend gesendet wird, wird protokolliert.
- **Safety:** progress_update und append_debug_log blockieren den Main-Thread nicht mehr bei Websocket-Problemen (Fire-and-Forget/Env-Check).

### Frontend Library (web/js/bibliothek.js)
- **Incoming Data Audit:** Das rohe media-Array wird sofort nach Empfang geloggt.
- **Filtering Trace:** Loggt, wenn Items durch globale Filter, Mock-vs-Real-Konflikte oder DOM-Fehler verloren gehen.

### UI Bridge (web/js/diagnostics_helpers.js)
- **Sync Status Pill:** Footer zeigt jetzt [DB: N | GUI: M] für sofortige Black-Hole-Erkennung.
- **Render Override:** "Force Render Everything"-Button zum Umgehen aller JS-Filter.

## Verifikation
- **Automatisiert:**
  - scripts/hydrate_db.py + recovery_audit.py prüfen, ob alle Items korrekt gezählt und übertragen werden.
  - JSON-Schema-Check: Backend-Kategorien müssen mit CATEGORY_MAP im Frontend übereinstimmen.
- **Manuell:**
  - Nach SCAN/SYNC zeigt die Konsole detailliert, warum Items (nicht) angezeigt werden.

## Ergebnis
- Black Holes im Medienfluss werden sofort sichtbar und nachvollziehbar.
- Stalls durch Eel/Websocket-Probleme werden verhindert.
- Recovery- und Diagnose-Transparenz auf höchstem Niveau.

---

**Meilenstein abgeschlossen: Diagnostic Black Hole Elimination (Library Recovery).**
