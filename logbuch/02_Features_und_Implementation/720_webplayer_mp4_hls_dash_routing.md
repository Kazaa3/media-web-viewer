# Web-Player: MP4, HLS, DASH – Routing & video.js

**Ziel:**
Drei HTTP-basierte Streaming-Modi (MP4, HLS, DASH) sauber trennen, Backend-Routing und video.js-Konfiguration darauf ausrichten.

---

## 1. Browser-Modi im Überblick

- **Progressives MP4 (Direct Play):**
  - Statische MP4-Datei mit Range-Support, `<source type="video/mp4">`
  - Kein Adaptive Streaming, minimaler Overhead, ideal für LAN/NAS
- **HLS (TS oder fMP4, inkl. mp4frag):**
  - Standardlösung, maximal kompatibel (nativ iOS/Safari, sonst hls.js/videojs-http-streaming)
  - mp4frag: ffmpeg erzeugt fragmentierte MP4, mp4frag splittet in Init + Media-Segmente, erzeugt HLS-m3u8 für fMP4
- **MPEG-DASH (MPD):**
  - Adaptiv, codec-agnostisch, kein natives Apple-Support, nur mit dash.js/videojs-contrib-dash

---

## 2. Routing-Entscheidung im Backend

Erweitere `get_play_plan()` um Streaming-Variante:

```python
def get_play_plan(relpath, client='browser'):
    full = os.path.join(MEDIA_ROOT, relpath)
    a = analyze_media(full)
    # 1. Progressive MP4
    if a['can_direct_play_browser'] and prefer_progressive(a):
        mp4_rel = ensure_mp4_remux(full)
        return {"mode": "http-mp4", "url": f"/direct/{mp4_rel}"}
    # 2. HLS (TS oder fMP4)
    if client_supports_hls(client):
        hls_url = ensure_hls_playlist(full, use_fmp4=True)
        return {"mode": "hls", "url": hls_url}
    # 3. DASH (optional)
    if client_supports_dash(client):
        dash_url = ensure_dash_manifest(full)
        return {"mode": "dash", "url": dash_url}
    # Fallback: VLC/RTSP etc.
    ...
```

- `ensure_hls_playlist(..., use_fmp4=True)`: ffmpeg `-hls_segment_type fmp4` oder mp4frag
- `ensure_dash_manifest(full)`: z.B. Bento4/mp4dash, HLS+DASH aus einem Fragment-Set

---

## 3. video.js-Konfiguration

### Progressives MP4
```js
player.src({ src: plan.url, type: "video/mp4" });
```

### HLS (TS/fMP4, inkl. mp4frag)
```js
player.src({
  src: plan.url,                 // /hls/<id>/index.m3u8
  type: "application/x-mpegURL" // HLS
});
```

### DASH
```js
player.src({
  src: plan.url,                    // /dash/<id>/manifest.mpd
  type: "application/dash+xml"
});
```

---

## 4. Modus-Auswahl im UI

- „Auto (Empfohlen)“ → Backend wählt MP4/HLS je nach Datei/Client
- „HLS (m3u8)“ → erzwingt `mode="hls"`
- „DASH (MPD)“ → falls vorhanden, `mode="dash"`
- „Roh-MP4“ → Debug, progressive only

Beispiel-Plan vom Backend:
```json
{
  "mode": "hls",
  "stream_type": "hls-fmp4",
  "url": "/hls/abcd/index.m3u8",
  "quality_score": 92
}
```

---

## 5. Empfehlung für deine App

- **Basis:** progressive MP4 + HLS (TS/fMP4) für maximale Kompatibilität
- **mp4frag/fMP4:** sinnvoll für Live/Kamera, da HLS und DASH aus einem Fragment-Set
- **DASH:** als Bonus für Nicht-Apple-Clients/Tests, Routing primär auf HLS lassen

So integrierst du alle drei Welten (MP4, HLS/mp4frag, DASH) sauber in deine Pipeline, ohne dass der Web-Player-Code komplex wird.
