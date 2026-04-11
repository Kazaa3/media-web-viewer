# Logbuch Meilenstein: Ultimate Config & Dependency Orchestration (v1.35.68)

## Ziel
Vollständige Zentralisierung aller Wartezeiten, Sleep-Intervalle und Abhängigkeitsdefinitionen. Die gesamte App ist jetzt über ein einziges, environment-aware Config-Hub steuerbar.

---

## Umsetzung & Details

### 1. Centralized Sleep & Wait Timing
- **config_master.py:** sleep_times-Section für globale Steuerung aller App-Intervalle
- **main.py:** nutzt sleep_times für Keepalive-Loop und Startup-Probe
- **app_core.js:** Boot-Watchdog respektiert window.CONFIG.sleep_times.watchdog_tick

### 2. Definitive Dependency Bundle
- **requirements-full.txt:** Konsolidiert Core, Test, Dev, Build, Selenium in eine modulare Quelle
- **pytest & UI-Engines:** pytest, Playwright, Selenium im Full-Bundle enthalten
- **Ease of Use:** Komplettinstallation via `./run.sh --full` in .venv

### 3. Full-Stack Build & Meta Sync
- **build_config.py:** Zentrale VERSION, PACKAGE, ARCH
- **build_deb.sh:** Nutzt build_config.py für konsistente Installer-Metadaten

### 4. Verified Configuration Template
- **.env.example:** Zeigt Override für MWV_SLEEP_*-Intervalle und MWV_TEST_ENGINE

---

## Ergebnis
Jeder Aspekt der App – von Boot-Intervallen über Abhängigkeitslayer bis zu Build-Metadaten – ist jetzt zentral, modular und environment-aware steuerbar.

---

**Meilenstein abgeschlossen: Ultimate Config & Dependency Orchestration (v1.35.68)**
