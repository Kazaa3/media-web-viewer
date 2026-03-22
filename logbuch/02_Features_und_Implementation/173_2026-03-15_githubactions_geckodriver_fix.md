# Fix: Geckodriver-Fehler in GitHub Actions (Ubuntu)

## Problem
Das Systempaket `firefox-geckodriver` ist auf aktuellen Ubuntu-Runnern oft nicht mehr verfügbar oder veraltet. Dies führt zu Fehlern wie `geckodriver not found` oder inkompatiblen Versionen im CI.

## Lösung (März 2026)
Im Workflow `.github/workflows/ci-main.yml` wurde ein Fallback-Schritt ergänzt, der Geckodriver direkt von Mozilla herunterlädt und installiert, falls er nicht im System vorhanden ist:

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

## Ergebnis
- Geckodriver ist immer in aktueller Version verfügbar, unabhängig vom Ubuntu-Paketstatus.
- CI-Fehler durch fehlenden oder veralteten Geckodriver werden vermieden.

**Letzte Änderung:** 15.03.2026
