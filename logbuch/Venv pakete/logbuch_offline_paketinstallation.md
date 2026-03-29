# Logbuch: Offline-Paketinstallation mit lokalem Wheel-Cache

## Ziel
Python-Pakete (Wheels/Tarballs) werden im Projekt-Unterordner (./packages/) vorgehalten und können in beliebige venvs **ohne Internetzugang** installiert werden. Ideal für reproduzierbare Builds, Docker, NAS oder Remote-Umgebungen.

---

## 1. Wheels & Dependencies herunterladen (einmalig, online)
- requirements.txt anlegen (z.B. mit pymkv2, enzyme, pymediainfo):
  ```bash
  echo "pymkv2\nenzyme\npymediainfo" > requirements.txt
  ```
- Alle Wheels und Abhängigkeiten in ./packages/ speichern:
  ```bash
  pip download -r requirements.txt -d ./packages/
  ```
- Jetzt enthält ./packages/ alle benötigten .whl/.tar.gz – kann ins Git oder Docker-Image übernommen werden.

---

## 2. Offline-Installation in jeder venv
- venv aktivieren:
  ```bash
  source .venv/bin/activate  # oder pyenv activate mkv-env
  ```
- Pakete offline installieren:
  ```bash
  pip install --no-index --find-links ./packages/ -r requirements.txt
  ```
  - `--no-index`: Kein PyPI-Zugriff
  - `--find-links ./packages/`: Nur lokaler Ordner wird genutzt
- Schnell, sicher, keine Internetabhängigkeit!

---

## 3. Automatisierungsskript (install_offline.sh)
```bash
#!/bin/bash
VENV=.venv
PACKAGES=./packages/
REQ=requirements.txt

source $VENV/bin/activate
pip install --no-index --find-links $PACKAGES/ -r $REQ
deactivate
echo "Offline install done!"
```
- Ausführbar machen: `chmod +x install_offline.sh`
- Starten: `./install_offline.sh`

---

## 4. Beispiel-Projektstruktur
```
media-lib/
├── packages/          # .whl/.tar.gz Dateien (im Git!)
├── requirements.txt
├── .venv/             # venv-3.12 (nicht ins Git)
├── envs/
│   └── mkv/           # weitere venvs
└── install_offline.sh
```

---

## 5. Für Docker/Produktivsysteme
```dockerfile
COPY packages/ /app/packages/
COPY requirements.txt .
RUN pip install --no-index --find-links /app/packages/ -r requirements.txt
```
- Keine Netzwerkabhängigkeit mehr – ideal für NAS, Remote, CI/CD.

---

## 6. Kontrolle
- Nach Installation: `pip list` zeigt alle Pakete, **ohne Download**.
- Funktioniert für beliebig viele venvs und Python-Versionen.

---

## Fazit
Mit lokalem Wheel-Cache und `--no-index`/`--find-links` installierst du Pakete offline, schnell und reproduzierbar – perfekt für professionelle Python-Projekte ohne Internetzugang.
