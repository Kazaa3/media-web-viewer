# 🧪 Test-Suite als Vorfilter für Media-Routing

In deinem Setup ist die „Test-Suite“ ein **Vorfilter**, der jede Datei einmal kurz durch ffprobe/FFmpeg/ffplay jagt, bevor du entscheidest: Direct Play, HLS oder VLC-Pfad.

---

## 1. Was die Suite konkret tut

Für einen gegebenen Pfad (`full_path`):

1. **ffprobe-Analyse**  
   - Container (mkv/mp4/iso), Dauer, Größe, Video-/Audio-Codecs, Auflösung, HDR-Flags, Audio-Kanäle, Untertitel.
2. **Kompatibilität / Direct-Play-Check**  
   - Browser-fähig? (mp4 + h264/avc + aac).  
   - Für VLC/ffplay praktisch immer „ja“.
3. **(Optional) Kurztest mit ffplay**  
   - 3–5 s abspielen, um offensichtliche Korruption zu erwischen.
4. **Quality-Score berechnen**  
   - z.B. Punkte für 1080p/4K, hohe Bitrate, Mehrkanal-Audio, vorhandene Subs & Chapters.

Ergebnis ist eine kleine Struktur wie:

```json
{
  "container": "matroska",
  "duration_min": 142.3,
  "video_codec": "hevc",
  "audio_codec": "truehd",
  "hdr": true,
  "subs": 2,
  "chapters": 24,
  "quality_score": 93,
  "direct_play_browser": false
}
```

---

## 2. Wie du sie im Player verwendest

Beim Klick auf ein Item:

```js
async function playItem(item) {
    // 1. Test-Suite aufrufen
    const info = await eel.analyze_media(item.relpath)();
    // info = { quality_score, direct_play_browser, recommended_mode, urls... }

    // 2. Routing basierend auf Testergebnis
    if (info.direct_play_browser) {
        // Direct Play (Range oder vorhandenes MP4)
        player.src({ src: info.direct_url, type: 'video/mp4' });
    } else if (info.recommended_mode === 'hls') {
        player.src({ src: info.hls_url, type: 'application/x-mpegURL' });
    } else {
        // komplexer Fall (HDR+PGS+TrueHD usw.) → VLC-Tab
        eel.open_in_vlc(item.path)();
        return;
    }

    updatePlayInfo(info, item);
    player.play();
}
```

Und das Backend-Pendant:

```python
@eel.expose
def analyze_media(relpath, client='browser'):
    full = os.path.join(MEDIA_ROOT, relpath)
    analysis = ffprobe_suite(full)
    score = ffprobe_quality_score(analysis)

    direct = is_direct_play_capable(full, client)
    if direct:
        url = f"/direct/{relpath}"
        mode = "direct"
        hls_url = None
    else:
        hls_playlist = ensure_hls(full)
        mode = "hls"
        # /hls/<hash>/index.m3u8
        h = os.path.basename(os.path.dirname(hls_playlist))
        url = None
        hls_url = f"/hls/{h}/index.m3u8"

    return {
        "analysis": analysis,
        "quality_score": score,
        "direct_play_browser": direct,
        "recommended_mode": mode,
        "direct_url": url,
        "hls_url": hls_url,
    }
```

---

**Kurz gesagt:**

- **Test-Suite = analyze_media()**  
- Sie liefert dir _alle_ Infos, die du fürs Routing brauchst.  
- Dein Video-Player (Direct Play / HLS / VLC) entscheidet dann nur noch anhand dieses einen Objekts, was zu tun ist.
