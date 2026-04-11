# Logbuch Meilenstein: UI & Session Orchestration (v1.35.68)

## Ziel
Vollständige Full-Stack-Zentralisierung von Ports, Fenstermaßen und Watchdog-Parametern. Alle UI- und Session-relevanten Einstellungen werden jetzt über das zentrale, environment-aware Config-Hub gesteuert.

---

## Umsetzung & Details

### 1. Centralized Window Control
- **config_master.py:** window_width und window_height als zentrale Settings
- --window-size-Flag wird dynamisch aus diesen Werten gebaut
- **Environment-Overrides:** MWV_WIDTH und MWV_HEIGHT in .env steuern die Auflösung ohne Codeänderung

### 2. Extended Port & Session Registry
- **vlc_port** (Default: 8080) und eel_port zentral im Registry
- **main.py:** nutzt Registry für Bootstrap-Ports und Session-Logging (besseres Audit-Trail beim Start)

### 3. Configurable Boot Watchdog
- **app_core.js:** Boot-Watchdog-Timeout aus window.CONFIG.boot_watchdog_max_ticks
- **Tuning:** MWV_WATCHDOG_TICKS in .env für längere Startup-Wartezeit auf langsamen Systemen

---

## Verified Configuration Example
```bash
# High-Res & längerer Boot-Timeout
export MWV_WIDTH=1920
export MWV_HEIGHT=1080
export MWV_WATCHDOG_TICKS=25
bash run.sh
```

---

## Ergebnis
Jeder Kernparameter – von Netzwerkports und UI-Dimensionen bis zu internen Timing-Constraints – ist jetzt zentral, dynamisch und environment-aware steuerbar.

---

**Meilenstein abgeschlossen: UI & Session Orchestration (v1.35.68)**
