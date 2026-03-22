# App Startup Optimization & Chrome Connection – März 2026

## Ziel
- Schnellere und reaktionsfähigere App-Initialisierung auf localhost:8345
- Chrome-Startup und UI-Initialisierung priorisieren

## Vorgehen
- Analyse von main.py ergab, dass mehrere ressourcenintensive Tasks (z.B. delayed_scan) vor UI-Start ausgeführt wurden und den Boot-Prozess verzögerten.
- Refaktor geplant: eel.init, eel.start und open_session_url werden an den Anfang des Startup-Prozesses verschoben.
- Nicht-essenzielle Tasks (z.B. delayed_scan, DB-Checks, Medien-Scans) werden erst nach erfolgreicher UI-Verbindung gestartet.

## Fortschritt
- Strukturfixes im UI und Backend-RTT-Logik bereits umgesetzt
- Chrome-Startup-Logik analysiert und optimiert

## Lessons Learned
- Priorisierung von eel.init/start und open_session_url sorgt für schnelleren UI-Launch
- Verzögerte Ausführung von Hintergrundtasks verhindert UI-Lags beim Boot
- Boot-Profiling und Task-Reihenfolge sind entscheidend für User Experience
