# Build-Pipeline Beschreibung

## Ziel
Die Build-Pipeline automatisiert die Qualitätssicherung, das Testen und die Bereitstellung des Media Web Viewer Projekts. Sie stellt sicher, dass nur geprüfter und lauffähiger Code als Artefakt veröffentlicht wird.

## Hauptschritte der Pipeline
1. **Linting & Type-Check**
   - Statische Codeanalyse (z.B. mit ruff, mypy)
   - Verhindert das Einchecken von fehlerhaftem oder unsauberem Code
2. **Unit-Tests**
   - Schnelle Überprüfung der Kernfunktionen
   - Hohe Testabdeckung wird angestrebt
3. **Integrationstests**
   - Testen des Zusammenspiels mehrerer Komponenten
   - Optional: GUI-Tests unter Xvfb
4. **Build-Artefakte erzeugen**
   - Erstellen von Wheel, sdist und PyInstaller-Binaries
   - Debian-Paket (falls aktiviert)
5. **Test-Gate**
   - Nur wenn alle Tests erfolgreich sind, werden Artefakte gebaut und veröffentlicht
   - Gate-Tests: Performance, UI-Stabilität, Paket- und Umgebungschecks
6. **Release & Versionierung**
   - Automatische Synchronisation der Versionsnummern
   - Validierung der installierten Artefakte auf frischer Umgebung
   - Upload zu GitHub Releases oder Paketserver

## Beispielhafter Workflow (GitHub Actions)
```yaml
name: Build & Release
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Lint & Type-Check
        run: |
          python infra/build_system.py --lint --type-check
      - name: Run Tests
        run: |
          python infra/build_system.py --test
      - name: Build Artifacts
        run: |
          python infra/build_system.py --build all
      - name: Release Pipeline
        if: github.ref == 'refs/heads/main'
        run: |
          python infra/build_system.py --pipeline
```

## Besonderheiten
- Test-Gate kann mit `SKIP_BUILD_TESTS=1` überschrieben werden (nur für Notfälle/Entwicklung)
- Artefakte werden nur bei erfolgreichem Testlauf gebaut und veröffentlicht
- Versionierung erfolgt zentral über `update_version.py` und `VERSION`-Datei
- UI- und Performance-Tests sind Teil des Gates

## Vorteile
- Automatisierte Qualitätssicherung
- Nachvollziehbare Releases
- Minimierung von Fehlerquellen durch konsistente Abläufe

---

**Siehe auch:**
- `infra/build_system.py`, `infra/build.py`, `infra/build_deb.sh`
- Logbuch-Einträge zu Teststruktur und Artefakten
- [README.md](../README.md), [DOCUMENTATION.md](../DOCUMENTATION.md)
