# Logbuch: MKV Tools für Media-Library (pymediainfo, FFmpeg, pymkv2, moviepy, enzyme)

## Datum: 10. März 2026

---

## Top MKV Python Tools
| Tool         | Features                   | Install                | Code/Wrapper         |
|--------------|----------------------------|------------------------|----------------------|
| pymediainfo  | Metadata (Tracks/Dauer)    | pip install pymediainfo| Direct               |
| ffmpeg-python| Audio/Subs/Thumbs Extract  | pip install ffmpeg-python| FFmpeg-Wrapper      |
| pymkv2       | Chapters/Tags/Mux          | pip install pymkv2     | MKVToolNix Wrapper   |
| moviepy      | Edit/Thumbs/Clips          | pip install moviepy    | Einfach              |
| enzyme       | MKV Parser                 | pip install enzyme     | Direct               |

---

## Voll-MKV Processor
### 1. Metadata Extract (pymediainfo)
```python
from pymediainfo import MediaInfo

def mkv_metadata(mkv_path):
    media_info = MediaInfo.parse(mkv_path)
    data = {
        'duration': media_info.tracks[0].duration / 1000,
        'video_codec': media_info.video_tracks[0].codec if media_info.video_tracks else None,
        'audio_tracks': len(media_info.audio_tracks),
        'subtitle_tracks': len(media_info.text_tracks),
        'chapters': media_info.tracks[0].chapter_count if hasattr(media_info.tracks[0], 'chapter_count') else 0
    }
    client.table('media').upsert({**data, 'path': mkv_path}).execute()
    return data
```

### 2. Chapters/Tags (pymkv2)
```python
from pymkv import MKVFile

mkv = MKVFile('movie.mkv')
print(f"Chapters: {len(mkv.chapters)}")
# Tags setzen
mkv.set_tags(title='Mein Film', genre='Sci-Fi')
mkv.save('movie_tagged.mkv')
```

### 3. Audio/Subs Extract (FFmpeg)
```python
import ffmpeg

def extract_mkv_audio(mkv_path, audio_path):
    stream = ffmpeg.input(mkv_path)
    stream = ffmpeg.output(stream, audio_path, acodec='flac')
    ffmpeg.run(stream)

def extract_subs(mkv_path, sub_path):
    ffmpeg.input(mkv_path).output(sub_path, map='0:s:0').run()
```

### 4. Thumbnails (moviepy)
```python
from moviepy.editor import VideoFileClip
from PIL import Image

clip = VideoFileClip('movie.mkv')
thumb = clip.get_frame(60)
Image.fromarray(thumb).save('thumb.jpg')
```

---

## MKV → Supabase Pipeline
```python
def full_mkv_process(mkv_path):
    meta = mkv_metadata(mkv_path)
    audio = extract_mkv_audio(mkv_path, f"{mkv_path.stem}.flac")
    audio_meta = extract_audio_metadata(audio)
    meta['audio'] = audio_meta
    chapters = get_mkv_chapters(mkv_path)
    meta['chapters'] = chapters
    client.table('media').upsert(meta).execute()
    return meta
```

---

## NiceGUI MKV Dashboard
```python
ui.upload('MKV laden', on_upload=lambda e: full_mkv_process(e.name))
ui.label('Chapters:').bind_text_from(mkv_data, 'chapters')
ui.video().props('controls')
ui.audio('extracted.flac').props('controls')
ui.aggrid(supabase_query('type=mkv')).classes('w-full')
```

---

## Batch
```python
for mkv in Path('mkvs').glob('*.mkv'):
    full_mkv_process(mkv)
```

---

## Pro-Tipp
- MKVToolNix GUI für Manual-Edit + Python-Automatisierung

---

## Follow-ups
- pymediainfo MKV test
- pymkv2 pip install
- FFmpeg Subs extract
- Chapters Supabase

---

**Fragen/Feedback:**
- pymkv2 für Chapters oder FFmpeg first?
- Weitere MKV-Workflow- oder Dashboard-Beispiele gewünscht?
