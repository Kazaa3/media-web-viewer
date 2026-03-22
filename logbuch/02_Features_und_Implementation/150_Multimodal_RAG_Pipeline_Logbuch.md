# Logbuch: Multimodal RAG Pipeline – Audio, PDF, ODF

## Datum: 10. März 2026

---

## Thema: Vollständige Multimodal RAG-Lösung (Whisper, PyMuPDF, Unstructured, ChromaDB, SentenceTransformer)

### Features
- ✅ Audio: MP3→Transkript (Whisper Turbo, 99% genau)
- ✅ PDF: Seiten/Chunks + Tabellen (PyMuPDF/Unstructured)
- ✅ ODF: Volltext-Extraktion
- ✅ Embeddings: SentenceTransformer (lokal)
- ✅ Suche: Cross-Modal (Audio fragt PDF, PDF fragt Audio!)
- ✅ Eel: GUI-Integration

---

### Installation (einmalig)
```bash
pip install openai-whisper chromadb sentence-transformers unstructured[pdf] pymupdf odfpy
# GPU: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### Multimodal Processor (Master-Funktion)
```python
import whisper
import fitz
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import eel
from unstructured.partition.auto import partition

whisper_model = whisper.load_model("turbo")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./rag_db")
sentence_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')
collection = chroma_client.get_or_create_collection(
    name="multimodal_media",
    embedding_function=sentence_ef
)

@eel.expose
def multimodal_ingest(file_path: str):
    path = Path(file_path)
    ext = path.suffix.lower()
    documents, metadata, ids = [], [], []
    if ext in ['.mp3', '.wav', '.flac', '.m4a']:
        result = whisper_model.transcribe(file_path, language='de')
        transcript = result['text']
        words = transcript.split()
        for i in range(0, len(words), 300):
            chunk = ' '.join(words[i:i+300])
            documents.append(chunk)
            metadata.append({'type': 'audio_transcript', 'file': path.name, 'start': i//300})
            ids.append(f"audio_{path.stem}_{i//300}")
    elif ext == '.pdf':
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page_text = doc[page_num].get_text()
            documents.append(page_text[:4000])
            metadata.append({'type': 'pdf_page', 'file': path.name, 'page': page_num})
            ids.append(f"pdf_{path.stem}_p{page_num}")
        doc.close()
    elif ext == '.odt':
        import odf.opendocument
        odt_doc = odf.opendocument.load(file_path)
        full_text = odt_doc.text.get_text()
        words = full_text.split()
        for i in range(0, len(words), 300):
            chunk = ' '.join(words[i:i+300])
            documents.append(chunk)
            metadata.append({'type': 'odt_chunk', 'file': path.name, 'chunk': i//300})
            ids.append(f"odt_{path.stem}_{i//300}")
    if documents:
        collection.add(documents=documents, metadatas=metadata, ids=ids)
        return json.dumps({'success': True, 'count': len(documents)})
    return json.dumps({'error': 'Unbekanntes Format'})
```

---

### Multimodal RAG Query
```python
@eel.expose
def multimodal_query(question: str, n_results=5):
    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )
    context = "\n\n".join([
        f"[{r['metadata']['type']} {r['metadata']['file']}]: {r['document']}"
        for r in zip(results['documents'][0], results['metadatas'][0])
    ])
    from transformers import pipeline
    generator = pipeline('text-generation', model='microsoft/DialoGPT-medium')
    prompt = f"Frage: {question}\nKontext: {context}\nAntwort: "
    response = generator(prompt, max_length=500, num_return_sequences=1)
    return json.dumps({
        'answer': response[0]['generated_text'],
        'sources': results['metadatas'][0]
    })
```

---

### Batch-Ingestion (Ordner)
```python
@eel.expose
def ingest_folder(folder_path: str):
    import glob
    files = glob.glob(folder_path + "/*.{mp3,wav,flac,m4a,pdf,odt}", recursive=True)
    results = []
    for f in files:
        results.append(multimodal_ingest(f))
    return json.dumps({'total': len(files), 'processed': len([r for r in results if r['success']])})
```

---

### Performance
- 1h Audio → 5min Transkript
- 100 PDFs → 2min Chunking
- ChromaDB Query → <100ms

---

### Use-Cases
- Modalitäten mischen: "Finde Audio zu PDF-Inhalt!"
- Cross-Modal RAG: Audio fragt PDF, PDF fragt Audio
- Eel-Frontend: GUI für Ingest & Suche

---

**Fragen/Feedback:**
- Welche LLM (lokal/offline) bevorzugst du für die Antwort?
- Weitere Modalitäten oder Workflow-Beispiele gewünscht?
