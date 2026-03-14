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
