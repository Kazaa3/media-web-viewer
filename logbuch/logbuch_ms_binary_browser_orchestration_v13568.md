# Logbuch Meilenstein: Binary & Browser Orchestration (v1.35.68)

## Ziel
Vollständige Full-Stack-Zentralisierung der Browser-Discovery und aller externen Programmpfade (cvlc, ffmpeg, ...). Die gesamte App- und Build-Umgebung ist jetzt über ein einziges, environment-aware Config-Hub steuerbar.

---

## Umsetzung & Details

### 1. Centralized Binary Registry
- **config_master.py:** program_paths-Registry und discover_binary()-Helper für automatische Tool-Lokalisierung (vlc, cvlc, ffmpeg, ffprobe, mkvmerge, ...)
- **main.py:** Entfernt alle ad-hoc shutil.which-Calls, nutzt nur noch zentrale Registry für alle Binaries

### 2. Unified Browser Discovery Ladder
- **Browser-Priorität:** Globale browser-Liste in config_master.py
- **build_system.py:** Nutzt dieselbe Ladder für Pre-Build-Checks wie main.py für Runtime
- **main.py:** start_app iteriert über zentrale Browser-Ladder für isolierte Sessions

### 3. Full Override Support
- **.env:** Jeder Programmpfad und die gesamte Browser-Ladder können via .env überschrieben werden (z.B. MWV_PATH_CVLC=/custom/path/cvlc)

---

## Zusammenfassung der zentralen Discovery
```python
"program_paths": {
    "vlc": discovery,
    "cvlc": discovery,
    "ffmpeg": discovery,
    ...
},
"browsers": ["google-chrome-stable", "google-chrome", "chrome", "chromium", "firefox", ...]
```

---

## Ergebnis
Das gesamte Media Viewer-Ökosystem wird jetzt von einem einzigen, environment-aware Config-Hub gesteuert – von Timings und Auflösung bis zu externen Binaries und Build-Metadaten.

---

**Meilenstein abgeschlossen: Binary & Browser Orchestration (v1.35.68)**
