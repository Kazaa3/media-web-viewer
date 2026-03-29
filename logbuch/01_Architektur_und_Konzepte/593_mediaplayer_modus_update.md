# Logbuch: Aktualisierte MediaPlayer-Modi (Chrome Native & VLC)

## Datum
16. März 2026

---

## Player 1: Chrome Native (HTML5 <video>)
┌─ 🎬 CHROME NATIVE MODI ──────────────────────────────┐
│ 1. Direct Play        → MP4/WebM (H.264/VP9+AAC)     │
│ 2. HLS Native         → MediaMTX http://8888/...     │
│ 3. FragMP4 Stream     → ffmpeg -f mp4 -listen 1      │
│ 4. Progressive Range  → HTTP Range-Requests          │
│ 5. WebM/VP9           → Moderne Codecs direkt        │
└──────────────────────────────────────────────────────┘
**Vorteile:** 0–5% CPU, native Seeking, mobil-freundlich  
**Limitation:** Nur MP4/WebM/HLS, kein ISO/Menus

---

## Player 2: VLC (Embedded/Extern/cvlc)
┌─ 📺 VLC MODI (Alle Formate) ─────────────────────────┐
│ 1. cvlc Solo           → TS-Stream :8090/            │
│ 2. VLC Embedded        → ActiveX/npapi Browser       │
│ 3. VLC Extern          → vlc http://localhost/...    │
│ 4. cvlc → ffmpeg Pipe  → cvlc | ffmpeg FragMP4       │
│ 5. DVD ISO Live        → cvlc dvd:///path/to/iso     │
└──────────────────────────────────────────────────────┘
**Vorteile:** 100% Format-Support, Menus, Hardware-Decoding  
**Limitation:** Desktop-only, kein Mobile, höhere CPU

---

## Optimiertes Dropdown (2 Player getrennt)
```html
<select id="player-type">
  <option value="chrome">🎬 Chrome Native (Mobile/Browser)</option>
  <option value="vlc">📺 VLC (Desktop/Alle Formate)</option>
</select>
<select id="video-mode" style="margin-left:10px;">
  <optgroup label="Chrome Native">
    <option value="chrome_direct">⚡ Direct Play</option>
    <option value="chrome_hls">📱 MediaMTX HLS</option>
    <option value="chrome_fragmp4">🔄 ffmpeg FragMP4</option>
  </optgroup>
  <optgroup label="VLC Modi">
    <option value="vlc_cvlc">📡 cvlc Solo</option>
    <option value="vlc_embedded">🖥️ VLC Embedded</option>
    <option value="vlc_iso">💿 DVD ISO Live</option>
  </optgroup>
</select>
```

---

## Backend-Logik (Player-basiert)
```python
@eel.expose
def open_video(file_path, player_type, mode):
    if player_type == "chrome":
        if mode == "chrome_direct":
            if is_direct_compatible(file_path):
                return f"/direct/{os.path.basename(file_path)}"
            else:
                return "chrome_hls"  # Fallback
        elif mode == "chrome_hls":
            trigger_mediamtx(file_path)
            return f"http://localhost:8888/{file_path}/index.m3u8"
    elif player_type == "vlc":
        if mode == "vlc_cvlc":
            port = get_free_port()
            subprocess.Popen([
                'cvlc', file_path,
                '--sout', f'#std{{access=http,mux=ts,dst=:{port}/}}'
            ])
            return f"http://localhost:{port}/"
        elif mode == "vlc_iso" and file_path.endswith('.iso'):
            return f"vlc dvd:///{file_path}"
```

---

## Modus-Matrix (Player-Vergleich)
| Feature/Player | Chrome Native | VLC           |
|----------------|---------------|---------------|
| MP4/H.264      | ✅ Direct Play| ✅ cvlc Stream |
| MKV            | ⚠️ FragMP4/HLS| ✅ Native      |
| ISO/DVD        | ❌ (Rip needed)| ✅ Live Menus  |
| Seeking        | Instant/Chunks| Gut           |
| Mobile         | ✅            | ❌            |
| CPU            | 0–5%          | 10–20%        |
| Setup          | Einfach       | VLC install   |

---

## "Öffnen mit" Flow
1. Player wählen: Chrome (Browser) | VLC (Desktop)
2. Modus: Direct Play → HLS → FragMP4 | cvlc → ISO Live
3. ffprobe Pre-Check → Auto-Fallback

---

## Fazit
MediaPlayer-Architektur jetzt mit getrennten Playern (Chrome Native, VLC), optimiertem Dropdown und intelligenter Backend-Logik. Chrome Native als Default für Mobil/Browser, VLC für maximale Format-Kompatibilität am Desktop.

---

*Siehe vorherige Logbuch-Einträge für Details zu einzelnen Modi und Backend-Integration.*
