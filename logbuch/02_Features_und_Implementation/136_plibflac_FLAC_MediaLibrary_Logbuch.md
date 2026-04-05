# Logbuch: plibflac für FLAC in Media-Library

## Datum: 10. März 2026

---

## Thema: plibflac – Spezialisierte Python-Library für FLAC (Samples/Metadaten)

### Installation
```bash
pip install plibflac  # Oder: pip install pyFLAC
sudo apt install libflac-dev  # System-Abhängigkeit
```

---

### Grundlagen: FLAC lesen/schreiben
```python
import plibflac
from pathlib import Path

def flac_node(flac_path: str):
    with plibflac.Decoder(flac_path) as decoder:
        info = {
            'sample_rate': decoder.sample_rate,
            'channels': decoder.channels,
            'bits_per_sample': decoder.bits_per_sample,
            'total_samples': decoder.total_samples,
            'duration': decoder.total_samples / decoder.sample_rate
        }
        samples = decoder.read(10 * decoder.channels)
        sample_preview = [float(s[0]) for s in samples[:10]]
        metadata = decoder.metadata or {}
        filename = Path(flac_path).name
        text = (
            f"FLAC: {filename} | "
            f"⏱️ {info['duration']:.1f}s | "
            f"🔊 {info['sample_rate']}Hz | "
            f"📡 {info['channels']}ch | "
            f"Samples: {len(sample_preview)}"
        )
        return {
            'text': text,
            'metadata': {
                'path': flac_path,
                'info': info,
                'sample_preview': sample_preview,
                'tags': metadata
            }
        }

def write_flac(input_audio, output_path: str, compression=8):
    with plibflac.Encoder(output_path, compression_level=compression,
                         channels=2, bits_per_sample=16, sample_rate=44100) as encoder:
        encoder.write(input_audio)
```

---

### Eel-Integration
```python
@eel.expose
def process_flac(flac_path: str):
    node = flac_node(flac_path)
    return json.dumps(node)

@eel.expose
def batch_flac(folder: str):
    import glob
    flacs = glob.glob(folder + "/*.flac")
    results = [flac_node(f) for f in flacs[:10]]
    return json.dumps(results)
```

---

### plibflac vs. Alternativen
| Library   | Speed | Metadaten | Samples | Installation |
|-----------|-------|-----------|---------|--------------|
| plibflac  | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐ | Mittel       |
| mutagen   | ⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐    | ❌      | Einfach      |
| librosa   | ⭐⭐⭐   | ⭐⭐⭐      | ⭐⭐⭐⭐   | Einfach      |
| pyFLAC    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐ | System-lib   |

**plibflac Vorteile:**
- Raw Samples (für MFCC/DSP)
- Keine Dekompression nötig
- Streaming (große Dateien)

---

### Kombi: plibflac + mutagen + librosa
```python
def ultimate_flac_node(flac_path: str):
    from mutagen.flac import FLAC
    tags = FLAC(flac_path)
    flac_info = flac_node(flac_path)
    import librosa
    y, sr = librosa.load(flac_path, sr=22050, duration=10)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(axis=1)
    return {
        'text': f"{tags.get('title', [''])[0]} | {flac_info['text']}",
        'metadata': {
            **flac_info['metadata'],
            'tags': {k: v[0] for k, v in tags.items()},
            'mfcc': mfcc.tolist()
        }
    }
```

---

### JS-Call
```javascript
async function analyzeFlac(file) {
    const result = await eel.process_flac(file.path)();
    const node = JSON.parse(result);
    console.log('FLAC:', node.text);
    // Vue-Table updaten
}
```

---

### Fazit
- Perfekt für FLAC in deiner Pipeline, wenn Raw-Audio-Samples gebraucht werden (DSP/MFCC)
- Sonst mutagen + librosa reicht
- Test: `with plibflac.Decoder("test.flac") as d: print(d.sample_rate)`

---

**Fragen/Feedback:**
- Weitere FLAC-Workflow- oder Feature-Beispiele gewünscht?
