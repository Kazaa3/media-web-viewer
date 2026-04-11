# Implementation Plan – Startup to GUI Debugging

## Ziel
Lückenlose, transparente Protokollierung des gesamten App-Startvorgangs – vom Python-Backend bis zur finalen Medienanzeige im DOM. Ziel ist es, exakt zu erkennen, wo Medienitems ggf. verloren gehen.

---

## Proposed Changes

### Backend Startup & Data Pipeline

**[MODIFY] main.py**
- **Early-Stage Trace:**
  - Logge DB-Initialisierungsstatus und Anzahl gefundener Records direkt beim Start.
- **get_library Audit:**
  - Detaillierte `eel.append_debug_log`-Aufrufe:
    - Gesamtzahl der Items.
    - Welche Items gefiltert werden und warum (z.B. "Category 'Audio' not managed").
    - Endgültige Anzahl, die ans Frontend geht.
- **Parser Trigger:**
  - Logge den exakten Befehl, der beim Auto-Scan an den Parser gesendet wird.

---

### Frontend Initialization

**[MODIFY] bibliothek.js**
- **Init Trace:**
  - Logge Start von `loadLibrary()`.
- **Data Arrival Trace:**
  - Logge die rohen Daten, die von `eel.get_library()` empfangen werden.
- **Rendering Block Trace:**
  - Logge Start/Ende von `renderItemGallery()` und `renderLibrary()`, inkl. Anzahl erzeugter DOM-Elemente.

**[MODIFY] audioplayer.js**
- **Gallery Sync Trace:**
  - Logge, wenn die "Mediengalerie" aktualisiert wird und ob das Ziel-Container-Element existiert.

---

## Open Questions
- Soll auch die Liste der gefundenen Dateiendungen im ./media-Ordner geloggt werden, um die Parser-Regex zu prüfen?

---

## Verification Plan

### Manual Verification
- App starten.
- LOGS-Overlay im Footer öffnen.
- Schritt-für-Schritt-Sequenz beobachten:
  - `[BACKEND] DB Initialized: X items`
  - `[BACKEND] get_library called`
  - `[BACKEND] Filtering: Item Y kept (Audio)`
  - `[LIBRARY] Data received: Z items`
  - `[LIBRARY] Rendering Z items in gallery...`
- Prüfen, ob die im Log sichtbaren Items mit der tatsächlichen GUI-Anzeige übereinstimmen.
