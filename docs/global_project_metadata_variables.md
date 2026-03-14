# Global Project Metadata Variables

**Datum:** 14.03.2026
**Autor:** Copilot

---

## Ziel

Name, Version, Lizenz und Projektbeschreibung werden als globale Variablen ähnlich der bestehenden VERSION-Variable zentral definiert und im gesamten Projekt verwendet.

---

## Umsetzung

1. **Definition zentraler Variablen**
   - PROJECT_NAME
   - PROJECT_VERSION (wie bisher: aus VERSION-Datei)
   - PROJECT_LICENSE
   - PROJECT_DESCRIPTION

2. **Ablageort**
   - Empfohlen: Zentrale Python-Datei (z.B. `src/core/project_metadata.py`) oder als JSON/YAML in `infra/`.
   - Automatisches Einlesen der Werte in main.py und build_system.py.

3. **Verwendung**
   - Alle Stellen, die Name, Version, Lizenz oder Beschreibung benötigen (z.B. UI, Build, Setup, About-Dialog), greifen auf diese Variablen zu.
   - Synchronisation mit pyproject.toml und VERSION_SYNC.json sicherstellen.

---

## Vorteile

- Konsistenz und einfache Pflege aller Metadaten
- Keine Redundanz oder Inkonsistenzen mehr
- Zentrale Steuerung für Build, UI und Dokumentation

---

**Empfohlene Datei:**
- [src/core/project_metadata.py] (neu anlegen)
- [infra/VERSION_SYNC.json] (für Build-Tools)
- [pyproject.toml] (für Packaging)

---

**Details siehe:**
- [walkthrough.md](walkthrough.md)
