# Logbuch: MoviePy für MKV/FLAC Media-Library

## Datum: 10. März 2026

---

## Thema: MoviePy – Python Video-Editing Library für Thumbnails, Clips, Metadata, Audio-Extract

### Setup & Features
```bash
pip install moviepy[optional]  # imageio-ffmpeg auto
```

---

### Video Metadata + Thumbnails
```python
from moviepy.editor import VideoFileClip
from PIL import Image
from pathlib import Path
import supabase

def process_video(video_path):
    clip = VideoFileClip(video_path)
    data = {
        'path': video_path,
        'duration': clip.duration,
        'fps': clip.fps,
        'size': clip.size,
        'resolution': f"{clip.w}x{clip.h}",
        'audio_bitrate': clip.audio.bitrate if clip.audio else None
    }
    thumb = clip.get_frame(5)
    thumb_path = f"thumbs/{Path(video_path).stem}.jpg"
    Image.fromarray(thumb).save(thumb_path)
    data['thumbnail'] = thumb_path
    client.table('media').insert(data).execute()
    clip.close()
    return data

# Batch
for mkv in Path('videos').glob('*.mkv'):
    process_video(mkv)
```

---

### Audio aus MKV extrahieren
```python
def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
    clip.close()
    return audio_path

extract_audio('movie.mkv', 'movie_audio.flac')
```

---

### Video-Clips/Thumbs Grid
```python
def create_thumbsheet(video_path, thumbs=9):
    import numpy as np
    import matplotlib.pyplot as plt
    clip = VideoFileClip(video_path)
    times = np.linspace(0, clip.duration, thumbs)
    fig, axes = plt.subplots(3, 3, figsize=(12, 9))
    for i, t in enumerate(times):
        ax = axes[i//3, i%3]
        frame = clip.get_frame(t)
        ax.imshow(frame)
        ax.set_title(f"t={t:.0f}s")
        ax.axis('off')
    plt.savefig(f"thumbsheet_{Path(video_path).stem}.png")
    clip.close()
```

---

### NiceGUI Integration
```python
ui.upload('MKV/FLAC laden', on_upload=lambda e: process_video(e.name))
video_clip = ui.video().props('controls')
thumb_gallery = ui.gallery().classes('grid-cols-3 gap-4')
ui.button('Thumbs generieren', on_click=create_thumbsheet(video_path))
```

---

### Supabase Integration
```python
data = client.table('media').select('path, thumbnail, duration').eq('type', 'video').execute()
ui.aggrid(data.data)
```

---

### MoviePy vs FFmpeg
| Feature   | MoviePy   | FFmpeg-python |
|-----------|-----------|---------------|
| Ease      | ⭐⭐⭐⭐⭐    | ⭐⭐⭐          |
| Speed     | Gut       | Blitz         |
| Thumbs    | Einfach   | Raw           |
| Edit      | Voll      | Commands      |

**Empfehlung:** Für Library: MoviePy (Thumbs/Meta) + pymediainfo (deep Metadata)

---

### Fazit
- MoviePy ist ideal für Thumbnails, Metadaten, Audio-Extract und einfache Video-Edits
- FFmpeg für Speed und Spezialfälle

---

**Fragen/Feedback:**
- MoviePy Thumbs oder FFmpeg Extract bevorzugt?
- Weitere Video-Workflow- oder Viewer-Beispiele gewünscht?
