# Fix: Backend-Logs erscheinen jetzt in der GUI-Konsole

**Datum:** 14.03.2026

## Analyse & Ursachen
- **Modul-Duplizierung:** Unterschiedliche Import-Styles (z. B. `import logger` vs. `import src.core.logger`) führten dazu, dass das Logger-Modul doppelt geladen wurde. Der Logbuffer wurde in einer Instanz gefüllt, die GUI-API (`get_konsole`) fragte aber eine zweite, leere Instanz ab.
- **Timing der Initialisierung:** Einige wichtige Startup-Logs wurden erzeugt, bevor das Logging-System vollständig initialisiert war.

## Durchgeführte Fixes
- **Import-Vereinheitlichung:** Alle Importe im Projekt (insbesondere in `main.py` und den Parsern) wurden auf den absoluten Pfad `src.core.logger` umgestellt. Dadurch nutzen alle Komponenten denselben globalen Log-Buffer.
- **Frühere Initialisierung:** Der Aufruf von `initialize_debug_flags()` in der `main.py` wurde an den Anfang der Datei verschoben. Damit werden jetzt auch frühe Umgebungs- und Datenbank-Logs erfasst.
- **GUI Auto-Refresh:** In der `app.html` wurde eine automatische Aktualisierung implementiert. Ist der "Debug & DB"-Tab aktiv, werden die Logs alle 2 Sekunden vom Backend abgefragt, inklusive Auto-Scroll (nur wenn man am unteren Ende der Liste ist).

## Ergebnis
- Die GUI-Konsole zeigt jetzt exakt die gleiche Log-Ausgabe wie das Terminal – vom ersten Einschalten des Loggings bis zu den UI-Traces.

---

**Hinweis:**
Das Programm kann jetzt gestartet werden, um die vollständige Log-Ausgabe im Debug-Tab zu verifizieren.
