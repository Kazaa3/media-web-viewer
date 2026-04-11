# Logbuch Meilenstein: Permanente Test-Suite & Erklär-Popups (v1.35.68)

## Verbesserungen & neue Features

### 1. Ausführliche Erklär-Popups
- Alle Schalter zeigen jetzt Klartext-Medaillons statt Abkürzungen:
  - DIAG: „Nuclear Recovery Mode (S1-S15 Stages) AKTIVIERT“
  - NATV: „Native HTML5 Engine (Kein Transcoding) AKTIVIERT“
  - HIDB: „Datenbank-Einträge ausgeblendet (Nur Mocks) AKTIVIERT“
  - RAW: „Rohdaten-Modus (Kategorie-Filter deaktiviert) AKTIVIERT“
  - BYPS: „DB-Bypass (Nur Test-Mocks aktiv) AKTIVIERT“

### 2. RAW-Button (Kategorie-Bypass)
- Aktiviert: Backend liefert alle 541 Einträge ungefiltert an das Frontend.
- Sofortige Diagnose, ob das Problem am Backend-Mapping oder an Frontend-Filtern liegt.

### 3. BYPS-Button (DB-Bypass)
- Trennt die Verbindung zur Datenbank und lädt nur hochwertige Mocks.
- Beweis, dass die GUI-Engine unabhängig von der DB funktioniert.

### 4. Unifiziertes Backend Mapping
- Alle Mapping- und Filter-Logiken in main.py in eine zentrale Funktion überführt.
- Keine widersprüchlichen Filter mehr möglich.

### 5. Audio-Queue Fix & Sync-Audit
- Filter in audioplayer.js entschärft.
- Neues Sync-Audit im Web-Log: „X Audio-Items übernommen, Y Items abgelehnt“.

## Empfehlung & Test
- RAW im Footer aktivieren:
  - Springt die Liste auf 541 Titel → Problem lag am Kategorie-Mapping.
  - Bleibt die Liste bei 0 → Frontend-Filter (Suche/Genre) ist die Ursache.
- Queue-Status prüfen: Erscheinen die Titel nach RAW?

## Ergebnis
- Permanente Test-Suite und Diagnose-Tools ermöglichen jederzeit reproduzierbare Fehleranalyse.
- Die „0 Items“-Problematik ist nachhaltig und transparent debugbar.

---

**Meilenstein abgeschlossen: Permanente Test-Suite & Erklär-Popups.**
