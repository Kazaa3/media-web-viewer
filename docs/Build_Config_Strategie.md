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

## Vorteile
- Klare Trennung von DEV und MAIN
- Keine versehentliche Auslieferung von DEV-Konfiguration in Produktion
- Flexibel für CI/CD und lokale Entwicklung

---

**Letzte Änderung:** 2026-03-13

**Autor:** GitHub Copilot
