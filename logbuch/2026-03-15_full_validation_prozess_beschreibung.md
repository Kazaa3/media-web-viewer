# Schritte im Full-Validation-Prozess (CI/CD)

## Ziel
- Sicherstellen, dass nur geprüfter, lauffähiger und vollständiger Code als Release/Artefakt veröffentlicht wird.

## Typische Schritte im Full-Validation-Workflow (z.B. ci-main.yml)
1. **Checkout Code**
   - Quellcode aus dem Repository holen
2. **Set up Python**
   - Python-Umgebung (z.B. 3.11) bereitstellen
3. **Systemabhängigkeiten installieren**
   - Tools wie ffmpeg, mediainfo, xvfb, ggf. geckodriver
4. **Python-Abhängigkeiten installieren**
   - requirements-build.txt, requirements-test.txt, requirements-selenium.txt
5. **Build-Gate/Pre-Checks**
   - Linting, Type-Check, ggf. statische Analyse
6. **Tests ausführen**
   - Unit-Tests (Kernfunktionen)
   - Integrationstests (Zusammenspiel Komponenten)
   - E2E-/UI-Tests (Selenium, Xvfb)
   - Performance-/Gate-Tests (z.B. Parser-Performance, UI-Stabilität)
7. **Artefakte bauen**
   - PyInstaller-Binary, Debian-Paket, Management-Reports
8. **Artefakte hochladen**
   - Upload der Binaries, DEB-Pakete, Reports als CI-Artifacts
9. **(Optional) Release-Schritt**
   - Nur bei erfolgreichem Durchlauf: Release-Tag setzen, Upload zu GitHub Releases

## Besonderheiten
- Geckodriver wird ggf. dynamisch installiert, falls nicht im System
- Konfigurationsdateien werden je nach Umgebung gesetzt (z.B. config.main.json → config.json)
- Fehlerhafte Schritte führen zum Abbruch des Prozesses

## Vorteile
- Automatisierte, reproduzierbare Qualitätssicherung
- Minimiert manuelle Fehlerquellen
- Nachvollziehbare Build- und Testhistorie

## Wichtiger Hinweis (ab Juni 2026)
- GitHub Actions stellt die Unterstützung für Node.js 20 ein. Die Actions `actions/checkout@v4` und `actions/setup-python@v5` laufen dann standardmäßig mit Node.js 24.
- Um Kompatibilität sicherzustellen:
  - Prüfe regelmäßig, ob es neuere Versionen dieser Actions gibt, die Node.js 24 offiziell unterstützen.
  - Opt-in: Setze `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` im Workflow oder Runner, um Node.js 24 schon jetzt zu erzwingen.
  - Opt-out (nur übergangsweise): Setze `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true`, falls Node.js 20 noch benötigt wird.
- Weitere Infos: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/

## Geckodriver-Fehler: "Package 'firefox-geckodriver' has no installation candidate"
- Ursache: Das Systempaket `firefox-geckodriver` ist auf aktuellen Ubuntu-Versionen nicht mehr verfügbar.
- Lösung (bereits im Workflow umgesetzt):
  - Geckodriver wird im CI-Workflow dynamisch direkt von Mozilla heruntergeladen und installiert, falls nicht vorhanden.
  - Beispiel (ci-main.yml):
    ```yaml
    - name: Install Geckodriver (Fallback)
      run: |
        if ! command -v geckodriver; then
          echo "Geckodriver not found, downloading from Mozilla..."
          GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_name | cut -d '"' -f4)
          wget -O geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz"
          tar -xzf geckodriver.tar.gz
          chmod +x geckodriver
          sudo mv geckodriver /usr/local/bin/
          rm geckodriver.tar.gz
        fi
        geckodriver --version || (echo "Geckodriver installation failed" && exit 1)
    ```
- Damit ist der Fehler im Build-Prozess behoben und die Tests können mit aktueller Geckodriver-Version laufen.

## TODO: Geckodriver-Fix in allen Pipelines
C
- Erst dann sind alle Pipelines robust gegen das fehlende Systempaket `firefox-geckodriver`.

---

**Siehe auch:**
- .github/workflows/ci-main.yml, release.yml
- Logbuch: Build-Pipeline, GitHub Actions, CI/CD-Konfig-Ausspielung
- infra/build_system.py
