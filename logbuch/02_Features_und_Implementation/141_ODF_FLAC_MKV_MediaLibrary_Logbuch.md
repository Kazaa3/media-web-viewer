# Logbuch: LibreOffice ODF + FLAC/MKV Tools für Media-Library

## Datum: 10. März 2026

---

## Thema: Voll-Support für ODT/ODS + FLAC/MKV (odfpy/odfdo, mutagen, pymediainfo, FFmpeg)

### ODF (LibreOffice)
- **odfpy/odfdo:** Metadaten, Text, Tabellen
- **Code:**
```python
from odfdo import Document
odt = Document.load('file.odt')
print(odt.get_meta('title'))
print(odt.text())
```

---

### FLAC Libs (Audio)
| Tool        | Features                | Install           |
|-------------|-------------------------|-------------------|
| mutagen     | Tags/Cover (FLAC/MP3)   | pip install mutagen|
| pymediainfo | Dauer/Bitrate/Channels  | pip install pymediainfo|
| plibflac    | Raw FLAC read/write     | pip install plibflac|
| tinytag     | Schnelle Metadaten      | pip install tinytag|

**FLAC Example:**
```python
from mutagen.flac import FLAC
from pymediainfo import MediaInfo
flac = FLAC('song.flac')
print(f"Titel: {flac.get('title', [''])[0]}")
print(f"Cover: {len(flac.pictures)} Bilder")
info = MediaInfo.parse('song.flac')
track = info.audio_tracks[0]
print(f"Dauer: {track.duration}s, Bitrate: {track.bit_rate}kbps")
```

---

### MKV Tools (Video)
| Tool           | Features              | Install           |
|----------------|----------------------|-------------------|
| pymediainfo    | Video/Audio Tracks    | pip install pymediainfo|
| FFmpeg-python  | Extract Audio/Subs    | pip install ffmpeg-python|
| moviepy        | Edit/Thumbnail        | pip install moviepy|

**MKV Example:**
```python
import ffmpeg

def extract_mkv_metadata(mkv_path):
    probe = ffmpeg.probe(mkv_path)
    streams = probe['streams']
    data = {
        'duration': float(probe['format']['duration']),
        'video': streams[0].get('codec_name'),
        'audio': streams[1].get('codec_name') if len(streams) > 1 else None,
        'subs': len([s for s in streams if s['codec_type'] == 'subtitle'])
    }
    client.table('media').insert({**data, 'path': mkv_path}).execute()
    return data
```

---

### ODF + FLAC/MKV Master-Funktion
```python
from pathlib import Path

def process_multimedia(path):
    suffix = Path(path).suffix.lower()
    if suffix == '.odt':
        return extract_odf_metadata(path)
    elif suffix in ['.flac', '.mp3']:
        return extract_audio_metadata(path)
    elif suffix in ['.mkv', '.mp4']:
        return extract_mkv_metadata(path)
    # Supabase
    client.table('media').upsert(data).execute()

# Batch
for file in Path('media_folder').iterdir():
    process_multimedia(file)
```

---

### NiceGUI Multi-Viewer
```python
ui.upload('Datei laden', on_upload=lambda e: process_multimedia(e.name))
if file_type == 'flac':
    ui.audio(file_path).props('controls')
elif file_type == 'mkv':
    ui.video(file_path).props('controls')
```

---

### Integration
- FLAC → mutagen Tags
- MKV → FFmpeg Probe
- ODF → odfdo Meta
- Supabase realtime

---

**Fragen/Feedback:**
- pymediainfo first oder FFmpeg-python bevorzugt?
- Weitere Workflow- oder Viewer-Beispiele gewünscht?
