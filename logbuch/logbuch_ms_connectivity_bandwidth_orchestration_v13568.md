# Logbuch Meilenstein: Connectivity & Bandwidth Orchestration (v1.35.68)

## Ziel
Integration von Connectionless Mode und Bandwidth Optimization in das zentrale Konfigurationssystem. Vollständige Steuerung von Netzwerk- und Ressourcenverhalten über die zentrale Registry.

---

## Umsetzung & Details

### 1. Connectionless Mode
- **Backend:** Respektiert MWV_CONNECTIONLESS (oder legacy --n)
- Startet im "detached" Modus (eel_mode = None), ideal für UI-Tests gegen Mocks ohne Browserbindung
- Aktivierung: `export MWV_CONNECTIONLESS=1` oder `bash run.sh --n`

### 2. Dynamic Bandwidth Optimization
- **bandwidth_mode** (Env: MWV_BANDWIDTH) hinzugefügt
- **Low-Bandwidth:**
  - ffmpeg_deep_analysis deaktiviert (CPU/I/O-sparend)
  - fast_scan auf True für schnelle Indexierung
- **High-Bandwidth:**
  - Volle Metadatenextraktion & Deep-Inspection
  - Standardmodus

### 3. Full-Stack Synchronization
- Beide Modi werden automatisch via Eel-Bridge in window.CONFIG synchronisiert
- UI kann window.CONFIG.bandwidth_mode prüfen (z.B. für Thumbnails vs. List-View)

---

## Quick Start Beispiele
```bash
# Low-Bandwidth-Modus für Remote/Slow
export MWV_BANDWIDTH=low
bash run.sh

# Connectionless-Mode für schnelle UI-Iterationen
export MWV_CONNECTIONLESS=1
bash run.sh --n
```

---

## Ergebnis
Die zentrale Konfiguration steuert jetzt alle Verhaltensweisen von Ressourcenverbrauch bis Netzwerkisolation.

---

**Meilenstein abgeschlossen: Connectivity & Bandwidth Orchestration (v1.35.68)**
