# Logbuch: Mehrere reine Python-Versionen mit pyenv und venv für saubere App-Umgebungen

## Ziel
Mehrere isolierte Python-Versionen (ohne Zusatzpakete) als venvs für Tests und Entwicklung in der App-Umgebung unter MX Linux bereitstellen. Keine Paketkonflikte, maximale Vergleichbarkeit und Reproduzierbarkeit.

---

## 1. Vorbereitung: pyenv installieren
- Systemabhängigkeiten installieren:
  ```bash
  sudo apt update && sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
  ```
- pyenv via Git installieren:
  ```bash
  curl https://pyenv.run | bash
  ```
- In `~/.bashrc` einfügen:
  ```bash
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  ```
- Terminal neu starten oder `source ~/.bashrc` ausführen.

---

## 2. Python-Versionen installieren
- Verfügbare Versionen anzeigen:
  ```bash
  pyenv install --list | grep 3.
  ```
- Gewünschte Versionen installieren (z.B.):
  ```bash
  pyenv install 3.12.2
  pyenv install 3.11.9
  pyenv install 3.10.14
  ```

---

## 3. Leere venvs pro Version anlegen
- Im Projektordner:
  ```bash
  pyenv local 3.12.2
  python -m venv venv-3.12
  pyenv local 3.11.9
  python -m venv venv-3.11
  ```
- Jede venv enthält nur die Python-Basisinstallation, keine Zusatzpakete.

---

## 4. Nutzung in der App
- Aktivieren:
  ```bash
  source venv-3.12/bin/activate
  ```
- Testen:
  ```bash
  python dein_script.py
  ```
- Deaktivieren:
  ```bash
  deactivate
  ```

---

## 5. Übersichtstabelle
| Befehl                        | Zweck                        |
|-------------------------------|------------------------------|
| pyenv versions                | Zeigt alle Versionen         |
| pyenv local 3.12.2            | Setzt lokale Version         |
| source venv-3.12/bin/activate | Aktiviert venv (leer)        |
| deactivate                    | Deaktiviert venv             |

---

## Hinweise
- Jede venv ist komplett unabhängig und enthält nur die gewünschte Python-Version.
- Für Docker: Multi-stage-Builds mit pyenv-basierten Images möglich.
- VS Code erkennt die venvs über den Interpreter-Selector.
- requirements.txt pro venv: `pip freeze > req-3.12.txt` (optional, leer starten).

---

## Fazit
Mit pyenv und venv lassen sich beliebig viele reine Python-Umgebungen für Tests und Entwicklung bereitstellen – ohne Paketkonflikte, mit maximaler Kontrolle über die Python-Versionen. Ideal für reproduzierbare Tests und CI/CD.
