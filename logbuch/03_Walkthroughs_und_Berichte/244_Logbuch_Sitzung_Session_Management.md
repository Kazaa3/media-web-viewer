# Logbuch: Sitzung / Session Management

## Zweck
Dokumentiert die Funktionsweise, Implementierung und Testfälle zur Sitzungs-/Session-Verwaltung im Media Web Viewer.

---

## Architektur & Ablauf
- Sitzungen werden durch laufende Prozesse (PID) und TCP-Ports identifiziert.
- Die Funktion `check_running_sessions()` (main.py) scannt alle laufenden Instanzen:
    - Ermittelt PID, Port und Kommandozeile.
    - Nutzt `psutil` für Prozess- und Netzwerk-Analyse.
- Mehrere parallele Sitzungen werden erkannt und können gezielt verwaltet oder beendet werden.

---

## Use Cases
- Debugging: Übersicht aller laufenden Sessions für Fehleranalyse.
- Testumgebungen: Sicherstellung, dass Test- und Produktionsinstanzen getrennt laufen.
- Monitoring: Automatisierte Überwachung und Reporting aktiver Sitzungen.

---

## Beispiel-Ausgabe
| PID  | Port | Kommandozeile           |
|------|------|------------------------|
| 1234 | 8080 | python main.py --ng    |
| 2345 | 8090 | python main.py         |

---

## Testfälle
- Start mehrerer Instanzen, Prüfung ob alle korrekt erkannt werden.
- Beenden einer Instanz, Prüfung ob Session-Liste aktualisiert wird.
- Fehlerhafte/abgebrochene Prozesse werden nicht als aktive Sitzung gelistet.

---

## Hinweise
- Sitzungsmanagement ist zentral für parallele Entwicklung, Debugging und CI/CD.
- Erweiterbar für User-Session-Tracking (Frontend/Backend).

---

## Referenzen
- main.py: `check_running_sessions()`
- Dokumentation: Abschnitt "Session Management"
- API: Keine direkte API-Expose, aber Debug- und Monitoring-Tools nutzen die Funktion.

---

## TODO
- Erweiterung für User-Session-Tracking (Frontend)
- Automatisierte Session-Reports im Logging-System
- Integration in CI/CD-Testpipeline
