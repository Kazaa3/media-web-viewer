# Build Process: Main vs. Dev

**Datum:** 13.03.2026
**Autor:** Copilot

## Übersicht
Im Projekt existieren zwei unterschiedliche Build-Prozesse:

1. **Main Build Process**
   - Wird bei jedem Push auf den `main`-Branch ausgelöst
   - Ziel: Sicherstellen, dass der Hauptzweig immer baubar, testbar und release-fähig bleibt
   - Führt vollständige Tests, Linting, Typprüfung und ggf. Paketierung durch
   - Keine experimentellen Features, nur geprüfter Code

2. **Dev Build Process**
   - Wird in Feature-Branches, Dev-Branches oder bei Pull Requests ausgeführt
   - Ziel: Schnelle Validierung von Entwicklungsständen, inkl. experimenteller Features
   - Kann zusätzliche Debug- oder Test-Tools aktivieren (z.B. erweiterte Logs, Debug-Artefakte)
   - Ergebnisse dienen der Entwicklung, nicht der Veröffentlichung

## Strategie
- **main**: Stabile, geprüfte Builds für Release und Produktion
- **dev/feature**: Flexible, schnelle Builds für Entwicklung und Tests
- Trennung sorgt für Zuverlässigkeit im Hauptzweig und Flexibilität in der Entwicklung

## Status
- Beide Build-Prozesse sind eingerichtet und dokumentiert
- Workflows und Trigger sind klar getrennt
