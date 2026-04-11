# Calibre Content Server: Plex für Ebooks/PDFs

## Schnell-Setup (MX Linux)
1. **Calibre installieren:**
```bash
sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.py | sudo python3
```
2. **Library erstellen:**
```bash
mkdir ~/Calibre-Library
calibredb add ~/Downloads/*.pdf ~/Downloads/*.epub --library-path ~/Calibre-Library
```
3. **Server starten (Port 8080):**
```bash
calibre-server ~/Calibre-Library --port 8080
```
4. **Automatisch als systemd-Service:**
```text
[Unit]
Description=Calibre Content Server
After=network.target

[Service]
Type=simple
User=deinuser
ExecStart=/usr/bin/calibre-server /home/deinuser/Calibre-Library --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now calibre-server
```

---

## Plex-ähnliche Features
| Funktion      | Wie Plex                |
|-------------- |------------------------|
| Web-GUI       | Browser: localhost:8080 – Grid, Suche, Tags! |
| User-Mgmt     | calibre-server --manage-users → Passwort/User |
| Mobile        | OPDS-Katalog für Kobo/Kindle/Apps |
| Upload        | Per Web + E-Mail-to-Library |
| Metadaten     | Auto-Fetch Amazon/Google Books |

---

## Eel-Integration (Hybrid-Library)
**Sync zu Calibre:**
```python
@eel.expose
def sync_to_calibre(pdf_path):
    import subprocess
    subprocess.run(['calibredb', 'add', pdf_path, '--library-path', '/home/user/Calibre-Library'])
    return "Hinzugefügt!"
```
**GUI-Link:**
```javascript
window.open('http://localhost:8080')
```

---

## Calibre-Web Alternative (Plex-Optik)
- `pip install calibreweb` – Docker-ready

---

## Voll-Ökosystem
```
Deine Eel-App (Audio/Bilder) ↔ SQLite-DB ↔ Calibre-Server (PDFs/Ebooks)
                ↓
Chrome: localhost:3000 (Eel) + localhost:8080 (Calibre)
```

---

**Start:**
- calibre-server ~/Calibre-Library → http://localhost:8080 – instant Plex für PDFs!

**Frage:**
Möchtest du User hinzufügen (calibre-server --manage-users) oder die Docker-Version (calibreweb) testen?
