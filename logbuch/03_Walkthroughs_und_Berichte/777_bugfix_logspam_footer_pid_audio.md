# Logbuch: Buganalyse und Fix-Plan – 20. März 2026

## Zusammenfassung
Im Rahmen der UI- und Backend-Überarbeitung wurden mehrere Fehlerquellen identifiziert, die die Stabilität und Nutzbarkeit der Anwendung beeinträchtigten. Nachfolgend die wichtigsten Findings und der geplante Lösungsweg.

---

## Identifizierte Probleme

**1. Log Spam (Rekursion):**
- Problem: Ein Rekursions-Loop, bei dem `ui_trace` (Backend) eine Log-Nachricht erzeugt, die von `UIHandler` aufgenommen und per `appendUiTrace` an das Frontend gesendet wird. Das Frontend ruft dann erneut `ui_trace` auf, was zu endlosem Log-Spam führen kann.

**2. Fehlender Footer:**
- Problem: Die Statusleiste `#app-bottom-bar` wurde versehentlich in das (standardmäßig versteckte) Modal `#about-imprint-modal` verschoben und war dadurch nicht mehr sichtbar.

**3. Leere UI-Felder:**
- Problem: Die Variable `BROWSER_PID` wurde im Backend nicht korrekt in die Environment-Info aufgenommen oder aktualisiert, sodass sie im Frontend leer blieb.

**4. Fehlende Audio-Objekte:**
- Problem: Potenzieller Casing-Mismatch bei Kategorien – die Datenbank verwendet "Audio", das Frontend erwartet aber "audio" (Kleinschreibung).

---

## Implementation Plan
1. **Log-Spam-Fix:**
   - Rekursive Logik in `src/core/logger.py` und `main.py` unterbrechen, sodass `ui_trace`-Nachrichten nicht erneut ins Backend gelangen.
2. **Footer-Restaurierung:**
   - `#app-bottom-bar` aus dem Modal herauslösen und wieder als festen Footer im Hauptlayout einbinden.
3. **UI-Felder fixen:**
   - Sicherstellen, dass `BROWSER_PID` im Backend korrekt gesetzt und an das Frontend übergeben wird.
4. **Audio-Kategorien normalisieren:**
   - Kategorie-Casing im Backend und Frontend vereinheitlichen (z.B. überall `.lower()` nutzen).

---

## Nächste Schritte
- Umsetzung der oben genannten Fixes in den jeweiligen Modulen.
- Nach jedem Fix gezielte Tests (UI, Log, Scan, Systeminfo).
- Dokumentation der Änderungen im Logbuch und ggf. in der Entwicklerdoku.

---

*Logbuch-Eintrag erstellt: 20. März 2026*