# Pipeline- und Paketbau-Fixes (März 2026)

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
   git checkout meilenstein-1-mediaplayer
   git pull origin meilenstein-1-mediaplayer
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

- source .venv_core/bin/activate
- which python  # Sollte ~/.venv_core/bin/python zeigen
- chmod +x ./infra/build_system.py
- ./infra/build_system.py --pipeline
- git checkout meilenstein-1-mediaplayer
- git pull origin meilenstein-1-mediaplayer