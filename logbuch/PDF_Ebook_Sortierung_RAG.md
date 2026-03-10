# PDF/Ebook-Sortierung & Wissensdatenbank (RAG/LLM)

## Heise/Golem-Empfehlungen für deine Library

### Calibre
- Organisiert PDFs/EPUBs nach Metadaten (Autor, Titel, Tags)
- Konvertiert, sortiert, dedupliziert
- Integration mit deiner DB möglich
- Web-GUI (calibre-manage-server)
- Python-API für Batch-Sortierung: `pip install calibre`

**Install:**
```bash
flatpak install flathub net.calibre_ebook.calibre
calibre-manage-server  # Web-GUI wie Plex
```

### PDF24 Creator
- Seiten sortieren per Drag&Drop
- Für Metadaten/Batch besser Calibre nutzen

---

## Wissensdatenbank aus PDFs (RAG/LLM)

**Workflow:**
1. Parse PDFs → Embeddings → Vector-DB (Chroma/FAISS)
2. LLM-Suche (Ollama, GPT)

**Python-Beispiel:**
```python
# pip install langchain chromadb ollama pypdf
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain_ollama import OllamaLLM

loader = PyPDFLoader("ebook.pdf")
docs = loader.load_and_split()
embeddings = OllamaEmbeddings(model="llama3")
vectorstore = Chroma.from_documents(docs, embeddings)
llm = OllamaLLM(model="llama3")
query = "Was sagt das PDF zu KI-Sortierung?"
results = vectorstore.similarity_search(query)
response = llm.invoke(f"Antworte basierend auf: {results}")
```

**Batch:** Multiprocessing PDFs laden → große SQLite + Vector-Index

---

## Erweiterte DB-Struktur
```sql
CREATE TABLE ebooks (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE,
    title TEXT,
    author TEXT,
    vector_embedding BLOB,  -- Chroma-Export
    ai_tags TEXT  -- LLM-Kategorien
);
```

---

## Integration in deine Library
- Calibre importiert/sortiert PDFs → Metadaten in DB
- PyPDF/Unstructured extrahiert Text
- Ollama + Chroma baut Wissens-DB (local, offline)
- Eel/JS: "Frage PDF-DB" → Antwort + Links

---

## GitHub-Projekte
- [ai-file-sorter](https://github.com/hyperfield/ai-file-sorter)
- [langchain](https://github.com/hwchase17/langchain)
- [chromadb](https://github.com/chroma-core/chroma)
- [ollama](https://github.com/ollama/ollama)

---

## Voll-Setup (Heise/Golem-Style)
1. Calibre installieren/importieren
2. PDFs sortieren, Metadaten in DB
3. RAG-Code für Wissensdatenbank

---

**Frage:**
Möchtest du zuerst Calibre installieren und PDFs sortieren, oder direkt den RAG-Code für Wissensdatenbank integrieren?
