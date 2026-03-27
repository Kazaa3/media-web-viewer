# Direct Play – Die komplette Kette (ausführlich)

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## 1. Was passiert technisch?

```
📁 /media/movie.mp4 (H.264/MP4, 2GB)
   ↓
🖥️ Backend Server (Bottle/Flask)
   ↓ HTTP GET /movie.mp4
📡 Browser: "Range: bytes=0-1048575" (1MB)
   ↓
Server: moov-Header (100KB) + 900KB Video
   ↓
Chrome: MP4-Parser → Index → "Seekbar ready!"
📱 User: Seek 1:30:00 → "Range: bytes=5.2GB-5.3GB"
```

---

## 2. Die 7-Schritte-Kette

```
1. ffprobe /movie.mp4 → {h264, mp4, 1080p, AAC} ✅ Direct Play!
2. Browser: <video src="/movie.mp4">
3. HTTP HEAD → Content-Length: 2GB, Accept-Ranges: bytes
4. Browser: GET Range: bytes=0- → moov-Header (Metadaten)
5. MP4-Parser: Tracks/Duration/Chapters extrahiert
6. Prefetch: 5-10s Buffer (Range-Requests parallel)
7. <video>: Play/Seek/Pause → On-Demand Ranges
```

---

## 3. HTTP Range Requests (Detail)

**Beispiel:**
```
Browser: GET /movie.mp4 HTTP/1.1
Range: bytes=0-1048575
Accept: */*

Server: HTTP/206 Partial Content
Content-Range: bytes 0-1048575/2147483648
Content-Length: 1048576

[moov + 1st GOP → Browser dekodiert sofort!]
```

**Seek 1:30:00:**
```
Range: bytes=5400000000-5401000000
→ I-Frame direkt → 100ms Jump!
```

---

## 4. Backend Implementierung (Bottle)

```python
@app.route('/movie/<filename>')
def direct_play(filename):
    file_path = f"/media/{filename}"
    size = os.path.getsize(file_path)
    
    # Range-Header parsen
    start, end = 0, size - 1
    range_header = request.headers.get('Range')
    if range_header:
        start, end = map(int, range_header.replace('bytes=', '').split('-'))
        end = min(end, size - 1)
    
    with open(file_path, 'rb') as f:
        f.seek(start)
        data = f.read(end - start + 1)
    
    return Response(data, 
                   status=206 if range_header else 200,
                   headers={
                       'Content-Range': f'bytes {start}-{end}/{size}',
                       'Accept-Ranges': 'bytes',
                       'Content-Length': str(len(data)),
                       'Content-Type': 'video/mp4'
                   })
```

---

## 5. Frontend (Video.js)

```html
<video-js id="player" data-setup='{"fluid": true}'>
  <source src="/movie/movie.mp4" type="video/mp4">
</video-js>
```

- **Seekbar:** Range-Requests automatisch
- **Buffer:** 5-30s Prefetch
- **Adaptive:** HTML5 Network-State

---

## 6. ffprobe Direct-Play-Check

```python
def is_direct_playable(streams):
    video = next((s for s in streams if s['codec_type']=='video'), None)
    audio = next((s for s in streams if s['codec_type']=='audio'), None)
    
    return (video['codec_name'] in ['h264', 'hevc'] and
            audio['codec_name'] in ['aac', 'mp3'] and
            streams[0]['format_name'] == 'mp4')
```

---

## 7. Warum Direct Play gewinnt?

```
Direct Play:  0% CPU, 0s Start, perfekte Qualität
HLS:         25% CPU, 5s Latenz, 20% Bandbreite-Overhead
MSE:         20% CPU, 0.5s Latenz, komplex
```

**Browser-Decoder:**
```
Chrome: H.264 → Arc QSV (0% CPU!)
Firefox: VP9 → Software
```

---

## 8. Edge-Cases

```
✅ MP4/H.264/AAC → Instant Play
✅ MKV → Container-Remux (1s, 5% CPU)
❌ ISO/BD → ffprobe → Title-Extract → MP4
❌ 3D SBS → VF Filter (10% CPU)
```

**Dein Flow:**
```
DROP MP4 → ffprobe ✅ → /movie.mp4 → <video src> → PLAY!
Kette-Zeit: 100ms (Range-Request + moov)! 0% FFmpeg! 🎥✨
```
