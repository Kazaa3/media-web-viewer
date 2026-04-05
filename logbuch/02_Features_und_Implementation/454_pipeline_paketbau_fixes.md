# Pipeline- und Paketbau-Fixes (März 2026)


---

## Hinweis: Hardcodierte Pfade im Paketbau

Im Rahmen der Migration und Bereinigung wurden an mehreren Stellen (z.B. im Paketbau, in postinst-Skripten und Test-Suites) hardcodierte Pfade wie

  './opt/media-web-viewer/src/core/main.py',
  './opt/media-web-viewer/infra/requirements.txt',
  './usr/bin/media-web-viewer'

identifiziert. Diese wurden im Zuge der Umstrukturierung angepasst, sodass sie mit der neuen Infrastruktur und den verschobenen requirements-Dateien kompatibel sind.

**Empfehlung:**
- Bei zukünftigen Änderungen an der Verzeichnisstruktur sollten alle Skripte und Paketdefinitionen auf solche hardcodierten Pfade überprüft und ggf. angepasst werden, um Build- und Installationsfehler zu vermeiden.
## Zusammenfassung der Korrekturen

- **SyntaxError behoben:**
  - In `infra/build_system.py` wurde ein unterbrochener f-string repariert, der den Start der Pipeline verhinderte.
- **Pfad-Korrektur für Requirements:**
  - Die `requirements.txt` wurde nach `infra/` verschoben. Das Debian-Installationsskript (`postinst`) und die Test-Suite (`test_reinstall_deb.py`) wurden angepasst, damit sie die Datei am neuen Ort finden.
- **Venv-Konzept in CI:**
  - Die Workflows nutzen jetzt explizit `infra/requirements-build.txt` (Build) und `infra/requirements-test.txt` (Tests).

## Nächste Schritte

1. **M1-Stand aktualisieren:**
   ```bash

  ---

  ## Ergänzung: venv/Requirements-Nutzung in CI/CD (März 2026)

  - **Build-Phase:** nutzt `infra/requirements-build.txt` (Core + PyInstaller + Wheel)
  - **Test-Phase:** nutzt `infra/requirements-test.txt` (Core + Pytest + Coverage)
  - **Selenium-Phase:** nutzt `infra/requirements-selenium.txt`
  - Die `infra/requirements.txt` im Root ist nur noch ein Redirect auf die Core-Abhängigkeiten (Abwärtskompatibilität).
  - In den Workflows wurden generische requirements-Aufrufe durch die spezialisierten Files ersetzt.

  Die Änderungen sind gepusht. Die GitHub Actions sollten jetzt automatisch neu starten und die Abhängigkeiten korrekt auflösen. Sobald die Checks grün sind, kann der Merge nach `main` (Schritt 1 im Tutorial) durchgeführt werden.

  Damit ist v1.34 technisch "sauber" und bereit, die stabile Basis für den Videoplayer in Meilenstein 1 zu bilden.
   ```
2. **Pipeline lokal verifizieren:**
   ```bash
   source .venv_testbed/bin/activate
   ./infra/build_system.py --pipeline
   ```

## Ausblick: Videoplayer
- Sobald die Pipeline für v1.34 grün ist, ist das Fundament fertig.
- Dann wird der Branch `feature/m1-video-implementation` erstellt und der eigentliche Player entwickelt.

## Merge nach main
- Gerne unterstütze ich dich beim Merge nach `main`, sobald die Tests erfolgreich durchgelaufen sind.

- source .venv_testbed/bin/activate
- which python  # Sollte ~/.venv_core/bin/python zeigen
- chmod +x ./infra/build_system.py
- ./infra/build_system.py --pipeline            oder: source .venv_testbed/bin/activate && ./infra/build_system.py --pipeline
- git checkout meilenstein-1-mediaplayer
- git pull origin meilenstein-1-mediaplayer



