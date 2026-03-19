# mpv/mpv.js Integration – Praxis-Logbuch

**Kurz:**
- **Externes mpv: Ja!**
- **mpv.js im normalen Eel/Bottle-Frontend: eher nein/overkill.**

---

## Was gut zu deiner Bottle/Eel/Vanilla-JS-App passt

### 1. mpv als externer Player (empfohlen)
- mpv wird wie VLC/cvlc über Python/Eel gestartet:

```python
import subprocess, json, os

MPV_SOCKET = "/tmp/mpv-socket"

def open_in_mpv(path):
    # mpv mit IPC-Socket starten
    cmd = [
        "mpv", path,
        f"--input-ipc-server={MPV_SOCKET}",
        "--force-window=yes"
    ]
    subprocess.Popen(cmd)

@eel.expose
def mpv_command(command, args=None):
    # JSON-RPC an mpv schicken
    msg = {"command": [command] + (args or [])}
    with open(MPV_SOCKET, "w") as sock:
        sock.write(json.dumps(msg) + "\n")
```

- Im JS-UI einfach als weiteren Button/Modus „In mpv abspielen“ anbieten – Integration fast identisch zu VLC.

### 2. mpv als weiterer „Test-Client“ in der Suite
- Statt nur ffplay/VLC kannst du auch kurz `mpv --no-video file` oder RTSP/HLS testen.
- Gleicher Gedanke wie bei ffplay: nur Smoke-Test, keine GUI-Integration nötig.

---

## Was in deiner Eel/vanilla-JS-App schwierig/unnötig ist

- **mpv.js direkt im Eel-Browserfenster:**
  - mpv.js ist kein normales JS-Plugin wie video.js; es braucht typischerweise eine spezielle Umgebung (Electron/Node, Canvas-Rendering, native Bindings).
  - Eel nutzt ein eingebettetes Chromium/WebView – dort hast du `<video>` + JS, aber keinen direkten mpv-Core.
  - Für deinen Use-Case (HTML-Frontend mit Bottle/Eel) ist video.js + MP4/HLS viel natürlicher und deutlich weniger Gefrickel.

---

## Fazit
- **Ja:** mpv als externer Player ist für Power-User und Testzwecke sehr gut integrierbar (wie VLC/cvlc/ffplay).
- **Eher nein:** mpv.js als eingebetteter Player im gleichen `<video>`-Tab – video.js + Direct-Play/HLS ist technisch und vom Aufwand her besser.
