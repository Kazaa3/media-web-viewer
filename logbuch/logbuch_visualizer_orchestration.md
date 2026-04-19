# Logbuch: Visualizer Global Configuration & Orchestration

## Ziel
Die Visualizer-(Equalizer-)Einstellungen werden aus dem lokalen Browser-Storage in die zentrale Backend-Konfiguration (`config_master.py`) verschoben. Dadurch ist eine administrative Steuerung von Animation, Stil und Farben möglich.

---

## Maßnahmen

### 1. Configuration Core
- **config_master.py:**
  - Neues `visualizer_orchestration`-Block in `GLOBAL_CONFIG`:
    - `animation_enabled`: True/False
    - `default_style`: "bars" (Default), "circle", "wave"
    - `accent_color`: "auto" (folgt UI) oder Hex-Code (z.B. "#00e5ff")
  - Backend-Flags haben Vorrang vor localStorage ("hard-lock").

### 2. Theme Coordination
- Standardmäßig folgt die Visualizer-Farbe der globalen `--accent-color`, außer es ist explizit ein `VISUALIZER_ACCENT_COLOR` gesetzt.

### 3. Frontend Pipeline
- **audioplayer.js:**
  - `setupVisualizer()` prüft `window.GLOBAL_CONFIG.visualizer_orchestration.animation_enabled`. Ist dies `False`, wird der Visualizer nicht initialisiert.
  - Stil-Fallback: `default_style` aus Config, falls localStorage leer ist.
  - `drawVisualizer()` holt die Farbe aus der globalen Config und wendet sie auf Balken/Wellen an.

---

## Offene Fragen
- Soll der Visualizer standardmäßig immer der UI-Akzentfarbe folgen oder fest auf "Perfect Reference Blue" (#007aff) stehen?
- Soll ein Footer-Toggle das globale "Animation Enabled"-Flag temporär überschreiben können?

---

## Verifikation
- **animation_enabled** auf `False` setzen → Bars verschwinden beim nächsten Track.
- **accent_color** auf `#ff0000` setzen → Bars werden überall rot.
- Verschiedene Styles (bars, circle, wave) über Backend-Config testen.

---

*Status: Visualizer-Konfiguration globalisiert und administrierbar. Weitere Orchestrierungsoptionen auf Wunsch möglich.*
