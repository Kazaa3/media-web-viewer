# Logbuch: MKV Tools für Media-Library – Vollständige Pipeline

## Datum: 10. März 2026

---

## MKV Tools Übersicht
| Tool         | Zweck                   | Install                | Sterne |
|--------------|-------------------------|------------------------|--------|
| pymediainfo  | Metadata (Tracks/Dauer) | pip install pymediainfo| ⭐⭐⭐⭐⭐ |
| ffmpeg-python| Audio/Subs/Thumbs       | pip install ffmpeg-python| ⭐⭐⭐⭐ |
| pymkv2       | Chapters/Tags           | pip install pymkv2     | ⭐⭐⭐⭐ |
| moviepy      | Thumbnails/Clips        | pip install moviepy    | ⭐⭐⭐   |
| enzyme       | Raw MKV Parser          | pip install enzyme     | ⭐⭐    |

---

## Vollständiger MKV Processor (Code)
```python
from pymediainfo import MediaInfo
import ffmpeg
from pymkv import MKVFile
from moviepy.editor import VideoFileClip
from supabase import Client
from pathlib import Path

client = Client(SUPABASE_URL, SUPABASE_KEY)

def full_mkv_pipeline(mkv_path):
    media_info = MediaInfo.parse(mkv_path)
    video_track = media_info.video_tracks[0]
    data = {
        'path': mkv_path,
        'type': 'mkv',
        'duration_s': media_info.tracks[0].duration / 1000,
        'width': video_track.width,
        'height': video_track.height,
        'video_codec': video_track.codec,
        'audio_tracks': len(media_info.audio_tracks),
        'sub_tracks': len(media_info.text_tracks),
        'bitrate_kbps': media_info.video_tracks[0].bit_rate / 1000
    }
    mkv = MKVFile(mkv_path)
    chapters = [{'start': c.start, 'end': c.end, 'title': c.title} for c in mkv.chapters]
    data['chapters'] = chapters
    clip = VideoFileClip(mkv_path)
    thumb = clip.get_frame(min(60, clip.duration/2))
    thumb_path = f"thumbs/{Path(mkv_path).stem}.jpg"
    Image.fromarray(thumb).save(thumb_path)
    data['thumbnail'] = thumb_path
    clip.close()
    audio_path = f"audio/{Path(mkv_path).stem}.flac"
    Path(audio_path).parent.mkdir(exist_ok=True)
    ffmpeg.input(mkv_path).output(audio_path, acodec='flac').run(quiet=True)
    data['audio_extract'] = audio_path
    subs = ffmpeg.probe(mkv_path, select_streams='s')
    if subs['streams']:
        ffmpeg.input(mkv_path).output(f"subs/{Path(mkv_path).stem}.srt", map='0:s:0').run()
        data['subs'] = f"subs/{Path(mkv_path).stem}.srt"
    client.table('media').upsert(data).execute()
    return data
```

---

## MKVToolNix via pymkv2 (Advanced)
```python
mkv = MKVFile('movie.mkv')
chapter1 = mkv.add_chapter(start_ms=0, end_ms=60000, title='Intro')
mkv.save('movie_with_chapters.mkv')
mkv.set_tags(title='Mein Film', genre='Sci-Fi', director='Peter-Christian')
```

---

## NiceGUI MKV Dashboard
```python
ui.upload('MKV laden', on_upload=lambda e: full_mkv_pipeline(e.name))
if data['chapters']:
    ui.timeline([{'content': c['title'], 'time': f"{c['start']/1000:.0f}s"} for c in data['chapters']])
ui.video(data['path']).props('controls')
ui.image(data['thumbnail']).classes('w-64 h-36 object-cover')
ui.audio(data['audio_extract']).props('controls')
ui.aggrid([{
    'type': t.track_type,
    'codec': t.codec,
    'language': t.language
} for t in media_info.tracks])
```

---

## Performance Batch
```python
from multiprocessing import Pool

def process_mkv_wrapper(args):
    return full_mkv_pipeline(args[0])

with Pool(4) as p:
    mkvs = list(Path('mkvs').glob('*.mkv'))
    results = p.map(process_mkv_wrapper, mkvs)
```

---

## Fazit
- MKV Tools: Metadata, Chapters, Subs, Mux/Split, Thumbnails, Audio-Extract
- Perfekte Integration für Media-Library mit Supabase/NiceGUI

---

**Fragen/Feedback:**
- pymkv2 Chapters oder FFmpeg Subs first?
- Weitere MKV-Workflow-, Dashboard- oder Batch-Beispiele gewünscht?
