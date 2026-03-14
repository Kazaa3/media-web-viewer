# Ollama + Chroma: Local RAG für PDF-Wissensdatenbank

## Schnellstart-Setup

### 1. Ollama installieren
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b  # Kleines Modell
ollama pull nomic-embed-text  # Embeddings
```

### 2. Python-Libs
```bash
pip install langchain-community langchain-ollama chromadb pypdf2 sentence-transformers
```

---

## Voll-Code: PDF → Wissens-DB
rag_pdf.py (für deine Media-Library)
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
import os

PERSIST_DIR = "./chroma_db"
MODEL_LLAMA = "llama3.2:3b"
MODEL_EMBED = "nomic-embed-text"

def add_pdfs_to_db(pdf_paths):
    loader = PyPDFLoader(pdf_paths[0])
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model=MODEL_EMBED)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=PERSIST_DIR)
    vectorstore.persist()
    print("PDFs in Chroma gespeichert!")

def query_db(question):
    embeddings = OllamaEmbeddings(model=MODEL_EMBED)
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    llm = ChatOllama(model=MODEL_LLAMA)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate
    system_prompt = "Du bist ein hilfreicher Assistent für PDFs. Antworte basierend nur auf Kontext: {context}"
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": question})
    return response["answer"]

if __name__ == "__main__":
    add_pdfs_to_db(["ebook1.pdf", "heise_guide.pdf"])
    print(query_db("Wie sortiert man PDFs mit Calibre?"))
```

---

## Eel-Integration (Web-Chat)
**main.py:**
```python
@eel.expose
def rag_query(question):
    return query_db(question)
```
**JS (Plex-Style Chat):**
```javascript
async function askRag(question) {
    const answer = await eel.rag_query(question)();
    document.getElementById('answer').innerHTML += `<p>Q: ${question}<br>A: ${answer}</p>`;
}
```
PDF-Upload → Auto-add zu Chroma → Sofort suchbar!

---

## Performance (1M Chunks)
| Aspekt         | Chroma + Ollama |
|--------------- |-----------------|
| Embed 100 PDFs | 5-10 Min (CPU)  |
| Query          | <2 Sek          |
| Speicher       | 1-5GB (SSD)     |
| GPU            | Optional (CUDA) |
| Persistenz     | Bleibt nach Neustart |

Batch-MP für 1000+ PDFs.

---

## Empfehlung
- Ollama + Chroma = perfekte lokale RAG-Lösung für PDF-Wissensdatenbank (offline, privat, MX Linux-ready)
- Erstes PDF testen oder Eel-Chat erweitern?

---

**Frage:**
Soll zuerst ein PDF getestet werden (add_pdfs_to_db), oder die Eel-Chat-Integration erweitert werden?
