# Logbuch: Startup Monitoring & Bottleneck Detection (Media Viewer v1.35.68)

## Analyse der Startzeit-Bottlenecks

Nach eingehender Analyse des Startvorgangs wurden zwei Hauptengpässe identifiziert:

1. **Binary Discovery**  
   In `config_master.py` werden ca. 46 blockierende Subprozessaufrufe (z.B. für ffmpeg, vlc, etc.) zur Versionsprüfung durchgeführt. Dies verzögert den Start um 5–10 Sekunden.

2. **Netzwerkscans**  
   Die Prozessbereinigung nutzt `psutil.net_connections()`, was auf manchen Linux-Systemen sehr langsam ist.

---

## Umsetzungsplan

### Zielsetzung
Implementierung eines umfassenden Startup-Profilings und eines „Window Heartbeat“-Mechanismus zur Überwachung der UI-Reaktionsfähigkeit.

### Kernelemente

- **Startup Profiler**  
  Neue Engine zur millisekundengenauen Messung aller Bootphasen.

- **Lazy Versioning**  
  Die 46 Subprozessaufrufe werden in einen Hintergrundtask ausgelagert, sodass das Fenster sofort erscheint. Versionsinfos sind initial ggf. „Unknown“.

- **Window Heartbeat**  
  Pulsmechanismus zur Erkennung von UI-Freezes oder Hängern.

- **Diagnostic Dashboard**  
  Neue UI-Ansicht zur Visualisierung der Engpässe.

---

## Vorgeschlagene Änderungen

### Backend

- **startup_monitor.py**  
  Neue `StartupProfiler`-Klasse zur Zeitmessung und API-Bereitstellung.

- **main.py**  
  - Profiler initialisieren (ganz oben).
  - Heartbeat-System via `@eel.expose`.
  - Diagnostics-API: `get_startup_report()`.
  - Window-Watchdog mit Heartbeat-Daten.

- **config_master.py**  
  - Lazy Loading/Caching für `get_binary_version`.
  - Profiler-Instrumentierung für `GLOBAL_CONFIG`.

- **process_manager.py**  
  - Optimierung von `kill_by_port` (gezieltere Scans).
  - Zeitmessung für `kill_stale_instances`.

### Frontend

- **JS/CSS/HTML**  
  - Heartbeat-Interval zur Backend-Kommunikation.
  - Startup-Dashboard zur Visualisierung der Profiler-Daten.
  - Farbige Statusanzeigen für langsame Phasen (>2s).

---

## Verifizierungsplan

- **Automatisierte Tests**  
  - `startup_monitor.py` standalone testen.
  - [PROFILER]-Einträge im Log prüfen.

- **Manuelle Verifikation**  
  - App starten, Dashboard öffnen.
  - Prüfen, ob „Config Initialization“ und „Process Cleanup“ beschleunigt wurden.
  - Hänger simulieren (z.B. `time.sleep` im Frontend) und prüfen, ob ein „Heartbeat Miss“ geloggt wird.

---

**Review erforderlich:**  
Bitte den Plan prüfen. Nach Freigabe beginne ich mit der Implementierung der Monitoring- und Optimierungsmaßnahmen.

---
