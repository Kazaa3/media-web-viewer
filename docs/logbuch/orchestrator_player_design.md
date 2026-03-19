# Orchestrator-Player-Design für Bottle/Eel/JS

**Kurz:**
Der „ultimative“ Player ist kein einzelner Player, sondern ein Orchestrator, der je nach Datei und Client automatisch den besten, leichtesten Pfad wählt – basierend auf einer vorgelagerten Test-/Analyse-Schicht.

---

## 1. Ziele
- **Direct Play** wo möglich (0 Transcoding, volle Qualität, minimale CPU)
- **HLS** für Browser-Streaming (Segmentierung, Caching, Adaptive)
- **VLC/mpv** für alles Komplizierte (ISO, BD, PGS, TrueHD, AV1/HDR)
- **MediaMTX/RTSP** als Streaming-Hub für VLC/ffplay
- **Test-Suite** davor, die jeden Input scannt und einen Play-Plan erzeugt

---

## 2. Schicht 1: Storage & Caches
- Primär: `/mnt/smb/media/...` (SMB/NAS)
- Caches:
  - `/var/cache/mp4/<hash>.mp4` – Remux-MP4 für Direct Play
  - `/var/cache/hls/<hash>/index.m3u8` – HLS-Playlists + Segmente
  - `/var/cache/iso_main/<hash>.mkv` – extrahierter Hauptfilm aus ISO/BD

---

## 3. Schicht 2: Multimedia-Test-/Analyse-Suite
Funktion: `analyze_media(full_path) -> dict`
- ffprobe: Container, Dauer, Codecs, Auflösung, HDR, Audio, Subs, Chapters
- Heuristiken: `can_direct_play_browser`, `is_complex`
- Optional: mkvmerge-Sanitize, ffplay/VLC-Smoke-Test
- Berechnet auch `quality_score` und Flags wie `prefer_vlc`

---

## 4. Schicht 3: Routing-Engine
Funktion: `get_play_plan(item, client='browser')`

```python
def get_play_plan(relpath, client='browser'):
    full = os.path.join(MEDIA_ROOT, relpath)
    if full.lower().endswith('.iso'):
        full = extract_main_from_iso(full)
    analysis = analyze_media(full)
    if client == 'browser':
        if analysis['can_direct_play_browser']:
            direct_rel = ensure_mp4_remux(full)
            return {"mode": "direct", "url": f"/direct/{direct_rel}", "quality_score": analysis['quality_score']}
        else:
            hls_url = ensure_hls_playlist(full)
            return {"mode": "hls", "url": hls_url, "quality_score": analysis['quality_score']}
    if client in ('vlc', 'cvlc', 'pyvlc'):
        if full.endswith('.iso'):
            return {"mode": "vlc-bluray", "url": full}
        else:
            if use_rtsp:
                rtsp_url = start_mtx_rtsp(full)
                return {"mode": "vlc-rtsp", "url": rtsp_url}
            return {"mode": "vlc-file", "url": full}
    if client == 'py-player':
        return {"mode": "pyvlc", "url": full}
    return {"mode": "unsupported", "url": full}
```

---

## 5. Schicht 4: Übertragungswege

### Browser-Pfad
- **Direct Play:** Flask `/direct/<relpath>` (Range-fähig), video.js mit `type: 'video/mp4'`
- **HLS:** FFmpeg erzeugt HLS, nginx/Flask serviert `/hls/<hash>/index.m3u8`, video.js mit `type: 'application/x-mpegURL'`

### VLC/mpv-Pfad
- **Datei-Direct-Play:** `vlc full_path`, `cvlc full_path`, `mpv full_path`
- **Blu-ray/ISO:** `vlc bluray:///path/to.iso`
- **RTSP über MediaMTX:** FFmpeg publish, VLC/mpv/ffplay konsumieren

---

## 6. Schicht 5: Video-Player-UI (Eel/Bottle + JS + video.js)

### Mode-Selector
- „Browser (Direct/HLS)“
- „VLC“
- „Py-Player“
- Fallback/Expert: „FFplay“, „MTX/RTSP“, „Pipe-Varianten“

### Play-Funktion (JS)
```js
async function playItem(item, clientMode = 'browser') {
  const plan = await eel.get_play_plan(item.relpath, clientMode)();
  updateStatus(plan, item);
  if (clientMode === 'browser') {
    if (plan.mode === 'direct') {
      player.src({ src: plan.url, type: 'video/mp4' });
    } else if (plan.mode === 'hls') {
      player.src({ src: plan.url, type: 'application/x-mpegURL' });
    } else {
      // Hinweis anzeigen: nur VLC/RTSP möglich
      return;
    }
    player.play();
  } else if (clientMode === 'vlc') {
    if (plan.mode === 'vlc-bluray') eel.vlc_bluray(plan.url)();
    else if (plan.mode === 'vlc-rtsp') eel.vlc_open_rtsp(plan.url)();
    else eel.open_in_vlc(plan.url)();
  } else if (clientMode === 'py-player') {
    eel.pyvlc_play(plan.url)();
  }
}
```

---

## 7. Bonus: Status & Debug
- Im Player-Tab anzeigen: Modus, Qualität, Auflösung, Codec, HDR
- Extra-Buttons: „ffprobe Details“, „5s ffplay-Smoke-Test“, „HLS neu erstellen“

---

**Fazit:**
- Einheitliche Test- und Routing-Schicht
- Mehrere klar definierte Abspielpfade
- Video-Tab führt nur noch den Play-Plan aus, kennt keine Medienlogik mehr
- Perfekte Mischung aus Mächtigkeit und Wartbarkeit für Bottle/Eel/JS
