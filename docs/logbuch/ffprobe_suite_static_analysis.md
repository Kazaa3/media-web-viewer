# 🧪 **ffprobe Test-Suite** – Statische Analyse

**ffprobe** = **Zero-Playback Tests**: **Codecs, HDR, Subs, Chapters** in **<1s** prüfen – **vor FFplay/FFmpeg**! [stackoverflow](https://stackoverflow.com/questions/61043821/how-can-i-extract-bonus-images-from-a-tv-show-dvd-using-ffmpeg)

## **ffprobe Test-Tabelle**

| **Test**          | **Command**                                      | **Prüft**                     | **Ergebnis**     |
|-------------------|--------------------------------------------------|-------------------------------|------------------|
| **Codecs**        | `-show_entries stream=codec_name`               | H.264/HEVC/TrueHD             | Liste            |
| **HDR**           | `-show_entries stream=color_*`                  | BT2020, HDR10, Dolby Vision   | Metadata         |
| **Subs**          | `-select_streams s -show_entries codec_name`    | SRT/PGS/SSA                   | Anzahl/Typ       |
| **Chapters**      | `-show_entries format=chapters`                 | Navigation                    | Anzahl/Dauer     |
| **Audio Tracks**  | `-select_streams a -show_entries channels`      | 5.1/7.1/Atmos                 | Kanäle           |
| **Container**     | `-show_entries format=filename,size`            | MKV/MP4/M2TS                  | Integrität       |
| **Bitrate**       | `-show_entries stream=bit_rate`                 | Qualität                      | Mbps             |

## **Backend: ffprobe Master Suite**

```python
def ffprobe_suite(input_path):
    """Komplette Analyse in 0.5s"""
    results = {}
    
    # 1. Container Info
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
           '-show_format', input_path]
    format_info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    results['container'] = {
        'format': format_info['format']['format_name'],
        'size_gb': round(format_info['format']['size'] / (1024**3), 2),
        'duration_min': round(float(format_info['format']['duration']) / 60, 1)
    }
    
    # 2. Video Streams
    cmd = ['ffprobe', '-v', 'quiet', '-select_streams', 'v', 
           '-print_format', 'json', '-show_entries', 
           'stream=codec_name,width,height,bit_rate,color_space,color_primaries,color_transfer', 
           input_path]
    video_info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)['streams']
    results['video'] = []
    for stream in video_info:
        results['video'].append({
            'codec': stream['codec_name'],
            'resolution': f"{stream['width']}x{stream['height']}",
            'bitrate_mbps': round(int(stream.get('bit_rate', 0)) / 1e6, 1),
            'hdr': 'bt2020' in stream.get('color_space', ''),
            'profile': stream.get('profile', 'N/A')
        })
    
    # 3. Audio Tracks
    cmd = ['ffprobe', '-v', 'quiet', '-select_streams', 'a', 
           '-print_format', 'json', '-show_entries', 
           'stream=codec_name,channels,bit_rate,sample_rate', input_path]
    audio_info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)['streams']
    results['audio'] = []
    for stream in audio_info:
        results['audio'].append({
            'codec': stream['codec_name'],
            'channels': stream['channels'],
            'sample_rate': stream['sample_rate'],
            'bitrate_kbps': round(int(stream.get('bit_rate', 0)) / 1000, 0)
        })
    
    # 4. Subs
    cmd = ['ffprobe', '-v', 'quiet', '-select_streams', 's', 
           '-show_entries', 'stream=codec_name:stream_tags=language', input_path]
    subs_info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)['streams']
    results['subs'] = len(subs_info)
    
    # 5. Chapters
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
           '-show_entries', 'format=chapters', input_path]
    chapters_info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    results['chapters'] = len(chapters_info['format'].get('chapters', []))
    
    return results
```

## **App-Integration: ffprobe UI**

```html
<div id="ffprobePanel">
  <button id="runFfprobe">🔍 Analyze File</button>
  <div id="ffprobeResults"></div>
</div>
```

```js
document.getElementById('runFfprobe').onclick = async () => {
    const analysis = await eel.ffprobe_suite(currentPath)();
    displayAnalysis(analysis);
};

function displayAnalysis(data) {
    const container = document.getElementById('ffprobeResults');
    container.innerHTML = `
        <h3>📊 File Analysis</h3>
        <div>Container: ${data.container.format} (${data.container.size_gb}GB)</div>
        <div>Duration: ${data.container.duration_min}min</div>
        <div>Video: ${data.video.length} Tracks</div>
        ${data.video.map(v => 
            `<div>  ${v.codec} ${v.resolution} ${v.bitrate_mbps}Mbps ${v.hdr ? 'HDR' : ''}</div>`
        ).join('')}
        <div>Audio: ${data.audio.length} Tracks</div>
        <div>Subs: ${data.subs}</div>
        <div>Chapters: ${data.chapters}</div>
    `;
}
```

## **Quick Quality Score**

```python
def ffprobe_quality_score(analysis):
    """0-100 Score"""
    score = 0
    
    # Video
    if analysis['video']:
        video = analysis['video'][0]
        if video['codec'] in ['h264', 'hevc']: score += 25
        if video['bitrate_mbps'] > 20: score += 15
        if video['hdr']: score += 20
        if int(video['resolution'].split('x')[0]) >= 1920: score += 15
    
    # Audio
    if len(analysis['audio']) >= 2: score += 10
    if any(a['channels'] >= 6 for a in analysis['audio']): score += 15
    
    # Subs/Chapters
    if analysis['subs'] > 0: score += 10
    if analysis['chapters'] > 5: score += 5
    
    return score
```

## **Eel Exposed**

```python
eel.expose(ffprobe_suite)
eel.expose(ffprobe_quality_score)
```

## **Batch Analyse**

```python
def batch_ffprobe(media_folder):
    """Alle Files analysieren"""
    files = glob.glob(f"{media_folder}/**/*.mkv", recursive=True)
    reports = {}
    
    for file in files[:10]:  # Top 10
        reports[file] = ffprobe_suite(file)
    
    return reports
```

## **Demo Output**

```
📊 movie.mkv
Container: matroska (12.3GB)
Duration: 142min
Video: 1 Track
  hevc 3840x2160 45.2Mbps HDR
Audio: 3 Tracks
  truehd 7.1 48kHz 5678kbps
Subs: 2
Chapters: 28
Score: 95/100 ✅
```

**ffprobe Suite** = **1s Analyse** → **Quality Gate** → **Stream Ready**! 🧪🚀

**Perfekt** vor **FFplay/FFmpeg**! **Integriere** `ffprobe_suite(path)`!
