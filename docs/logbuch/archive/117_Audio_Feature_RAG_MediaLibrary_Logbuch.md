# Logbuch: Audio-Feature Extraction für RAG/Media-Library

## Datum: 10. März 2026

---

## Thema: MFCC-Feature Extraction & Integration in RAG-Pipeline

### Verbesserter Audio-Processor (librosa/torchaudio/mutagen)
```python
import torchaudio
import librosa
import numpy as np
from pathlib import Path
from mutagen import File as AudioFile

def audio_node(audio_path: str):
    """
    Extrahiert MFCC-Features aus Audio → TextNode für RAG/Embeddings
    Unterstützt: WAV, MP3, FLAC, M4A, OGG
    """
    try:
        y, sr = librosa.load(audio_path, sr=22050, duration=30)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_delta = librosa.feature.delta(mfcc)
        features = {
            'mfcc_mean': np.mean(mfcc, axis=1).tolist(),
            'mfcc_delta_mean': np.mean(mfcc_delta, axis=1).tolist(),
            'duration': len(y) / sr,
            'tempo': librosa.beat.tempo(y=y, sr=sr)[0],
            'spectral_centroid': float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))),
        }
        filename = Path(audio_path).name
        text = (
            f"Audio: {filename} | "
            f"Dauer: {features['duration']:.1f}s | "
            f"Tempo: {features['tempo']:.0f} BPM | "
            f"MFCC: {np.mean(features['mfcc_mean']):.2f}"
        )
        return {
            'text': text,
            'metadata': {
                'path': audio_path,
                'features': features,
                'sr': sr
            }
        }
    except Exception as e:
        return {'error': f"Audio Fehler {audio_path}: {str(e)}"}

def complete_audio_node(audio_path: str):
    audio_file = AudioFile(audio_path)
    meta = {
        'title': audio_file.get('title', ['Unbekannt'])[0],
        'artist': audio_file.get('artist', ['Unbekannt'])[0],
        'album': audio_file.get('album', ['Unbekannt'])[0],
        'duration': audio_file.info.length if audio_file.info else 0
    }
    node = audio_node(audio_path)
    node['metadata'].update(meta)
    node['text'] = f"{meta['title']} by {meta['artist']} | {node['text']}"
    return node
```

---

### Eel-Integration
```python
@eel.expose
def process_audio_library(audio_paths):
    results = []
    for path in audio_paths:
        node = complete_audio_node(path)
        results.append(node)
    return json.dumps(results)

@eel.expose
def audio_search(query_embedding, audio_features):
    similarities = []
    for i, feat in enumerate(audio_features):
        mfcc_sim = np.dot(query_embedding, feat['mfcc_mean']) / (np.linalg.norm(query_embedding) * np.linalg.norm(feat['mfcc_mean']))
        similarities.append({'index': i, 'similarity': float(mfcc_sim)})
    return json.dumps(sorted(similarities, key=lambda x: x['similarity'], reverse=True))
```

---

### Installation & Abhängigkeiten
```bash
pip install librosa torchaudio soundfile numpy mutagen
```

---

### Performance-Tipps
- Batch-Processing: librosa.load parallel mit multiprocessing
- Cache: Features in SQLite speichern
- Short-Cuts: Nur 10-30s Clip laden (duration=30)

---

### Use-Cases
- RAG/Audio-Suche: Embeddings via MFCC
- Media-Library: Metadaten + Features für Suche, Inventur, Recommendation
- JS-Frontend: Ergebnisse als Tabelle/Live-Grid

---

**Fragen/Feedback:**
- Welche Audio-Formate nutzt du (FLAC/MP3/M4A)?
- Weitere Feature- oder Embedding-Beispiele gewünscht?
