# Architektur- und Testplan für Bottle/Eel-Mediaplayer-App (22.03.2026)

## 1. Gesamtaufbau der App

### Backend (Bottle)
- API-Endpunkte für Medien-Metadaten, Playlists, Suche, Konfiguration
- Eel als Bridge für JS-Aufrufe (`@eel.expose`), die auf Bottle-Routen oder Python-Logik aufbauen

### Frontend (HTML/CSS/JS)
- Vanilla-JS, kein Framework-Overhead
- Player-Logik (Wiedergabe, Seek, Playlist-Steuerung) via JS-APIs (HTMLMediaElement, webkitAudioContext etc.)

### Eel-Rolle
- Nur für Kommunikation zwischen Python und Browser (z. B. eel.call_python(...), @eel.expose)
- Startet Chromium im App-Mode (`--app=` oder `--kiosk`)

## 2. Test-Architektur (Schichten)
| Schicht           | Tests                                 | Technologie                |
|-------------------|---------------------------------------|----------------------------|
| Backend-Unit      | Python-Funktionen, DAOs, Parser       | pytest oder unittest       |
| API-Integration   | Bottle-Endpunkte (HTTP-Level)         | pytest + requests/Test-Client |
| UI-Unit           | JS-Logik (Player, Playlist, Hotkeys)  | Jest, Mocha, jsdom         |
| E2E-UI            | Nutzer-Workflows im Player-Browser    | Selenium (ChromeDriver)    |

## 3. Konkrete Planung der Tests

### a) Backend-Tests (pytest/unittest)
- Teste Scan-Logik, Metadaten-Extraktion, DB-Layer, Suchalgorithmen
- pytest als Haupt-Framework empfohlen

