# Walkthrough: Centralized Media Pipelines (v1.46.044)

Die Forensic Media Workstation wurde auf eine konfigurationsgesteuerte Architektur umgestellt. Alle Audio- und Video-Pipeline-Parameter, die zuvor hartkodiert in Backend-Modulen lagen, werden nun zentral in `config_master.py` verwaltet.

---

## 🛠️ Was umgesetzt wurde

### 1. Zentrales Register (`media_pipeline_registry`)
- **Audio SSOT:** Definiert alle unterstützten Audio-Endungen und deren MIME-Typen (z.B. `.mp3` → `audio/mpeg`, `.opus` → `audio/ogg`).
- **Video SSOT:** Definiert unterstützte Videoformate und leistungsrelevante Orchestrierungs-Flags.
- **Ort:** `src/core/config_master.py` → `media_pipeline_registry`.

### 2. Konfigurationsgesteuertes Routing
- **main.py (`server_file_direct`):** MIME-Resolution erfolgt dynamisch über das Konfigurationsregister, keine hartkodierten if/elif-Blöcke mehr.
- **mode_router.py (`smart_route`):** Bitraten-Schwellen für MSE (15 Mbps), DASH (30 Mbps), MPV (50 Mbps) und Logik-Flags wie `prefer_mpv_wasm_for_webm` sind jetzt konfigurierbar.
- **handlers/ (Factory Sync):** Die Media-Handler-Factory bestimmt den Playback-Typ (Audio/Video) anhand der zentralen Endungen-Liste.

### 3. Forensische Transparenz
- **Logs:** Jede Playback-Entscheidung enthält nun ein `(Config-Driven)` oder `(Config-Tuned)` Tag, damit Auditoren nachvollziehen können, dass die Workstation-Konfiguration eingehalten wird.

---

## 🔍 Vorteile
- **Wartbarkeit:** Neue Formate können durch eine Zeile in `config_master.py` hinzugefügt werden – keine Backend-Codeänderung nötig.
- **Performance-Tuning:** Bitraten-Schwellen für Player-Engines sind im Betrieb anpassbar.

---

## Verification Results
- **Dynamic MIME Change Test:**
    - Aktion: `.mp3`-Mapping in `config_master.py` geändert.
    - Ergebnis: `[PLAY-PULSE] Direct Stream Handshake: ... | MIME: audio/mpeg (Config-Driven)`
- **Orchestrator Threshold Test:**
    - Aktion: `mse_threshold_mbps` im Registry angepasst.
    - Ergebnis: `[PLAY-PULSE] smart_route decision: ... (Config-Tuned)`

---

## Hinweise
- **Wichtig:** Um ein neues Medienformat zu unterstützen, genügt ein Eintrag in `media_pipeline_registry` in `config_master.py`.
- **Tipp:** Für Low-Bandwidth-Umgebungen kann die Schwelle `mse_threshold_mbps` direkt in der Konfiguration gesenkt werden.

---

Alle technischen Details findest du im Walkthrough v1.46.044.
