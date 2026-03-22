# KI-gestütztes Sortieren & Tagging von Medien

## Überblick
Moderne Medienbibliotheken profitieren von KI-gestütztem Tagging und Sortieren. Mit OpenAI CLIP, LLMs (ChatGPT, Llama) und spezialisierten GitHub-Projekten kannst du Audio, Bilder und Metadaten automatisch klassifizieren und organisieren.

---

## Top GitHub-Projekte für AI-Tagging/Organizing
| Repo | Beschreibung | Tech | Stars/Link |
|------|--------------|------|------------|
| [ai-file-sorter](https://github.com/hyperfield/ai-file-sorter) | KI sortiert Downloads/Media per LLM (Llama/ChatGPT) in Ordner – perfekt für 1M Files! | Python, GTK, Local LLM | ⭐ |
| [ai-file-organizer](https://github.com/thebearwithabite/ai-file-organizer) | Lernt Verhalten, sortiert intelligent (ADHD-friendly) | Python, ML | ⭐ |
| [mediasorter](https://github.com/joshuaboniface/mediasorter) | Media-Sort nach TMDb/TVMaze (Filme/Serien/Audio) | Python, APIs | ⭐ |
| [Sortify](https://github.com/Mrtracker-new/Sortify) | AI-Content-Sort (Faces/Screenshots/Social Media) + NL-Commands | Python, ML | ⭐ |
| [CLIP (OpenAI)](https://github.com/openai/CLIP) | KI klassifiziert Bilder/Audio-Features per Text (z.B. "rock album cover") | PyTorch | ⭐ |
| [music-vibe-classifier](https://github.com/AhmedFalahQ/music-vibe-classifier) | Bild → Music-Genre via ResNet + YouTube-Playlists | SageMaker, Flask | ⭐ |

---

## Integration in deine DB/Library
### CLIP-Beispiel: KI-Tags aus Cover-Bildern
```python
pip install clip-by-openai torch
import clip
import torch
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def ai_classify_cover(thumb_path, candidates=["rock", "pop", "jazz", "classical", "electronic"]):
    image = preprocess(Image.open(thumb_path)).unsqueeze(0).to(device)
    text_tokens = clip.tokenize([f"a photo of a {c} album cover" for c in candidates]).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_tokens)
        probs = (100. * image_features @ text_features.T).softmax(dim=-1)
    top_genre = candidates[probs[0].argmax()]
    return top_genre  # Speichere in DB als 'ai_tag'
```

### Batch mit Multiprocessing
```python
def batch_ai_sort():
    conn = connect_db()
    thumbs = conn.execute("SELECT id, cover_thumb FROM media WHERE ai_tag IS NULL LIMIT 1000").fetchall()
    for row in thumbs:
        genre = ai_classify_cover(f"thumbnails/{row[1]}")
        conn.execute("UPDATE media SET ai_tag=? WHERE id=?", (genre, row[0]))
    conn.commit()
```

---

## LLM-Sort (ChatGPT/Local Llama)
Aus ai-file-sorter inspiriert:
```python
from openai import OpenAI  # Oder ollama
client = OpenAI(api_key="sk-...")
def llm_sort_metadata(metadata_json):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Sortiere diese Medien-Metadaten in Kategorien: {metadata_json}"}]
    )
    return response.choices[0].message.content  # z.B. "Party-Musik, Chill, Workout"
```

---

## Workflow für Integration
1. DB-Werte (Artist, Duration, Genre, Cover) auslesen
2. CLIP/LLM klassifiziert und vergibt ai_tag/ai_category
3. Update media-Tabelle: ai_tag/ai_category
4. Eel-GUI: ORDER BY ai_tag → Automatisch sortierte Grids

---

## Empfehlung
- **Für Cover-Bilder:** Starte mit CLIP für Genre/Tags.
- **Für Metadaten/Audio:** Nutze ai-file-sorter für LLM-Kategorisierung.
- Forke/clone das passende Repo, implementiere Batch-Tagging mit Multiprocessing, speichere KI-Tags in DB und sortiere im GUI.

---

## Links
- [ai-file-sorter](https://github.com/hyperfield/ai-file-sorter)
- [ai-file-organizer](https://github.com/thebearwithabite/ai-file-organizer)
- [mediasorter](https://github.com/joshuaboniface/mediasorter)
- [Sortify](https://github.com/Mrtracker-new/Sortify)
- [CLIP (OpenAI)](https://github.com/openai/CLIP)
- [music-vibe-classifier](https://github.com/AhmedFalahQ/music-vibe-classifier)

---

**Frage:**
Möchtest du zuerst CLIP für Cover-Bilder (Genre/Tags) oder ai-file-sorter für Metadaten/Audio (LLM-Kategorisierung) integrieren? Oder sollen spezifische Werte (z.B. Duration/Genre) priorisiert werden?
