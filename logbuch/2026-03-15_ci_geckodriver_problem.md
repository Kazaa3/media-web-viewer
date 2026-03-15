# Logbuch: CI/CD Build Diagnostics – firefox-geckodriver Fehler

**Datum:** 15.03.2026

## Kontext
Automatisierter Build/CI-Lauf (GitHub Actions) für das Repository `Kazaa3/media-web-viewer`.

## Ablauf (Auszug)
- Repository wird ausgecheckt und initialisiert
- Systempakete werden per `apt-get update` aktualisiert
- Versuch, das Paket `firefox-geckodriver` zu installieren

## Fehlerbild
- Die Installation von `firefox-geckodriver` schlägt fehl:
  - `Package firefox-geckodriver is not available, but is referred to by another package.`
  - `This may mean that the package is missing, has been obsoleted, or is only available from another source.`
  - `However the following packages replace it: firefox`
  - `E: Package 'firefox-geckodriver' has no installation candidate`
  - `Error: Process completed with exit code 100.`

## Analyse
- Das Paket `firefox-geckodriver` ist in Ubuntu 24.04 (noble) nicht mehr direkt verfügbar oder wurde durch das Hauptpaket `firefox` ersetzt.
- Der Build bricht ab, da ein zwingend benötigtes Test-/E2E-Tool nicht installiert werden kann.

## Lösungsvorschläge
- Statt `apt install firefox-geckodriver` sollte das Geckodriver-Binary direkt von der offiziellen Mozilla-Seite geladen und installiert werden:
  - Download: https://github.com/mozilla/geckodriver/releases
  - Beispiel (CI):
    ```sh
    wget -qO- "https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz" | tar xz -C /usr/local/bin
    chmod +x /usr/local/bin/geckodriver
    ```
- Alternativ: Nur das Paket `firefox` installieren und prüfen, ob der enthaltene Geckodriver ausreicht (`which geckodriver`).
- Build-Skripte und CI-Workflows anpassen, um auf Paketänderungen in neuen Ubuntu-Versionen zu reagieren.

## Ergebnis
- Fehler ist dokumentiert, Build bleibt reproduzierbar.
- Anpassung der CI-Workflows notwendig, um E2E-Tests mit Firefox/Geckodriver weiterhin zu ermöglichen.
