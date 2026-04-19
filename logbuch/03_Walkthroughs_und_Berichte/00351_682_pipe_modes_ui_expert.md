# Logbuch: Pipe-Varianten – Erweiterte Modus-Auswahl (Expert-Optionen)

## Stand März 2026


### Features & Architektur
- Pipe-Varianten (mkvmerge → FFmpeg) und Python-Player (pyvidplayer) sind als Expert-Optionen ganz unten im UI (<details> collapsed).
- Modus-Auswahl: Primary (Chrome Native, Video.js, VLC), Fallbacks (ffplay, MTX), Expert (Pipe-FragMP4, Pipe-HLS, pyvidplayer).
- UI-Hierarchie: Primary > Fallback > Expert (Pipes & Python-Player) – für optimale Usability.
- Status-Feedback: Expert-Modi zeigen Pipe-Status im UI (z.B. "🔄 Piping: mkvmerge → FFmpeg HLS...").

#### Python-Player (pyvidplayer)
- pyvidplayer ist ein programmatischer Python-Player für Video/Audio, ideal für Embedded- und Backend-Integration.
- Expert-Modus: "pyvidplayer" als Button im <details> Bereich.

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
        <summary>Expert: Pipe-Varianten & Python-Player</summary>
        <button data-mode="pipe-fragmp4">mkvmerge→FFmpeg FragMP4</button>
        <button data-mode="pipe-hls">mkvmerge→FFmpeg HLS</button>
        <button data-mode="pyvidplayer">pyvidplayer (Python)</button>
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

def generate(path, mode): # Refractor to generate_pipe
    if mode in PIPE_MODES:
        return PIPE_MODES[mode](path, f"/tmp/output_{mode}")
    # ... andere Modi
```




### Modus-Tabelle (alle Varianten)
| Kategorie   | Modus                | Tool-Chain                | Output           |
|-------------|----------------------|---------------------------|------------------|
| Primary     | chrome-native        | FFmpeg mp4-faststart      | .mp4             |
| Primary     | videojs              | FFmpeg HLS                | .m3u8            |
| Primary     | vlc (Direct Replay)  | VLC ohne Transcoding      | Original         |
| Primary     | vlc/cvlc/pyvlc       | mkvmerge/native           | MKV/RTSP         |
| Primary     | pyvidplayer          | pyvidplayer (Python)      | Embedded/Direct  |
| Fallback    | ffplay               | FFmpeg/ffplay             | Direct           |
| MTX         | mtx Variante 1       | FFmpeg → MTX (RTSP)       | RTSP             |
| MTX         | mtx Variante 2       | FFmpeg → MTX (UDP)        | UDP Stream       |
| Expert      | mkvmerge alleine     | mkvmerge                  | MKV              |
| Expert      | ffmpeg Variante 1    | FFmpeg FragMP4            | FragMP4          |
| Expert      | ffmpeg Variante 2    | FFmpeg HLS                | HLS (.m3u8)      |
| Expert      | ffmpeg Variante 3    | FFmpeg → ffplay           | Direct           |
| Expert      | pipe-fragmp4         | mkvmerge → FFmpeg         | FragMP4          |
| Expert      | pipe-hls             | mkvmerge → FFmpeg         | HLS              |

### Zusammenfassung
- Pipe-Varianten sind als Expert-Optionen ganz unten im UI.
- Status-Feedback und Usability optimiert.
- Alle Modi (Primary, Fallback, Expert) übersichtlich und nutzbar.

---
Perfekt für fortgeschrittene Nutzer: Pipes als Expert-Optionen, Status-Feedback, volle Kontrolle!
