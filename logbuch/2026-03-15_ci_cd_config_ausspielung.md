# Verknüpfung: CI/CD-Pipeline & Konfigurationsausspielung

## Ziel
- Die CI/CD-Pipeline sorgt dafür, dass je nach Umgebung (Entwicklung, Test, Produktion) die passende JSON-Konfigurationsdatei ausgeliefert und verwendet wird.

## Mechanismus
- Im Build- und Release-Prozess (z.B. GitHub Actions) wird gesteuert, welche Konfigurationsdatei (`config.json`, `config.main.json`, `config.develop.json`) ins Web-Frontend oder ins Artefakt kopiert wird.
- Typische Muster:
  - **Entwicklung:** `config.develop.json` → `config.json`
  - **Produktion:** `config.main.json` → `config.json`
  - **Test/CI:** ggf. eigene Test-Konfig
- Das Ziel: Im ausgelieferten Paket liegt immer eine Datei `config.json` mit den passenden Einstellungen für die Zielumgebung.

## Beispiel: GitHub Actions Workflow-Step
```yaml
- name: Set production config
  if: github.ref == 'refs/heads/main'
  run: cp web/config.main.json web/config.json

- name: Set develop config
  if: github.ref == 'refs/heads/develop'
  run: cp web/config.develop.json web/config.json
```

## Vorteile
- Klare Trennung von Umgebungen und Einstellungen
- Minimiert Fehler durch falsche Konfiguration
- Automatisierte, reproduzierbare Ausspielung

## Hinweise
- Die Auswahl und das Kopieren der Konfigurationsdatei kann auch im Build-Skript (`build_system.py`) erfolgen
- Für lokale Entwicklung kann die Konfig manuell gewechselt werden
- Im Release-Artefakt (z.B. PyInstaller, Debian) ist immer nur die passende `config.json` enthalten

---

**Siehe auch:**
- Logbuch: JSON-Konfigs Beschreibung
- .github/workflows/ci-main.yml, build_system.py
- web/config.json, web/config.main.json, web/config.develop.json
