# Advanced Parser Robustness Measures & Verification

**Datum:** 12. März 2026

---

## Maßnahmen zur Robustheit

### 1. Timeout Enforcement
- Alle `subprocess.run`-Aufrufe in Parsern enthalten jetzt ein Timeout.

### 2. Data Sanitization
- Extrahierte Metadaten werden validiert und begrenzt:
  - Maximale Kapitelanzahl (z.B. 500).
  - Maximale Tag-Länge (z.B. 4KB).
  - Schutz vor UI-Lags und Speicherproblemen.

### 3. Unicode Resilience
- Alle String-Extraktionen nutzen `decode(errors='replace')`.
- Fehlerhafte/corrupt Strings werden robust behandelt.

### 4. Resource Limits
- Filehandle-Leaks werden durch `try...finally` und Kontextmanager verhindert.
- Alle Dateioperationen sind abgesichert.

### 5. Process Isolation (Phase 2)
- Optionale Auslagerung von Heavy-Parsers (FFmpeg, VLC) in separate Prozesse/Threads.
- Native C-Library-Crashes (Segfaults) killen nicht mehr die Hauptanwendung.

### 6. Magic Byte Verification
- Dateikopf wird vor Parser-Aufruf geprüft.
- Verhindert Fehlaufrufe (z.B. ISO-Parser auf MP3).

### 7. Depth-Limit Tracking
- Rekursionstiefe für Containerstrukturen wird begrenzt.
- Schutz vor "Parser Bombs".

### 8. Semantic Validation
- Ergebnisse verschiedener Parser werden verglichen.
- Bei Diskrepanzen: Warnung oder Confidence-Voting.

---

## Verifikationsplan
- **Automatisierte Tests:**
  - Corruption Test: Parser crasht, nachfolgende Parser erhalten sauberen State.
  - Timeout Test: Hängender Parser, Chain läuft nach Timeout weiter.
  - Process Death Test: Prozessabbruch, Exception wird abgefangen.
- **Manuelle Verifikation:**
  - App starten, Logs beim Parsen "schwieriger" Dateien beobachten.

---

*Entry created: 12. März 2026*
