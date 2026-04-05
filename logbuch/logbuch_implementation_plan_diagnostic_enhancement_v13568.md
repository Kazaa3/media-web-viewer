# Logbuch: Implementation Plan – Diagnostic Suite Enhancement (v1.35.68)

## Key Improvements
- **JSON Deep-Probe:**
  - Dropdown zum Umschalten zwischen Library (Live), Active Config, Parser Mappings, System Environment und Format Utils (Extensions).
- **Console Controls:**
  - Log Level Selector: Echtzeit-Filterung nach DEBUG, INFO, WARN, ERROR.
  - Text Filter: Live-Suchfeld für gezielte Stichworte (z.B. Dateinamen, PIDs).
  - Live Counter: Anzeige von Sichtbar / Gesamtanzahl der Logzeilen.

## Umsetzungsschritte
1. **Frontend:**
   - Erweiterung des Diagnostic Hubs im Options-Panel um die neue JSON-Dropdown-Auswahl und die erweiterten Logfilter.
   - Implementierung eines Live-Counters und eines Suchfelds für die Log-Konsole.
2. **Backend:**
   - Sicherstellen, dass alle relevanten Datenquellen (Config, Parser, Env, Extensions) für die Dropdown-Auswahl bereitgestellt werden.
   - Log-API so erweitern, dass Filter und Level dynamisch unterstützt werden.

## Status
- **Plan erstellt:** Siehe implementation_plan_diagnostic_enhancement.md für Details.
- **Warten auf:** User-Feedback und ggf. weitere Wünsche zu den Logfiltern.

## Nächste Schritte
- Nach Freigabe: Umsetzung der UI- und Backend-Erweiterungen gemäß Plan.
