# Fast Boot & UI Priority Plan – März 2026

## Ziel
- Nahezu sofortiger App-Start durch Priorisierung von Eel-Server und Chromium-Verbindung vor schweren Backend-Initialisierungen

## Backend (src/core/main.py)
- Startup-Sequenz neu geordnet:
  - Minimal Logging und Pfade initialisieren
  - eel.init("web")
  - session_port berechnen (8345 bevorzugt, sonst dynamisch)
  - eel.start(..., block=False)
  - open_session_url(session_url)
  - Nach Browser-Launch: ensure_singleton(), db.init_db(), Environment-Validierung im Hintergrund/sequenziell
- wait_for_port optimiert: Sleep-Intervall auf 0.1s reduziert für schnellere Port-Erkennung
- Chromium-Flags erweitert: --disable-background-networking, --disable-sync, --disable-translate für schnellere Browser-Bereitschaft

## Frontend (web/app.html)
- Initialer UI-State: "Loading..." (responsiv), schwere Komponenten (Library, Video-Listen) werden nach Backend-Ready geladen

## Verifikationsplan
- App-Start: python3 src/core/main.py --debug
- Zeit messen: Start bis Chrome-Fenster (< 2s Ziel)
- UI zeigt "Initializing..." während Backend DB/Session prüft
- Responsivität auf localhost:8345 prüfen

## Lessons Learned
- UI-First-Strategie verbessert Boot-Geschwindigkeit und User Experience
- Hintergrundinitialisierung verhindert Blockaden beim Start
- Optimierte Chromium-Flags und Port-Erkennung beschleunigen den Verbindungsaufbau
