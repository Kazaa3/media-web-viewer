# Logbuch: FFmpeg-python & MoviePy für MKV Media-Library

## Datum: 10. März 2026

---

## Thema: FFmpeg-python & MoviePy – Audio/Subs Extract, Metadaten für MKV

### FFmpeg-python: Extract Audio/Subs
```bash
pip install ffmpeg-python
```

**MKV Metadaten-Extraktion:**
```python
import ffmpeg
from pathlib import Path
import supabase

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

### MoviePy: Video-Editing, Thumbnails, Audio-Extract
```bash
pip install moviepy[optional]
```

**Audio aus MKV extrahieren:**
```python
from moviepy.editor import VideoFileClip

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
    clip.close()
    return audio_path

extract_audio('movie.mkv', 'movie_audio.flac')
```

---

### Integration in Media-Library
- FFmpeg-python: Deep Metadata, Subtitle-Count, Codec-Info
- MoviePy: Thumbnails, Audio-Extract, Video-Clips
- Supabase: Realtime Sync

---

### Workflow
1. MKV → FFmpeg-python: Metadaten/Subs
2. MKV → MoviePy: Thumbnails, Audio-Extract
3. Daten → Supabase

---

**Fragen/Feedback:**
- Weitere FFmpeg/MoviePy-Workflow-Beispiele gewünscht?
- Subtitle-Extract oder Audio-Clip bevorzugt?