### b) API- und Integrationstests
- Starte Bottle-App im Test-Modus (z. B. http://127.0.0.1:8080)
- Teste Endpunkte mit requests oder Bottle-Test-Client

### c) UI-Unit-Tests (JS)
- Teste Player-Steuerung, Playlist-Handling, Hotkeys
- Framework: Jest oder Mocha/Chai mit jsdom

### d) E2E-Tests mit Selenium
- Nutzer-Workflows: Player öffnen, Titel wählen, Play/Seek/Stop, Playlist-Wechsel, Hotkeys, Eel-Feedback
- Setup: App mit eel.start(...), Chromium im App-Mode, Selenium-WebDriver mit --remote-debugging-port + debuggerAddress
- Beispiel (pytest):
  ```python
  import pytest
  from selenium import webdriver
  from selenium.webdriver.chrome.options import Options

  @pytest.fixture
  def selenium_chrome():
      options = Options()
      options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
      driver = webdriver.Chrome(options=options)
      yield driver
      driver.quit()

  def test_player_starts(selenium_chrome):
      selenium_chrome.get("http://127.0.0.1:8080/player.html")
      play_button = selenium_chrome.find_element(...)
      play_button.click()
      # assert, dass der Player-Status entsprechend ändert
  ```

## 4. Praktischer Architektur-Vorschlag

```
project/
├── bottle_eel/
│   ├── main.py          # Bottle + Eel start
│   ├── media_api.py     # Endpunkte, Logik
│   └── playerserver.py  # Eel-Funktionen, Player-Steuerung
├── frontend/
│   ├── index.html
│   ├── css/...
│   ├── js/
│   │   ├── player.js      # Player-Logik
│   │   └── player.test.js # JS-Unit-Tests
├── tests/
│   ├── backend/          # Python-Unit/API-Tests
│   │   ├── test_api.py
│   │   └── test_logic.py
│   ├── ui/               # JS-Unit-Tests
│   └── e2e/              # Selenium-E2E-Tests
│       └── test_player_e2e.py
```

## 5. Testklassifizierung & Testpyramide

### Test-Ebenen für die Bottle/Eel-Mediaplayer-App

| Ebene                          | Kurzbeschreibung                                                                 | Beispiel für diese App                                                                 |
|--------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **Unit-Tests**                 | Einzelne Funktionen/Klassen, ohne Abhängigkeiten (Mocks, reine Logik)            | Python: `parse_metadata`, `scan_library`; JS: Player-Funktionen                        |
| **Integrationstests**          | Zusammenspiel mehrerer Komponenten (API + DB, Frontend + Backend)                | Bottle-Endpunkte + DB-Layer; JS-Player bezieht Daten von Bottle-API                    |
| **System-/E2E-Tests (UI-Layer)**| Komplette Nutzer-Workflows im Browser (End-to-End)                               | Selenium-Tests, die die Mediaplayer-UI im Chromium-App-Fenster durchklicken            |
| **Abnahme-/Akzeptanztests**    | Validieren, ob die App den Anforderungen entspricht (User-Perspektive)            | Album wählen → Play → Seek → Pause → Darstellung prüfen                                |

### Ordnerzuordnung & Testarten

| Ordner/Datei                | Testart             | Typische Tools/Frameworks         |
|-----------------------------|---------------------|-----------------------------------|
| `tests/backend/`            | Unit, Integration   | pytest, unittest                   |
| `tests/ui/`                 | JS-Unit             | Jest, Mocha, jsdom                 |
| `tests/e2e/`                | E2E (UI)            | Selenium (Python, ChromeDriver)    |
| `frontend/js/player.test.js`| JS-Unit             | Jest, Mocha                        |

### Empfehlungen zur Testpyramide
- Viele kleine Unit-Tests (schnell, stabil)
- Weniger Integrationstests
- Noch weniger E2E-Tests (aufwendig, aber wertvoll)

**Praxis für dieses Projekt:**
- `pytest`-Unit-Tests auf Python-/JS-Logik
- Integrationstests auf API- und DB-Ebene
- Selenium-E2E-Tests für zentrale Player-Workflows (Play, Seek, Playlist-Wechsel)

**Weitere Infos:**
- [walter-test-engineering: Teststufen](https://walter-test-engineering.de/lexikon/teststufen/)
- [onit: Unit, Integration, E2E](https://onit.eu/de/blog/when-to-unit-e2-e-and-integration-test)
- [Testpyramide erklärt (LinkedIn)](https://de.linkedin.com/pulse/mastering-testing-pyramid-c-complete-guide-unit-e2e-tests-hernandes-lrgnf?tl=de)

## Dev-Workflow
- Backend-Änderung → pytest tests/backend/
- Frontend-Änderung → JS-Unit-Tests + manuelles Testen im Chromium-App-Fenster
- Großer UX-Change → E2E-Selenium-Suite laufen lassen

**Für ein minimal lauffähiges E2E-Test-Setup einfach Start-Call und Test-Framework angeben!**

## 6. Fehlende Infrastruktur-, CI- & Testqualitäts-Bausteine

### 1. Infrastruktur & Setup
- **Docker-Container**: Ein Image, das Bottle, Eel, Chromium-App-Modus und alle Tests kapselt → saubere Dev-/CI-Umgebung ohne "läuft nur auf meinem Rechner"-Effekte. [Microsoft: Selenium in CI](https://learn.microsoft.com/de-de/azure/devops/pipelines/test/continuous-test-selenium?view=azure-devops)
- **Test-Portabilität**: Explizite Start-Skripte (`start_dev.sh`, `start_test.sh`), die Bottle-Eel + Chromium + `--remote-debugging-port` für Selenium vorbereiten. [Tutorialspoint: Selenium attach](https://www.tutorialspoint.com/article/how-to-connect-to-an-already-open-browser-using-selenium-webdriver)

### 2. Test-Organisation & Qualität
- **Explizite Test-Tags/Kategorien**: In `pytest` z. B. `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.selenium` – gezieltes Ausführen von Testgruppen. [dev.to: pytest + selenium](https://dev.to/testmuai/test-automation-using-pytest-and-selenium-webdriver-jd8)
- **Page-Object-Pattern für Selenium**: Zentrale Klasse `MediaPlayerPage` mit Methoden wie `play()`, `seek()`, `get_current_track()` für wartbare E2E-Tests. [Picnic: UI-Test-Automation](https://jobs.picnic.app/en/blogs/behavior-driven-ui-test-automation-with-selenium)
- **Testdaten-Management**: Kleines Beispiel-Medienverzeichnis (2–3 Tracks), das Tests automatisch anlegen/löschen → reproduzierbare E2E-Tests. [doubleslash: E2E-Testabdeckung](https://blog.doubleslash.de/software-technologien/e2e-testabdeckung-messen/)

### 3. Qualität & Wiederholbarkeit
- **Health-Check/Setup-Test**: Minimaler Test prüft Browser-Sitzung, Media-Endpunkt, Player-Elemente – läuft immer zuerst. [walter-test-engineering: E2E-Test](https://walter-test-engineering.de/lexikon/end-to-end-test-testing/)
- **Headless-Modus für Tests**: Selenium-E2E-Tests im `headless`-Chromium (schneller, CI-tauglich), UI-Tests im normalen Browser nur manuell debuggen. [browserstack: Selenium Headless](https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test)

### 4. CI / Release-Aspekte
- **CI-Pipeline**: Git-Hook/GitHub-Actions/GitLab-CI, die `pytest tests/backend/` und `tests/e2e/` durchläuft, die Bottle-Eel-App im Test-Modus startet und Selenium-E2E-Tests ausführt. [Microsoft: Selenium in CI](https://learn.microsoft.com/de-de/azure/devops/pipelines/test/continuous-test-selenium?view=azure-devops)
- **Test-Reporting**: JSON/HTML-Reports aus `pytest` und Screenshots bei fehlgeschlagenen Selenium-Tests (`pytest-html`, Screenshot-Hook in Selenium). [blazemeter: Selenium UI-Tests](https://www.blazemeter.com/blog/selenium-ui-tests)

**Wenn du deinen aktuellen Projektbaum und Docker/CI-Status schickst, folgt ein konkretes "Fehlende-Bausteine"-Set mit Beispielskripten und pytest-Konfiguration!**

## 7. Beispiel: Ordnernamen rekursiv mit Fortschrittsbalken (Python)

Hier ein erweitertes Python-Skript, das alle Ordnernamen (rekursiv) mit Fortschrittsbalken und Anzeige der aktuellen Ordnernummer ausgibt:

```python
import os
from tqdm import tqdm

# Zähle zuerst alle Ordner
folder_list = []
for root, dirs, files in os.walk("."):
    for d in dirs:
        folder_list.append(d)

total = len(folder_list)

with open("folders.txt", "w", encoding="utf-8") as out:
    for idx, d in enumerate(tqdm(folder_list, desc="Ordner", unit="Ordner")):
        out.write(d + "\n")
        print(f"{idx+1}/{total}: {d}")
```

**Hinweise:**
- tqdm muss installiert sein: `pip install tqdm`
- Fortschrittsbalken und aktuelle Nummer werden in der Konsole angezeigt.
- Die Datei `folders.txt` enthält alle Ordnernamen (wie vorher).
- Dieses Skript funktioniert auch auf Netzlaufwerken, solange Python Schreibrechte hat.

## 8. Spotify Connect von der Kommandozeile

**Ziel:** Spotify-Playback und Geräteauswahl (Connect) direkt vom Terminal aus steuern.

### Tools
- **spotifyd**: Headless Spotify-Client (Daemon), der als Connect-Device erscheint
- **spotify-tui (spt)**: Terminal-UI für Spotify (Playlists, Suche, Device-Auswahl)
- **spotipy**: Python-API für eigene Skripte

### Kurzanleitung
1. **Installation**
   - spotifyd: z. B. `sudo apt install spotifyd` oder via Paketmanager
   - spotify-tui: `cargo install spotify-tui` oder Paketmanager
2. **Konfiguration** (`~/.config/spotifyd/spotifyd.conf`):
   ```
   [global]
   username = "dein_spotify_benutzername"
   password = "dein_spotify_passwort"
   backend = "pulseaudio"
   device_name = "MeinLinux"
   ```
3. **Starten**
   - `spotifyd --no-daemon`
   - `spt` (spotify-tui starten, einloggen, unter "Devices" Connect-Ziel wählen)

### Hinweise
- Spotify Connect benötigt Premium-Account
- Mit spotipy (Python) lassen sich Geräte und Playback auch programmatisch steuern
- Funktioniert auf Linux, Mac, Windows (je nach Backend)

**Quellen:**
- [spotifyd GitHub](https://github.com/Spotifyd/spotifyd)
- [spotify-tui GitHub](https://github.com/Rigellute/spotify-tui)
- [spotipy Doku](https://spotipy.readthedocs.io/en/2.22.1/)

## 9. Spotify Connect – Strukturierter Überblick & Entwickler-Tipps

### 1. Spotify-Daemon + TUI-Client (spotifyd + spotify-tui)
- **spotifyd**: Leichtgewichtiger Daemon, erscheint als Spotify-Connect-Gerät. Konfiguration in `~/.config/spotifyd/spotifyd.conf` (Benutzername, Passwort, Backend, device_name).
- **spotify-tui**: Terminal-UI für Spotify. Einloggen, Playlists durchsuchen, unter „Devices“ Connect-Ziel wählen.

**Typischer Ablauf (Linux):**
```bash
# Installieren (z.B. via cargo oder Paketmanager)
cargo install spotifyd spotify-tui
# oder
sudo apt install spotifyd spotify-tui

# Konfiguration anlegen
mkdir -p ~/.config/spotifyd
vim ~/.config/spotifyd/spotifyd.conf
# [global]
# username = "dein_spotify_username"
# password = "dein_spotify_pass"
# backend = pulse
# device_name = "spotifyd"

# Daemon starten
spotifyd

# Terminal-Client starten
spotify-tui
```

### 2. Eigene Python-Skripte mit spotipy
- **spotipy**: Offizielles Python-SDK für die Spotify-Web-API. Geräte abfragen, Playlists/Tracks/Status lesen, mit `transfer_playback()` Geräte wechseln.

**Beispiel:**
```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-playback-state,user-modify-playback-state",
    client_id="...",
    client_secret="...",
    redirect_uri="http://localhost:8888",
))

devices = sp.devices()
for device in devices["devices"]:
    print(device["name"], device["id"], device["is_active"])
    if device["name"] == "spotifyd":
        sp.transfer_playback(device["id"])
```
**Wichtig:** Für Connect/transfer_playback brauchst du einen Premium-Account und die richtigen OAuth-Scopes.

### 3. Bonus für Entwickler / Self-Host-Nutzer
- **spotifyd als systemd-Service**: Dein Rechner/NAS ist immer ein Connect-Gerät.
- **Eigene spotipy-Skripte**: Automatischer Gerätewechsel, Integration in eigene Mediaplayer-Setups.

**Tipp:** Kombiniere spotifyd, spotify-tui und spotipy für ein flexibles, skriptgesteuertes Multiroom- oder Server-Setup.

**Auf Wunsch: Konkretes Setup-Beispiel für systemd, TUI und spotipy-Skript passend zu deinem Bottle/Eel-Mediaplayer!**

## 10. spotipy – Spotify Web API in Python

**spotipy** ist ein offizielles Python-Paket für die Spotify-Web-API. Es ermöglicht:
- Geräte- und Playback-Steuerung (Connect, Play, Pause, transfer_playback)
- Playlists, Tracks, Alben, Nutzerinfos abfragen und verwalten
- Integration in eigene Tools, Server, Automatisierungen

### Installation
```bash
pip install spotipy
```

### OAuth-Scopes (wichtig für Connect/Playback)
- `user-read-playback-state`
- `user-modify-playback-state`
- `user-read-currently-playing`
- (je nach Anwendungsfall weitere, z. B. für Playlists)

### Beispiel-Workflow: Geräte abfragen & Playback umschalten
```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-playback-state,user-modify-playback-state",
    client_id="...",
    client_secret="...",
    redirect_uri="http://localhost:8888",
))

devices = sp.devices()
for device in devices["devices"]:
    print(device["name"], device["id"], device["is_active"])
    if device["name"] == "spotifyd":
        sp.transfer_playback(device["id"])
```

### Tipps
- Die erste Authentifizierung öffnet einen Browser für das OAuth-Login.
- Die Zugangsdaten (Tokens) werden lokal gespeichert und automatisch erneuert.
- Für Server/Headless-Betrieb: Token-Handling und Redirect-URI beachten.
- Kombinierbar mit anderen Tools (z. B. für automatisches Umschalten auf ein bestimmtes Gerät beim Start deines Mediaplayers).

**Doku:** [https://spotipy.readthedocs.io/en/2.22.1/](https://spotipy.readthedocs.io/en/2.22.1/)

## 11. Übersicht: Verwendete Programme & Tools

| Programm/Tool   | Zweck/Beschreibung                                              |
|-----------------|-----------------------------------------------------------------|
| **spotifyd**    | Headless Spotify-Connect-Daemon, erscheint als Connect-Gerät    |
| **spotify-tui** | Terminal-UI für Spotify, Playlists/Devices/Playback steuern     |
| **spotipy**     | Python-API für Spotify Web API, Automatisierung/Skripting       |
| **tqdm**        | Fortschrittsbalken für Python-Skripte                           |
| **pytest**      | Python-Testframework für Unit-/Integration-/E2E-Tests           |
| **unittest**    | Standard-Python-Testframework                                   |
| **Selenium**    | E2E-Browserautomatisierung (z. B. für UI-Tests)                 |
| **Bottle**      | Python-Webframework, Backend-API für Mediaplayer                |
| **Eel**         | Python-zu-JS-Bridge, Desktop-UI mit Browser-Frontend            |
| **Chromium**    | Browser, App-Modus für Mediaplayer-Frontend und Selenium-Tests  |
| **systemd**     | (Optional) Service-Manager für spotifyd/andere Daemons          |
| **cargo**       | Rust-Paketmanager, Installation von spotify-tui/spotifyd möglich|

**Hinweis:** Diese Liste umfasst alle im Architektur- und Testplan genannten Tools. Für Details siehe jeweilige Abschnitte oben.

## 12. spotipy – Installation & Schnelltest

### 1. Standard-Installation mit pip
Im Terminal (im gewünschten venv/Python-Env):
```bash
pip install spotipy
```
Für ein Upgrade auf die neueste Version:
```bash
pip install spotipy --upgrade
```

### 2. Installation mit conda (optional)
Falls du Anaconda/Miniconda nutzt:
```bash
conda install -c conda-forge spotipy
```
Oder via pip innerhalb der conda-Umgebung:
```bash
pip install spotipy
```

### 3. Mini-Test, ob spotipy funktioniert
```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
print(spotipy.__version__)
```
Wenn kein `ModuleNotFoundError` kommt, ist spotipy korrekt installiert.

### 4. Hinweis: Client-ID/Secret als Umgebungsvariablen
Für sichere Skripte empfiehlt es sich, Spotify-Client-ID und -Secret als Umgebungsvariablen zu setzen:
```bash
export SPOTIPY_CLIENT_ID="..."
export SPOTIPY_CLIENT_SECRET="..."
export SPOTIPY_REDIRECT_URI="http://localhost:8888"
```

**Tipp:** Sag Bescheid, ob du venv, conda oder systemweit arbeitest – dann folgt ein self-contained spotipy-Setup für dein Musik-Projekt!
1. spotifyd manuell installieren
Führe in deiner Shell (z. B. dein Projekt‑Ordner) aus:

bash
# 1. Download (x86_64)
wget https://github.com/Spotifyd/spotifyd/releases/latest/download/spotifyd-linux-x86_64.tar.gz

# 2. Entpacken
tar xzf spotifyd-linux-x86_64.tar.gz

# 3. Binary systemweit installieren (z. B. /usr/local/bin)
sudo chmod +x spotifyd
sudo mv spotifyd /usr/local/bin/spotifyd

# 4. Teste
spotifyd --version
Jetzt kannst du spotifyd immer aufrufen.

2. Konfiguration erstellen
bash
mkdir -p ~/.config/spotifyd
vim ~/.config/spotifyd/spotifyd.conf
Beispiel‑Minimal‑Config (für PulseAudio‑Systeme):

text
[global]
username = "dein_spotify_email"
password = "dein_spotify_pass"
device_name = "my-spotifyd"

[playback]
backend = "alsa"
device = "default"
volume_controller = "softvol"
backend anpassen:

PulseAudio: backend = "pulseaudio"

ALSA: backend = "alsa"


3. spotifyd testweise starten
bash
spotifyd --no-daemon
Dann in Spotify‑App (Handy oder Desktop) unter „Geräte“ sollte my-spotifyd auftauchen.

4. Optional: Als systemd‑Service (für dein System)
bash
sudo cp /usr/local/bin/spotifyd /opt/spotifyd
sudo cp ~/.config/spotifyd/spotifyd.conf /etc/spotifyd.conf

sudo tee /etc/systemd/system/spotifyd.service << 'EOF'
[Unit]
Description=A Spotify playing daemon
Wants=sound.target
After=sound.target network-online.target
Wants=network-online.target

[Service]
ExecStart=/opt/spotifyd --no-daemon
Restart=always
RestartSec=12

[Install]
WantedBy=default.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now spotifyd.service
Damit läuft spotifyd im Hintergrund und ist immer als Gerät sichtbar.

Wenn du willst, schick mir kurz den Auszug von:

bash
cat /etc/os-release
und sag mir, ob du PulseAudio oder ALSA nutzt (pactl info vs. aplay -l); dann passe ich dir Configuration und Service‑Datei exakt auf dein Setup an.

## 13. swyh-rs – System-Audio per UPnP/DLNA streamen

**swyh-rs** ("Stream What You Hear – Rust") ist ein modernes, plattformübergreifendes Tool, das den System-Audio-Stream deines Rechners per UPnP/DLNA/OpenHome ins Netzwerk streamt.

### 1. Was macht swyh-rs?
- Nimmt den System-Sound ("Was du hörst") auf
- Streamt ihn an Netzwerk-Renderer (z. B. Sonos, Volumio, Chromecast Audio, UPnP-Receiver)
- Ermöglicht z. B. Spotify, YouTube, lokale Player auf beliebige Netzwerk-Lautsprecher zu bringen

### 2. Installation & Nutzung
- GitHub: [https://github.com/dheijl/swyh-rs](https://github.com/dheijl/swyh-rs)
- Download passende Binary (Linux/Windows) aus den Releases
- Starten (GUI-Anwendung)
- Automatischer Scan nach UPnP/DLNA-Geräten im Netzwerk
- Renderer auswählen (z. B. Volumio, Sonos Kitchen) und Stream starten

### 3. Typischer Einsatz im Mediaplayer-Setup
- Bottle-/Eel-Frontend spielt Playlists/lokale Medien ab
- swyh-rs läuft parallel und streamt den gesamten System-Audio (inkl. Spotify, Browser, Player) zu Netzwerk-Renderern
- Ideal für Multiroom, Sonos, Volumio, Chromecast Audio etc.

### 4. Hinweise
- Funktioniert auf Linux und Windows
- Zielgerät: Volumio, Sonos, Chromecast, DLNA-Receiver etc.
- Keine Installation nötig, einfach Binary ausführen

**Tipp:** Für ein konkretes Setup-Beispiel (Download, Start, Zielgerät) einfach gewünschtes Zielsystem nennen!

## 14. swyh-rs-cli – Headless System-Audio-Streaming per CLI

**swyh-rs-cli** ist die Kommandozeilen-Variante von swyh-rs und ermöglicht System-Audio-Streaming komplett ohne GUI – ideal für Server, Headless-Setups und Automatisierung.

### 1. Headless CLI-Mode
- Startet ohne grafische Oberfläche, läuft im Terminal oder als Daemon
- Steuerung über Kommandozeilen-Optionen (Audioquelle, Format, Zielgerät etc.)

### 2. Typische Optionen (Linux/Server)
- `-s <index>` / `--source <index>`: Audioquelle wählen (Indexe mit `-n` anzeigen)
- `-f <format>`: Format (lpcm, wav, rf64, flac)
- `-b <bits>`: Auflösung (z. B. 16 oder 24 Bit)
- `-c <config_id>`: Mehrere Konfigurationen parallel
- `-x` / `--serve_only`: Nur UDP-Server, kein SSDP-Discovery (Renderer ruft Stream ab)

**Beispiel:**
```bash
swyh-rs-cli --source 0 --format flac --bits 16 --config_id 1
```

### 3. Integration im Mediaplayer-Setup
- swyh-rs-cli als headless Daemon (z. B. systemd-Service) auf dem Server
- System-Audio (inkl. Spotify, Browser, Player) als Quelle
- UPnP/DLNA-Renderer (Volumio, Sonos, BubbleUPnP, Chromecast-Server) empfängt den Stream

### 4. Beispiel: systemd-Service-Template
```ini
# /etc/systemd/system/swyh-rs-cli.service
[Unit]
Description=swyh-rs CLI (Stream What You Hear) headless daemon
After=network.target sound.target

[Service]
User=xc
Environment="HOME=/home/xc"
ExecStart=/usr/local/bin/swyh-rs-cli --source 0 --format flac --bits 16 --config_id 1
Restart=always

[Install]
WantedBy=multi-user.target
```
Aktivieren mit:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now swyh-rs-cli.service
```

**Tipp:** Für ein kopierfertiges Kommando + Service-Config einfach Zielsystem und Renderer nennen!

## 15. Lyrion Music Server – Moderner Open-Source-UPnP/DLNA-Server

**Lyrion Music Server** (früher: upmpdcli) ist ein moderner, plattformübergreifender Open-Source-UPnP/DLNA/MediaRenderer-Server für Musik-Streaming im Heimnetz.

### 1. Überblick & Features
- UPnP/DLNA-Server und Renderer (empfängt und streamt Musik im Netzwerk)
- Unterstützt lokale Musikbibliotheken, Streaming-Dienste (Qobuz, Tidal, HRA, Radio Paradise u. a.)
- Kompatibel mit OpenHome (z. B. Linn, BubbleUPnP)
- Integration mit MPD (Music Player Daemon) für lokale Wiedergabe
- Web-UI und API für Steuerung und Verwaltung

### 2. Typische Einsatzszenarien
- Musik-Streaming zu Netzwerk-Playern (z. B. Volumio, Sonos, Smart Speaker)
- Multiroom-Setup im Heimnetz
- Integration in bestehende Mediaplayer- oder Home-Automation-Umgebungen

### 3. Integration im Mediaplayer-Setup
- Lyrion als zentraler Musikserver für lokale und Streaming-Inhalte
- Steuerung via Web-UI, Apps (BubbleUPnP, Linn Kazoo, etc.) oder API
- Kombinierbar mit swyh-rs, spotifyd, spotipy für flexible Multiroom- und Streaming-Lösungen

### 4. Links & Ressourcen
- Projektseite: [https://www.lyrion.org/](https://www.lyrion.org/)
- GitHub: [https://github.com/lyrion-org/lyrion-music-server](https://github.com/lyrion-org/lyrion-music-server)
- Doku: [https://www.lyrion.org/doc/](https://www.lyrion.org/doc/)

**Tipp:** Lyrion eignet sich als universeller Musikserver für anspruchsvolle Multiroom- und Streaming-Setups im Heimnetz.

## 16. swyh-rs-cli – Detaillierte CLI-Referenz & Tipps

### 1. Wichtige CLI-Optionen (ab v1.7.0)
- `-h` / `--help`: Hilfe/Usage anzeigen
- `-n` / `--no-run`: Dry-run, zeigt verfügbare Soundquellen/Player, startet keinen Stream
- `-c` / `--config_id` <string>: Konfigurations-ID (für parallele Instanzen)
- `-C` / `--configfile` <string>: Alternativer Pfad zur Config-Datei
- `-p` / `--server_port` <u16>: Port für HTTP-Streaming (Default: 5901)
- `-a` / `--auto_reconnect` <bool>: Automatisch neu verbinden (Default: true)
- `-r` / `--auto_resume` <bool>: Automatisch Wiedergabe fortsetzen (Default: false)
- `-s` / `--sound_source` <index|name>: Audioquelle (Index oder Name, mit -n anzeigen)
- `-l` / `--log_level` <string>: Log-Level (info/debug)
- `-i` / `--ssdp_interval` <i32>: SSDP-Discovery-Intervall in Minuten
- `-b` / `--bits` <u16>: Bit-Tiefe (16/24, Default: 16)
- `-f` / `--format` <string>: Streaming-Format (lpcm, flac, wav, rf64)
- `-o` / `--player_ip` <string>: Zielgerät (IP oder Name, auch Substring möglich)
- `-e` / `--ip_address` <string>: Netzwerk-Interface (IP)
- `-x` / `--serve_only`: Kein SSDP, sofort als Server starten (Renderer ruft Stream ab)
- `-u` / `--upfront-buffer` <i32>: Initiales Buffering vor Streamstart

**Tipp:** Mit `-n` (dry-run) bekommst du die Indizes/Namen der Soundquellen und Player angezeigt.

### 2. Soundquellen & Player-Auswahl
- Soundquelle: Index, Name oder Substring (bei Mehrfachnamen mit :n für n-tes Vorkommen)
- Player: IP, Name oder Substring (bei mehreren Geräten auch kommasepariert)

### 3. Streaming-Formate & Latenz
- **LPCM**: Geringste Latenz, meist 16 Bit, ideal für Echtzeit (wenn Receiver es unterstützt)
- **WAV/RF64**: Etwas höhere Latenz, evtl. HTTP-Request zu Beginn
- **FLAC**: Höchste Latenz, aber weniger Netzlast, besser bei instabilem WLAN
- **Chunked/NotChunked**: Für unbegrenzte Streamdauer ggf. NoneChunked verwenden

### 4. Headless- & Multi-Instance-Betrieb
- Mit `-c` verschiedene Konfigs/Instanzen parallel starten (z. B. für mehrere Quellen)
- Mit `-x` als reiner Streaming-Server ohne Discovery (Renderer ruft Stream ab)
- Stoppen nur durch Prozess-Kill (CTRL+C, kill, Task-Manager)

### 5. Beispielaufruf
```bash
swyh-rs-cli --source 0 --format flac --bits 16 --config_id 1
```

### 6. Tipps
- Für minimale Latenz: LPCM, 16 Bit, stabile Verbindung
- Für weniger Aussetzer bei WLAN: FLAC wählen
- Mit -n/-h alle verfügbaren Optionen und Geräte anzeigen lassen
- Einmal funktionierende Config kann gespeichert und wiederverwendet werden

**Quelle & weitere Details:** [https://github.com/dheijl/swyh-rs](https://github.com/dheijl/swyh-rs)

## 17. Audioaufnahme – Hinweis & Alternativen

**swyh-rs** unterstützt keine Audioaufnahme (Recording), sondern nur das Streamen des System-Audios zu Netzwerk-Renderern.

Für Audioaufnahmen (z. B. Mitschnitt von System-Sound) empfiehlt sich ein spezialisiertes Tool wie **Audacity**.

### Audacity – Aufnahme von Computer-Sound
- Plattformübergreifend, Open Source, sehr leistungsfähig
- Unterstützt direkte Aufnahme von "Was du hörst" (je nach Betriebssystem und Soundkarte)
- Umfangreiche Bearbeitungs- und Exportfunktionen

**Links:**
- [Audacity: Computer-Sound aufnehmen (Windows)](https://manual.audacityteam.org/man/tutorial_recording_computer_playback_on_windows.html)
- [Audacity: Aufnahme-Längenbegrenzung](https://manual.audacityteam.org/man/recording_length.html)
- [swyh-rs Issue #44: Keine Aufnahmefunktion](https://github.com/dheijl/swyh-rs/issues/44)

**Fazit:** Für Recording immer Audacity oder ein vergleichbares Tool nutzen – swyh-rs ist rein für Streaming gedacht.

## 18. Equalizer unter Linux – Systemweit für Mediaplayer & Spotify

### 1. Gängige Equalizer-Lösungen
| Lösung             | Empfohlen für                                   | Typisch für             |
|--------------------|-------------------------------------------------|-------------------------|
| **PulseEffects**   | PulseAudio-/PipeWire-Systeme, GUI + viele Effekte | Desktop-Nutzer  [flathub](https://flathub.org/en/apps/com.github.wwmm.pulseeffects) |
| **alsaequal**      | ALSA-direktes Equalizer-Plugin (`~/.asoundrc`)    | ALSA-basierte Systeme  [baeldung](https://www.baeldung.com/linux/sound-equalizers) |
| **system-wide LADSPA** / `pulseaudio-equalizer-ladspa` | PulseAudio-Equalizer-Plugin ohne GUI, systemweit  [bbs.archlinux](https://bbs.archlinux.org/viewtopic.php?id=247109) |
| **VLC-/Spotify-EQ** | Nur innerhalb der App (systemweit besser via PulseEffects)  [gutefrage](https://www.gutefrage.net/frage/was-ist-der-beste-equalizer-und-audiomixer-fuer-linux) |

### 2. Beispiel: PulseEffects (empfohlen)
- **Installation:**
  ```bash
  flatpak install flathub com.github.wwmm.pulseeffects
  ```
- **Einrichtung:**
  - PulseEffects starten, PulseAudio-Sink wählen
  - Equalizer aktivieren, andere Effekte ggf. deaktivieren
  - Profil speichern (gilt für alle System-Sounds)
- **Wirkt auf:**
  - spotifyd-Audio
  - Browser-Spotify
  - Eel-Bottle-Player
  - ...alles, was über PulseAudio läuft

### 3. ALSA-Equalizer (`alsaequal`)
- **Installation:**
  ```bash
  git clone --depth 1 https://github.com/raedwulf/alsaequal
  cd alsaequal
  make && sudo make install
  ```
- **~/.asoundrc Beispiel:**
  ```
  ctl.equal {
    type equal;
  }
  pcm.plugequal {
    type equal;
    slave.pcm "plughw:0,0";
  }
  pcm.equal {
    type plug;
    slave.pcm plugequal;
  }
  ```
- **Anwendung:**
  - Über `aplay`, `alsaplayer`, `mplayer` mit `pcm.plugequal` als Ausgabe

### 4. Empfehlung für dein Setup
- System-Equalizer via PulseEffects (PulseAudio/PipeWire) einrichten
- spotifyd, swyh-rs, Browser-Spotify, Mediaplayer nutzen denselben Audio-Pfad → EQ gilt für alles
- Optional: Musik-Profil (z. B. Bass, Höhen) speichern

**Tipp:** Bei Angabe deines Audio-Stacks (PulseAudio, ALSA, PipeWire) kann ein exakter Setup-Weg (inkl. Config) geliefert werden!

## 19. Equalizer-Integration in der Bottle/Eel-App: Systemweit vs. Player-spezifisch

### 1. Systemweiter Equalizer (PulseEffects / alsaequal)
- Kein zusätzlicher Code in der App nötig
- Einmalige Einrichtung (z. B. PulseEffects, alsaequal)
- Gilt für alle Audioquellen: Browser, spotifyd, Eel-Player etc.
- Ideal für zentrale Mediaplayer-Server und „alles klingt gleich gut“-Ansatz
- [baeldung: Linux Sound Equalizer](https://www.baeldung.com/linux/sound-equalizers)

### 2. JS-Equalizer direkt im Player (Web Audio API)
- Nur für den eigenen Mediaplayer-Tab/Fenster
- Unabhängig vom System-EQ
- Beispiel (Vanilla-JS, Web Audio API):
```js
// player.js – Beispiel-Equalizer (Parametric EQ)
class PlayerEQ {
  constructor(context) {
    this.ctx = context;
    // z. B. Bänder: 100 Hz, 1 kHz, 10 kHz
    this.filters = [
      this.makeFilter("low", 100, 1.0),
      this.makeFilter("mid", 1000, 1.0),
      this.makeFilter("high", 10000, 1.0)
    ];
  }
  makeFilter(id, freq, gain) {
    const f = this.ctx.createBiquadFilter();
    f.type = "peaking";
    f.frequency.value = freq;
    f.Q.value = 1.0;
    f.gain.value = gain;
    return {id, node: f};
  }
  connect(inputStream) {
    let last = inputStream;
    this.filters.forEach(f => {
      last.connect(f.node);
      last = f.node;
    });
    return last;
  }
  setBandValue(bandId, value) {
    const entry = this.filters.find(f => f.id === bandId);
    if (entry) entry.node.gain.value = value;
  }
}
// Beispiel: MediaElement → EQ → destination
const audioCtx = new AudioContext();
const playerEQ = new PlayerEQ(audioCtx);
const source = audioCtx.createMediaElementSource(document.getElementById("audio"));
const eqOut = playerEQ.connect(source);
eqOut.connect(audioCtx.destination);
// Slide-Regler (HTML) ändern via:
// playerEQ.setBandValue("low", 3);  // 3 dB Zusatz bei 100 Hz
```
- Einbindung eines HTML-EQ-Panels möglich (z. B. für Bass/Mitten/Höhen)
- [gutefrage: Equalizer für Linux](https://www.gutefrage.net/frage/was-ist-der-beste-equalizer-und-audiomixer-fuer-linux)

### 3. Entscheidungshilfe
- **System-EQ:** Für globalen Sound, alles klingt gleich, keine App-Änderung nötig
- **JS-EQ:** Nur für den eigenen Player, flexibel für Presets, unabhängig vom System

**Tipp:** Bei Angabe deines Audio-Stacks (PulseAudio, ALSA, PipeWire) und EQ-Präferenz kann ein fertiges Setup (JS-Modul oder System-EQ-Config) geliefert werden!

## 21. Fertige Python-Equalizer-Module & Frameworks für das Backend

### 1. Einfache, fertige Python-EQ-Pakete
#### a) `pyequalizer` (scipy-basiert)
- Equalizer für WAV-Dateien, arbeitet mit scipy/NumPy
- Frequenzbereiche, Gewichtungskurven, viele Bänder
- [pypi: pyequalizer](https://pypi.org/project/pyequalizer/)
**Beispiel:**
```bash
pip install pyequalizer
```
```python
import pyequalizer.Filter as Filter
import librosa
y, sr = librosa.load("input.wav", sr=44100)
y_eq = Filter.equalizer(
    y, sr,
    start_iv=200, end_iv=8000,
    num_iv=100,
    peak_scale=20, peak_iv=20,
    type="parabola"
)
```
→ Gut für Datei-basierte Equalizer, z. B. für lokale Medienvorverarbeitung.

#### b) `awesome-audio-equalizer` (GUI, Windows-orientiert)
- Python-GUI-Equalizer für System-Sound (Windows), aber Filter-Logik als Referenz nutzbar
- [github: awesome-audio-equalizer](https://github.com/Hyper5phere/awesome-audio-equalizer)

### 2. Echtzeit-Audio-Processing-Frameworks
#### a) `pedalboard` (Spotify)
- Audio-Processing-Plugins, inkl. Gain, Filter, Reverb, EQ-ähnliche Effekte
- [github: pedalboard](https://github.com/spotify/pedalboard)
**Beispiel:**
```bash
pip install pedalboard
```
```python
import pedalboard
import librosa
board = pedalboard.Pedalboard([
    pedalboard.Gain(gain_db=3.0),
    # weitere Filter/Plugins möglich
])
y, sr = librosa.load("input.wav", sr=48000)
y_eq = board(y, sr)
```

#### b) Weitere Beispiele/Repos
- [Audio-Equalizer (tkinter)](https://github.com/mayank12gt/Audio-Equalizer)
- [sound-equalizer (PyQt5)](https://github.com/rohitjoshi21/sound-equalizer)
- [StackOverflow: Audio-Equalizer](https://stackoverflow.com/questions/54932976/audio-equalizer)

### 3. Vorschlag für dein Setup
- Für das Backend (Eel/Bottle-Server):
  - Nutze `pyequalizer` oder ein eigenes `eq_backend.py` (inspiriert von o. g. Beispielen)
  - Implementiere eine Funktion `apply_eq(bands=...)`
  - Diese kann von der Eel-App per Hook aufgerufen werden
  - Ergebnis: internes Audio-Processing oder Preset-Steuerung für System-EQ-Tools (z. B. PulseEffects per Skript)

**Tipp:** Bei Angabe, ob Datei-basierter oder Echtzeit-EQ gewünscht ist, kann ein fertiges Python-Modul (inkl. pip-Paket und eel-Hook) geliefert werden!

## 22. mpv als leistungsfähiger Backend-Player (Audio/Video) für Bottle/Eel

### 1. Was mpv bringt
- Open-Source-Mediaplayer (FFmpeg-basiert, MPlayer/mplayer2-Nachfolger)
- Unterstützt fast alle Formate (Audio, Video, Streams, YouTube via yt-dlp)
- Hochwertige Videoausgabe, viele Filter, Scripting (Lua, Python), Konfigurierbarkeit
- Steuerbar via Kommandozeile, mpv.conf, input.conf, JSON-IPC

### 2. mpv als Backend-Player in deinem Setup
- mpv wird als Subprozess vom Python-Backend gestartet:
  ```python
  subprocess.Popen(["mpv", "--no-video", "datei.mp3"])
  # oder für Video: ["mpv", "datei.mkv"]
  ```
- Eel-Frontend steuert mpv über exposed Python-Methoden (Play, Pause, Seek, EQ)
- Für fortgeschrittene Steuerung: mpv im Idle-Modus mit JSON-IPC-Socket starten

### 3. Audio-Equalizer in mpv nutzen
- mpv bietet FFmpeg-basierte Audiofilter, z. B. superequalizer (18-Band-EQ)
- Beispiel (Kommandozeile):
  ```bash
  mpv --af="superequalizer=1b=3:2b=4:...:18b=8" datei.mp4
  ```
- Oder in ~/.config/mpv/mpv.conf:
  ```
  af=superequalizer=1b=3:2b=4:...:18b=8
  ```
- EQ-Presets für verschiedene Genres möglich

### 4. Integration in die App-Logik (Python-Backend)
**Beispiel:**
```python
# player_backend.py
import subprocess
import json
class MPVPlayer:
    def __init__(self):
        self.proc = subprocess.Popen([
            "mpv",
            "--idle",
            "--no-terminal",
            "--input-ipc-server=/tmp/mpv.sock"
        ])
    def send_cmd(self, cmd):
        data = json.dumps(cmd)
        with open("/tmp/mpv.sock", "w") as f:
            f.write(data + "\n")
    def play(self, path):
        self.send_cmd({"command": ["loadfile", path]})
    def set_eq(self, af_filter):
        self.send_cmd({"command": ["set_property", "af", af_filter]})
```
- Eel-Expose:
  ```python
  @eel.expose
  def web_play(path):
      player_backend.play(path)
  ```
- EQ-Presets können als Strings (z. B. "superequalizer=...") übergeben werden

### 5. Hinweise für dein Setup
- mpv eignet sich als Audio- und Video-Backend (je nach Bedarf)
- Steuerung via IPC ermöglicht Play, Pause, Seek, EQ, Playlist etc.
- Für reine Audio-Setups: mpv mit --no-video starten
- Für Video-UI: mpv-Fenster kann im App-Mode angezeigt werden

**Tipp:** Bei Angabe, ob nur Audio oder auch Video gewünscht ist, kann ein fertiges mpv-Backend-Modul mit eel-Hooks und EQ-Steuerung geliefert werden!

## 23. Integration: video.js + mpv als Backend-Engine

### 1. Szenarien: "video.js + mpv"
- **Variante A (empfohlen):**
  - Frontend nutzt `video.js` als Browser-Player (HTML5-Video, HLS, Streams)
  - Backend nutzt `mpv` als Media-/Transcoding-Engine (Audio-EQ, Metadaten, ggf. HLS-Streaming)
- **Variante B (fortgeschritten):**
  - mpv läuft als HLS-/RTSP-Server, `video.js` streamt direkt von mpv

### 2. Empfohlene Architektur
- `video.js` im Browser als UI/Player
- `mpv` im Backend für Audio-/Video-Processing, EQ, ggf. Streaming
- Fluss: User wählt Datei → Backend startet mpv (mit EQ/Filter) → mpv erzeugt HLS-Stream → video.js spielt Stream ab

### 3. Beispiel: mpv als HLS-Streamer + video.js-Frontend
**Backend (Python, pseudo-bottle):**
```python
import subprocess
def start_stream(input_path, stream_id):
    cmd = [
        "mpv",
        "--no-audio",
        "--stream-lavf-o="
            "hls_segment_filename=/tmp/segment-%03d.ts&"
            "hls_segment_type=mpegts&"
            "hls_flags=DELETE_SEGMENTS&"
            "hls_flags=independent_segments&"
            "hls_time=5&"
            "hls_list_size=3&"
            "hls_target_duration=5",
        input_path,
        "--stream-lavf-format=hls",
        "--stream-lavf-name=/tmp/stream_" + stream_id + ".m3u8",
        "--no-terminal"
    ]
    subprocess.Popen(cmd)
```
**Frontend (video.js):**
```html
<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<link href="https://vjs.zencdn.net/8.10.0/video-js.min.css" rel="stylesheet">
<video id="video-player" class="video-js vjs-default-skin" controls preload="auto" width="800" height="450"></video>
<script>
  const player = videojs('video-player', {
    autoplay: false,
    controls: true,
    sources: [{
      src: 'http://127.0.0.1:8080/stream/hls/xyz.m3u8',
      type: 'application/x-mpegURL'
    }]
  });
</script>
```
**Backend-Routing (bottle/flask):**
```python
@app.route('/stream/hls/<id>.m3u8')
def stream_hls(id):
    manifest = f"/tmp/stream_{id}.m3u8"
    return static_file(manifest)
@app.route('/stream/segment-<id>.ts')
def stream_ts(id):
    # Segmente aus /tmp/segment-*.ts senden
    ...
```

### 4. mpv als Audio-EQ-Engine
- mpv kann als reiner Audio-EQ-Prozess laufen (z. B. mit --af="superequalizer=...")
- video.js spielt Video, mpv bearbeitet Audio im Hintergrund
- Steuerung via eel-Hooks und Backend-API

### 5. Hinweise
- mpv eignet sich als Audio-/Video-Backend, Transcoder, EQ-Engine
- video.js bleibt UI/Player im Browser
- Für Audio-EQ oder HLS-Streaming kann ein fertiges Beispiel geliefert werden – einfach Use-Case angeben!

## 24. mpv.js & mpvPlayer.js – Unterschiede, Integration, Relevanz

### 1. Kagami/mpv.js (libmpv im Browser/Electron)
- GitHub: [Kagami/mpv.js](https://github.com/Kagami/mpv.js)
- Wrapper für libmpv als Pepper-Plugin/WebComponent
- Ermöglicht mpv-Funktionalität in Electron-/Chromium-Apps (z. B. ReactMPV)
- Relevanz: Nur sinnvoll, wenn du eine Electron-/Chromium-Shell-App mit nativer mpv-Integration bauen willst
- Ablauf: libmpv installieren → mpv.js npm-Package → Integration in Electron/React

### 2. mpvPlayer.js (kommerzieller HTML5-Player)
- Externer Video-Player-Service, kein Bezug zum mpv-CLI-Player
- Einbindung wie ein klassischer HTML5-Player (z. B. video.js)
- Beispiel:
  ```html
  <script src="https://.../mpvPlayer.js"></script>
  <div id="mvpplayer"></div>
  <script>
    var player = new mpvPlayer({ id: "mvpplayer", file: "https://example.com/video.mp4" });
  </script>
  ```
- Relevanz: Nur, wenn du einen externen Player-Service nutzen willst

### 3. Empfehlung für dein Setup
- Für Eel-/Bottle-App mit Vanilla-JS-/video.js-Player und mpv als Backend:
  - **Nutze video.js im Browser** als UI/Player
  - **Nutze mpv im Backend** als EQ-/Transcoder-/Streaming-Engine (CLI/IPC)
  - mpv.js/mpvPlayer.js sind nicht nötig, außer du willst explizit Electron-/Chromium-Shell oder externen Service

### 4. Hinweise
- mpv.js ist für Electron-/Chromium-Apps mit nativer mpv-Integration
- mpvPlayer.js ist ein externer HTML5-Player, kein echter mpv-Backend-Player
- Für klassische Web-/Eel-Apps: video.js + mpv-Backend ist der pragmatische Weg

**Tipp:** Bei Bedarf an Electron-/Chromium-Shell oder nativer mpv-Integration kann ein passendes mpv.js- oder video.js/mpv-Backend-Beispiel geliefert werden!

## 25. mpv.js im Kontext Bottle/Eel: Zusammenfassung & Beispiel

### 1. Was ist mpv.js?
- **Kagami/mpv.js**: Wrapper für libmpv als Pepper-Plugin/WebComponent, gedacht für Electron-/Chromium-Shell-Apps ([GitHub](https://github.com/Kagami/mpv.js/))
- **mpvPlayer.js**: Kommerzieller HTML5-Player-Service, kein Bezug zum mpv-CLI-Player ([mpvplayer.com](https://mpvplayer.com))

### 2. Sinnvolle Architektur für dein Setup
- **Im Browser:**
  - `video.js` (oder HTML5-Player) als Video-UI
- **Im Backend (Bottle/Eel):**
  - `mpv` als Backend-Prozess (CLI/IPC) für EQ, Filter, Transcoding, Presets

### 3. Beispiel: mpv-Backend-Steuerung aus Eel-App
**Backend (mpv_backend.py):**
```python
import subprocess
import json
# mpv im Hintergrund starten
proc = subprocess.Popen([
    "mpv",
    "--idle",
    "--no-terminal",
    "--input-ipc-server=/tmp/mpv.sock"
])
def send_cmd(cmd_dict):
    data = json.dumps(cmd_dict)
    with open("/tmp/mpv.sock", "w") as f:
        f.write(data + "\n")
# Beispiel: Play-Funktion
@eel.expose
def play_video(path):
    cmd = {"command": ["loadfile", path]}
    send_cmd(cmd)
```
**Frontend (video.js-Player):**
```html
<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<link href="https://vjs.zencdn.net/8.10.0/video-js.min.css" rel="stylesheet">
<video id="video-player" class="video-js vjs-default-skin" controls preload="auto"></video>
<script>
  const player = videojs('video-player');
  async function web_play(path) {
    await eel.play_video(path)();
  }
  // Beispiel-Aufruf
  web_play('/pfad/zu/video.mkv');
</script>
```

### 4. Wann mpv.js sinnvoll ist
- Nur bei Electron-/Chromium-Shell-Apps mit nativer mpv-Integration
- Für klassische Eel-/Bottle-Apps: video.js + mpv-Backend ist der pragmatische Weg

**Tipp:** Bei Angabe, ob Electron-Integration oder klassisches Eel-/Bottle-Setup gewünscht ist, kann ein passendes Beispiel-Repo/Setup geliefert werden!

## 26. Electron-Integration mit mpv.js: Architektur, Vorteile, Beispiel-Setup

### 1. Was bedeutet der Wechsel zu Electron + mpv.js?
- Eel wird durch Electron als App-Shell ersetzt (Window-Manager, main.js, preload.js)
- mpv.js (Kagami/mpv.js) nutzt libmpv als Video-Player-Komponente in Electron/Chromium
- Backend-Logik (z. B. Metadaten, Playlists) bleibt in Python (Bottle/REST)

### 2. Vergleich: Eel-Bottle vs. Electron + mpv.js
| Aspekt          | Eel-Bottle                             | Electron + mpv.js                        |
|-----------------|----------------------------------------|------------------------------------------|
| Shell/Fenster   | bottle/eel + Chromium-App-Mode         | electron main-Prozess + BrowserWindow    |
| Player-Engine   | video.js im Browser                    | mpv.js (libmpv) als Electron-Komponente  |
| Steuerung       | eel.expose/eel in Python               | ipcRenderer/ipcMain in JS/TS + Node-Backend |

### 3. Beispiel-Architektur (Electron + mpv.js)
- **Electron-Main-Prozess (main.js):**
  - Startet BrowserWindow, lädt HTML/JS-Frontend
  - Steuert Python-Backend über REST/Sockets
- **Frontend (React/JS/TS, mpv.js):**
  ```js
  import mpv, { MPV, ReactMPV } from 'mpv.js';
  const player = new MPV({ container: document.getElementById('mpv-container') });
  player.load('file:///path/to/video.mp4');
  // Steuerung: player.play(), player.pause(), player.seek(seconds)
  ```
- **Python-Backend (Bottle):**
  - Läuft separat als HTTP-Server
  - Electron-Frontend ruft REST-Endpoints auf
  ```python
  from bottle import route, run
  @route('/play/<path>')
  def play(path):
      # Sende IPC/CLI-Befehl an mpv
      ...
      return {"status": "playing"}
  ```
  ```js
  fetch('http://localhost:8080/play/' + encodeURIComponent(path));
  ```

### 4. Vorteile für dein Setup
- mpv-Funktionalität direkt in der App (Equalizer, Filter, Video/Audio-Sync, Codecs)
- Wiederverwendbarer Code, mpv.js übernimmt libmpv-Integration
- Bessere Kontrolle via Electron-IPC (Steuerung, Logging, EQ)

### 5. Hinweise für den Umstieg
- Vollständiger Wechsel zu Electron möglich (Bottle-Backend als REST-Server)
- Alternativ: Eel im Hintergrund, Electron als Frontend-Shell
- Bei Angabe, ob Eel-Funktionalität erhalten bleiben oder komplett Electron genutzt werden soll, kann ein minimales Beispiel-Setup (main.js, package.json, mpv.js, Python-Backend) geliefert werden!
