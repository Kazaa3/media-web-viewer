# Logbuch-Eintrag: Database Purge & Clean Release Policy (Final)

## Ziel
Sicherstellen, dass Release-Installationen immer mit einem sauberen Zustand starten, während Entwicklungsinstallationen persistente Daten für effizientes Testen behalten.

## Konzept & Umsetzung
- **Clean Packages:** Das .deb-Installationspaket schließt das `data/`-Verzeichnis explizit aus. Jede Neuinstallation startet mit einer leeren Datenbank ("let app build it").
- **Environment-Aware Purge:**
  - **Release Builds:** `apt purge` entfernt das gesamte Anwendungsverzeichnis.
  - **Development Builds:** `apt purge` erhält das `data/`-Verzeichnis, um den User-Library-Status für Tests zu bewahren.
- **Verbesserte Metadaten:** Branch-Awareness in den Packaging-Skripten, gesteuert über `.build_metadata`.

---

# Logbuch-Eintrag: Advanced Build Pipeline & Stabilization (Update)

## Ziel
Letzter Feinschliff für stabile Releases und Entwicklung.

## Konzept & Umsetzung
- **Branch-Aware Deployments:** Automatische Erkennung von `main` vs. `develop` und deployment-spezifischer `config.json`-Templates.
- **Reporting Infrastructure:** Standardisierte `build/management_reports` für alle Testergebnisse, automatisierte JUnit-XML-Generierung für das 24-Test-Build-Gate.
- **Test Suite Haerdening:** Fix für parents[3] vs. parents[4] bei tief verschachtelten Tests, UI-Assertions gegen Browser-Formatierungsänderungen gehärtet.
- **Database Persistence Policy:** `postrm` prüft `.build_metadata`, um `data/` für Dev-Builds zu erhalten, aber für Releases zu löschen.
- **Usage:**
  ```bash
  python3 infra/build_system.py --test-gate  # 100% Pass verified
  ```

## Status
Abgeschlossen – Release- und Entwicklungs-Policy, Build-Pipeline und Testhärtung sind umgesetzt und getestet.

## Stand
13. März 2026
