# 🛠️ Alternative Test- und Routing-Pipeline: ffmpeg, mkvmerge, MediaMTX

Eine alternative Test- und Routing-Pipeline kann die drei Schwergewichte so nutzen:

- **ffprobe**: reine Analyse (wie oben)
- **ffmpeg**: Remux/Transcode-Tests + HLS
- **mkvmerge**: MKV-„Sanitizer“ / Track-Fixer
- **MediaMTX (mtx)**: RTSP-/UDP-Streaming für VLC/ffplay-Modi

---

## 1. ffmpeg-Variante in der Suite

Statt nur zu prüfen, ob Direct Play geht, kannst du aktiv testen, ob **Remux/HLS/RTSP** funktioniert:

```python
def ffmpeg_remux_test(src):
    out = src.rsplit('.', 1)[0] + ".__test__.mp4"
    cmd = ["ffmpeg", "-y", "-i", src, "-c", "copy", "-movflags", "+faststart", out]
    res = subprocess.run(cmd, capture_output=True)
    ok = (res.returncode == 0 and os.path.getsize(out) > 0)
    if ok:
        return out
    return None

def ffmpeg_hls_test(src):
    out_dir = "/tmp/hls_test"
    os.makedirs(out_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-c:v", "libx264", "-preset", "veryfast",
        "-f", "hls", "-hls_time", "4", "-hls_list_size", "3",
        f"{out_dir}/test.m3u8",
    ]
    res = subprocess.run(cmd, capture_output=True)
    ok = (res.returncode == 0 and len(glob.glob(f"{out_dir}/*.ts")) > 0)
    return ok
```

Die Suite kann dann sagen: „Remux OK, HLS OK → Browser-Pfad stabil“.

---

## 2. mkvmerge-Variante für „kaputte“ MKVs

Vor ffmpeg/HLS kannst du MKVs optional durch mkvmerge jagen, um Container-Probleme zu bereinigen (Timecodes, Header, seltsame Extra-Tracks).

```python
def mkv_sanitize(src):
    if not src.lower().endswith(".mkv"):
        return src
    out = src.rsplit('.', 1)[0] + ".__fixed__.mkv"
    cmd = ["mkvmerge", "-o", out, "--no-global-tags", "--no-chapters", src]
    res = subprocess.run(cmd, capture_output=True)
    return out if res.returncode == 0 else src
```

Die Test-Suite:

1. ffprobe → sehen, ob MKV verdächtig ist (komische Streams, 0-Dauer etc.).
2. Wenn ja: `fixed = mkv_sanitize(src)` und alle ffmpeg-Tests auf `fixed` ausführen.

---

## 3. MediaMTX-Variante für „Streaming-Modus“

Statt HLS kannst du als Alternative testen, ob ein **RTSP-Stream via MediaMTX** sauber läuft:

```python
def mtx_rtsp_test(src):
    # mtx läuft bereits als Dienst
    cmd = [
        "ffmpeg", "-re", "-i", src,
        "-c", "copy",
        "-f", "rtsp", "rtsp://localhost:8554/test"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(3)
    # z.B. mit ffprobe kurz prüfen, ob der RTSP-Stream lesbar ist
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "rtsp://localhost:8554/test"],
        capture_output=True
    )
    ok = (probe.returncode == 0)
    proc.terminate()
    return ok
```

Damit hast du drei „Pfade“, die die Suite testet:

- **Direct/Remux-Pfad**: ffmpeg-Remux → Direct Play
- **HLS-Pfad**: ffmpeg-HLS → video.js
- **RTSP-Pfad**: ffmpeg → MediaMTX → VLC/ffplay

---

## 4. Routing-Entscheidung aus der erweiterten Suite

Die Suite liefert dir z.B.:

```json
{
  "direct_ok": true,
  "remux_ok": true,
  "hls_ok": true,
  "rtsp_ok": true,
  "mkv_fixed": "/path/to/fixed.mkv"
}
```

Und dein Backend entscheidet:

```python
@eel.expose
def choose_play_mode(relpath, client='browser'):
    full = os.path.join(MEDIA_ROOT, relpath)
    fixed = mkv_sanitize(full)
    tests = {
        "remux_ok": ffmpeg_remux_test(fixed) is not None,
        "hls_ok": ffmpeg_hls_test(fixed),
        "rtsp_ok": mtx_rtsp_test(fixed),
    }

    if client == "browser":
        if tests["remux_ok"]:
            mp4 = ffmpeg_remux_test(fixed)
            rel = os.path.relpath(mp4, MEDIA_ROOT)
            return {"mode": "direct", "url": f"/direct/{rel}"}
        elif tests["hls_ok"]:
            hls_url = get_hls_url(relpath)
            return {"mode": "hls", "url": hls_url}
    # alles andere → VLC/RTSP
    if tests["rtsp_ok"]:
        return {"mode": "vlc-rtsp", "url": "rtsp://localhost:8554/test"}
    return {"mode": "vlc-file", "url": full}
```

---

**Kurz:**

- **ffmpeg**: prüft, ob Remux/HLS klappt und erzeugt die Artefakte.  
- **mkvmerge**: optionaler „Vorfilter“ für problematische MKVs.  
- **MediaMTX**: Streaming-Alternative für Clients im VLC-Pfad.

Das ist die „nächstbeste“ (und ziemlich robuste) Alternative zur reinen ffprobe+Direct-Play-Variante.
