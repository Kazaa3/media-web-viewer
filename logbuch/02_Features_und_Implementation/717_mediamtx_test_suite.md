# MediaMTX Test-Suite: Health, Publish & Read

**Ziel:**
Eine robuste Test-Suite für MediaMTX, die Server-Health, Publish- und Read-Pfade automatisiert prüft – ideal für Integration in Backend, CI oder als Diagnose-Tool.

---

## 1. Server-Health / Konfiguration

- MediaMTX mit aktivierter API starten (`MTX_API=true`, Port 9997).
- Health-Check (API):

```bash
curl -s http://localhost:9997/v3/paths | jq '.items | length'
# > 0 ⇒ Server & API laufen, Paths bekannt
```

- RTSP-Listener-Check:

```bash
nc -z localhost 8554   # Exitcode 0 = Listener offen
```

---

## 2. Publish-Pfad testen (ffmpeg → mtx)

```bash
ffmpeg -re -i /path/to/test.mp4 \
  -c copy -f rtsp rtsp://localhost:8554/teststream
```

- Erwartung: MediaMTX-Logs zeigen `publisher connected on path teststream`.
- Automatisiert (Python):

```python
import subprocess, requests, time

def mtx_publish_test(src):
    proc = subprocess.Popen([
        "ffmpeg", "-re", "-i", src,
        "-c", "copy", "-f", "rtsp", "rtsp://localhost:8554/teststream"
    ])
    time.sleep(2)
    r = requests.get("http://localhost:9997/v3/paths")
    paths = [p["name"] for p in r.json().get("items", [])]
    ok = "teststream" in paths
    proc.terminate()
    return ok
```

---

## 3. Read-Pfad testen (Clientseite)

### a) ffprobe-Health (empfohlen)

```bash
FFPROBE_PARAMS="-v fatal -rtsp_transport tcp -stimeout 5000000 \
  -of compact=print_section=0:item_sep=,:nokey=1 \
  -show_entries stream=codec_name,width,height -select_streams v"

ffprobe $FFPROBE_PARAMS rtsp://localhost:8554/teststream || echo unavailable
```

- Wenn ffprobe Metadaten liefert, ist der Stream lesbar; bei Fehlern → `unavailable`.

### b) ffplay/VLC-Smoke-Test

```bash
ffplay -autoexit -t 5 rtsp://localhost:8554/teststream
# oder
vlc rtsp://localhost:8554/teststream
```

- Automatisiert (Python):

```python
def mtx_read_test(url="rtsp://localhost:8554/teststream"):
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name", "-of", "csv=p=0", url],
        capture_output=True, text=True
    )
    return res.returncode == 0
```

---

## 4. Zusammengefasst als Suite-Resultat

```json
{
  "server_up": true,
  "api_ok": true,
  "publish_ok": true,
  "read_ok": true,
  "streams": ["teststream", "camera1", "cam_frontdoor"]
}
```

- RTSP-Modus im Player nur aktivieren, wenn `publish_ok && read_ok`.
- Bei Problemen automatisch auf HLS/VLC-Direktpfad zurückfallen.

---

**Quellen & Links:**
- [MediaMTX API & Health](https://github.com/bluenviron/mediamtx/discussions/1605)
- [MediaMTX Config](https://raw.githubusercontent.com/bluenviron/mediamtx/main/mediamtx.yml)
- [RTSP Health-Check](https://stackoverflow.com/questions/49002614/is-it-possible-to-do-a-simple-health-check-of-rtsp-stream-with-curl-tool)
- [MediaMTX Publish/Read](https://mediamtx.org/docs/usage/publish)
