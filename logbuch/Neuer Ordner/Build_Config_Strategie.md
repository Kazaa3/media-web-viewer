# Build Config Strategie: DEV vs MAIN

## Ziel

Konfigurationsdateien für Entwicklungs- und Produktionsumgebungen (main) getrennt ausliefern und in der Build-Pipeline berücksichtigen.

---

## Vorgehen

1. **Konfigurationsdateien strukturieren**
   - `config/dev_config.yaml` oder `.env.dev`
   - `config/main_config.yaml` oder `.env.main`

2. **Build-Pipeline anpassen**
   - DEV-Build: verwendet dev_config.yaml oder .env.dev
   - MAIN/Release-Build: verwendet main_config.yaml oder .env.main
   - Automatische Auswahl per Build-Flag oder Umgebungsvariable (z.B. `BUILD_ENV=dev` oder `BUILD_ENV=main`)

3. **Auslieferung**
   - DEV-Artefakte enthalten nur DEV-Konfiguration
   - Release-Artefakte enthalten nur MAIN-Konfiguration
   - Optional: Beispiel-Konfiguration (`config/example_config.yaml`) für neue Installationen

4. **.gitignore beachten**
   - Sensible oder maschinenbezogene Konfigurationsdateien (z.B. mit Passwörtern) nicht ins Repo aufnehmen
   - Nur Beispiel- oder Template-Konfigurationen versionieren

---

## Beispiel für Build-System (build_system.py)

```python
import os
BUILD_ENV = os.environ.get('BUILD_ENV', 'dev')
if BUILD_ENV == 'main':
    config_path = 'config/main_config.yaml'
else:
    config_path = 'config/dev_config.yaml'
```

---

## Ultimate Mode / Full Mode

Der "Ultimate Mode" (teils als "Full Mode" referenziert) ist eine spezielle Build- und Laufzeit-Konfiguration, die alle Features, Parser, und Integrationen aktiviert.

### Eigenschaften
- Aktiviert sämtliche optionalen und experimentellen Features
- Nutzt alle verfügbaren Parser und Backend-Module
- Ermöglicht vollständige Integrationstests und End-to-End-Tests
- Wird für CI/CD, Release-Validierung und Feature-Demos verwendet

### Konfiguration
- Eigene Konfigurationsdatei: `config/ultimate_config.yaml` oder `.env.ultimate`
- Build-Flag: `BUILD_ENV=ultimate`
- Kann als Referenz für "Full Mode" in Dokumentation und Code verwendet werden

### Auslieferung
- Ultimate-Artefakte enthalten alle Features und Integrationen
- Für Entwickler, CI/CD und Testumgebungen empfohlen
- Nicht für Endnutzer/Produktivsysteme

---

**Letzte Änderung:** 2026-03-13

**Autor:** GitHub Copilot
