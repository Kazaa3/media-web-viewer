# Logbuch: plibflac vs. pyFLAC – Vergleich für Media-Library

## Datum: 10. März 2026

---

## Technische Unterschiede
| Kriterium      | plibflac (MIT-LCP)      | pyFLAC (Sonos)         |
|----------------|------------------------|------------------------|
| Fokus          | File I/O (lesen/schreiben) | Streaming/Real-time   |
| API            | Context-Manager (with Decoder()) | Callback-basiert |
| Performance    | Datei-orientiert (schnell) | Stream (latenzoptimiert) |
| Version        | Neu (2024)              | Etabliert (2021+)      |
| Installation   | pip install plibflac    | pip install pyflac + libsndfile |
| GitHub         | MIT-LCP/plibflac        | sonos/pyFLAC           |

---

## Code-Vergleich
### plibflac (file-based)
```python
import plibflac
with plibflac.Decoder("track.flac") as decoder:
    print(f"Sample Rate: {decoder.sample_rate}")
    print(f"Channels: {decoder.channels}")
    samples = decoder.read(1000)
```

### pyFLAC (streaming/callback)
```python
import pyflac
import soundfile as sf

def audio_callback(data, sr, channels, samples):
    if output is None:
        output = sf.SoundFile("out.wav", mode='w', samplerate=sr, channels=channels)
    output.write(data)

decoder = pyflac.StreamDecoder(callback=audio_callback)
decoder.process(flac_bytes)
```

---

## Empfehlung für Media-Library
**Wähle plibflac wenn:**
- FLAC-Dateien scannen/indexieren (Metadaten + Samples)
- Batch-Processing (1000+ FLACs)
- Einfache Integration (mutagen-ähnlich)
- Raw Samples für MFCC/DSP

**Wähle pyFLAC wenn:**
- Real-time Audio-Streaming (Radio/Podcasts)
- WebSocket → Browser Audio-Streaming
- Callback-basierte Verarbeitung

---

## Hybrid-Lösung (beide + mutagen)
```python
def flac_universal(flac_path: str):
    from mutagen.flac import FLAC
    tags = FLAC(flac_path).tags or {}
    try:
        with plibflac.Decoder(flac_path) as decoder:
            tech = {
                'sample_rate': decoder.sample_rate,
                'duration': decoder.total_samples / decoder.sample_rate
            }
    except:
        tech = {}
    import librosa
    y, sr = librosa.load(flac_path, duration=10)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return {
        'title': tags.get('TITLE', [''])[0],
        'tech': tech,
        'mfcc_mean': list(mfcc.mean(axis=1))
    }
```

---

## Installationstest
```bash
pip install plibflac
sudo apt install libsndfile1-dev
pip install pyflac
```

---

## Fazit
🎯 **plibflac = DEINE WAHL**
- Perfekt für Library-Scan, Batch, MFCC
- Einfacher Code
- pyFLAC nur für Streaming/Real-time

---

**Fragen/Feedback:**
- Weitere FLAC-Workflow-, Streaming- oder Feature-Beispiele gewünscht?
