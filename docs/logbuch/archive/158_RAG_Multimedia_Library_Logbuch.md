# Logbuch: RAG Library für Multimedia-Sammlung

## Datum: 10. März 2026

---

## Thema: Retrieval-Augmented Generation (RAG) – LlamaIndex, Chroma, Ollama, Supabase

### Beste RAG Frameworks (2026)
| Framework    | Best For      | Features                  | Install                  |
|--------------|--------------|---------------------------|--------------------------|
| LlamaIndex   | Produktion   | Multimodal, 300+ Connectors| pip install llama-index  |
| LangChain    | Agents       | Scrapy/OCR, MCP/A2A       | pip install langchain-community |
| Haystack     | Multilingual | DE Bücher/PDFs            | pip install farm-haystack|
| RAGFlow      | Visual       | No-Code Pipeline          | Docker                   |
| FlashRAG     | Research     | Benchmarks                | pip install flashrag     |

**Empfehlung:** LlamaIndex – einfach, multimodal, Ollama-native

---

### Voll-RAG Library Code (LlamaIndex + Chroma + Ollama)
```python
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.file import PDFReader, SimpleDirectoryReader
from llama_index.core.schema import TextNode
import chromadb
from pathlib import Path

Settings.llm = Ollama(model="llama3.2:3b", request_timeout=60.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

class MultimediaRAG:
    def __init__(self, persist_dir="./rag_library"):
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_or_create_collection("multimedia")
        self.vector_store = ChromaVectorStore(chroma_collection=self.collection)
        self.index = None
    def add_media(self, paths):
        nodes = []
        for path in paths:
            if path.suffix == '.pdf':
                reader = PDFReader()
                docs = reader.load_data(path)
                nodes.extend(docs)
            elif path.suffix in ['.mp3', '.flac']:
                from mutagen import File
                audio = File(path)
                text = f"{audio.get('title', [''])[0]} - {audio.get('artist', [''])[0]}\nLyrics: {audio.get('lyrics', [''])[0]}"
                node = TextNode(text=text, metadata={'path': path, 'type': 'audio'})
                nodes.append(node)
            else:
                docs = SimpleDirectoryReader(input_files=[path]).load_data()
                nodes.extend(docs)
        self.index = VectorStoreIndex(nodes, storage_context=StorageContext.from_defaults(vector_store=self.vector_store))
    def query(self, question):
        retriever = self.index.as_retriever(similarity_top_k=5)
        nodes = retriever.retrieve(question)
        context = "\n".join([n.text for n in nodes])
        response = Settings.llm.complete(f"Frage: {question}\nKontext: {context}\nAntwort:")
        return {
            'answer': response.text,
            'sources': [n.metadata['path'] for n in nodes]
        }

# Usage
rag = MultimediaRAG()
rag.add_media(['song.mp3', 'ebook.pdf', 'notes.odt'])
result = rag.query("Welche Python Bücher habe ich?")
print(result)
```

---

### Multimodal Erweiterung (Audio/Video)
```python
import torchaudio
import librosa
from llama_index.core.schema import TextNode

def audio_node(audio_path):
    y, sr = librosa.load(audio_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    text = f"Audio: {Path(audio_path).name} MFCC Features"
    return TextNode(text=str(mfcc.mean(axis=1)), metadata={'path': audio_path})
```

---

### Supabase Hybrid (pgvector)
```python
def save_embedding(text, embedding, path):
    client.rpc('match_documents', {
        'query_embedding': embedding.tolist(),
        'match_threshold': 0.78,
        'match_count': 10
    }).execute()
```

---

### Vorteile
| Feature     | Benefit                  |
|-------------|--------------------------|
| Multimodal  | Audio-Transkripte + PDF + ODF |
| Realtime    | Supabase Subscriptions   |
| Scale       | 1M+ Docs                 |

---

### Test
- `rag.add_media(['test.pdf'])`
- `rag.query('Zusammenfassung')`

---

**Fragen/Feedback:**
- LlamaIndex oder LangChain Agentic RAG gewünscht?
- Weitere Multimodal- oder Supabase-Integrationsbeispiele?
