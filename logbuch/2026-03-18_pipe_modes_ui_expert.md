# Logbuch: Pipe-Varianten – Erweiterte Modus-Auswahl (Expert-Optionen)

## Stand März 2026

### Features & Architektur
- Pipe-Varianten (mkvmerge → FFmpeg) sind als Expert-Optionen ganz unten im UI (<details> collapsed).
- Modus-Auswahl: Primary (Chrome Native, Video.js, VLC), Fallbacks (ffplay, MTX), Expert (Pipe-FragMP4, Pipe-HLS).
- UI-Hierarchie: Primary > Fallback > Pipes – für optimale Usability.
- Status-Feedback: Expert-Modi zeigen Pipe-Status im UI (z.B. "🔄 Piping: mkvmerge → FFmpeg HLS...").

### Beispiel-Implementierung
#### HTML (Modus-Selector)
```html
<div class="mode-selector">
  <button data-mode="chrome-native">Chrome Native</button>
  <button data-mode="videojs">Video.js</button>
  <button data-mode="vlc">VLC</button>
  <button data-mode="ffplay">FFplay</button>
  <button data-mode="mtx">MTX RTSP</button>
  <details class="expert-modes">
    <summary>Expert: Pipe-Varianten</summary>
    <button data-mode="pipe-fragmp4">mkvmerge→FFmpeg FragMP4</button>
    <button data-mode="pipe-hls">mkvmerge→FFmpeg HLS</button>
  </details>
</div>
```

#### JS (switchPlayerMode)
```js
function switchPlayerMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.player-panel').forEach(p => p.style.display = 'none');
    const panelId = mode === 'chrome-native' ? 'chromePanel' : 
                    (['vlc','cvlc','pyvlc'].includes(mode) ? 'vlcPanel' : 'statusPanel');
    document.getElementById(panelId).style.display = 'block';
    if (mode.startsWith('pipe-')) {
        updateStatus(`🔄 Piping: mkvmerge → FFmpeg ${mode.split('-')[1].toUpperCase()}...`);
        const url = await eel.generate(path, mode)();
        nativeVideo.src = url;
        nativeVideo.play();
    } else {
        playFile(path, mode);
    }
}
```

#### Python (Backend)
```python
PIPE_MODES = {
    'pipe-fragmp4': generate_pipe_fragmp4,
    'pipe-hls': generate_pipe_hls
}

def generate_pipe_hls(input_file, output_base):
    tmp_mkv = tempfile.NamedTemporaryFile(suffix='.mkv').name
    subprocess.run(['mkvmerge', '-o', tmp_mkv, input_file], check=True)
    out_dir = f"{output_base}_hls"
    os.makedirs(out_dir, exist_ok=True)
    cmd = [
        'ffmpeg', '-i', tmp_mkv,
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-f', 'hls', '-hls_time', '6', f"{out_dir}/playlist.m3u8"
    ]
    subprocess.run(cmd, check=True)
    os.unlink(tmp_mkv)
    return f"{out_dir}/playlist.m3u8"

def generate(path, mode):
    if mode in PIPE_MODES:
        return PIPE_MODES[mode](path, f"/tmp/output_{mode}")
    # ... andere Modi
```

### Modus-Tabelle (inkl. Pipes)
| Kategorie   | Modus         | Tool-Chain           | Output         |
|-------------|-------------- |--------------------- |--------------- |
| Primary     | chrome-native | FFmpeg mp4-faststart | .mp4           |
| videojs     | FFmpeg HLS    | .m3u8                |
| vlc/cvlc/pyvlc | mkvmerge/native | MKV/RTSP         |
| Fallback    | ffplay        | FFmpeg/ffplay        | Direct         |
| mtx         | FFmpeg → MTX  | RTSP                 |
| Expert      | pipe-fragmp4  | mkvmerge → FFmpeg    | FragMP4        |
| Expert      | pipe-hls      | mkvmerge → FFmpeg    | HLS            |

### Zusammenfassung
- Pipe-Varianten sind als Expert-Optionen ganz unten im UI.
- Status-Feedback und Usability optimiert.
- Alle Modi (Primary, Fallback, Expert) übersichtlich und nutzbar.

---
Perfekt für fortgeschrittene Nutzer: Pipes als Expert-Optionen, Status-Feedback, volle Kontrolle!
