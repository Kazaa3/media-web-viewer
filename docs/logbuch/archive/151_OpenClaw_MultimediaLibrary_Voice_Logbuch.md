# Logbuch: OpenClaw KI-Assistent für Multimedia-Library

## Datum: 10. März 2026

---

## Thema: OpenClaw – Open-Source KI-Assistent für Scraping, Inventur, RAG (Voice/Chat)

### Features
- **Voice Commands:** "Inventur Regal A1 scannen" → OCR → Supabase
- **Skills:** YouTube-Scraper, Album-Art, PDF-RAG
- **MCP-Tools:** Scrapy/Supabase als Agent-Tool
- **Realtime:** WhatsApp/Telegram/DB-Sync
- **Multi-Agent:** OCR + Scraper + RAG parallel
- **Offline:** Local LLM (llama3.2)

---

### 5-Min Setup (MX Linux)
```bash
curl -fsSL https://get.docker.com | sh
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw skills install --all
openclaw skills enable media-scraper rag-inventur
```

---

### Config (~/.openclaw/config.yaml)
```yaml
mcp_tools:
  - name: scrapy_amazon
    command: ["scrapy", "crawl", "amazon"]
  - name: ocr_scanner
    command: ["python", "ocr_gui.py"]
  - name: supabase_sync
    url: "http://localhost:54321/rest/v1/media"
llm: llama3.2
voice: de
```

---

### Voice/Media-Kommandos
- "Scrap Amazon Python Bücher" → Scrapy → Supabase live
- "Scan Buchregal" → OCR → Inventur
- "RAG: Beste Python Bücher?" → Chroma-Antwort
- "Album Art song.mp3" → mutagen → Cover
- "Supabase: Neue PDFs sync" → Calibre + DB

---

### MCP-Tool Beispiel (Scrapy)
```python
from mcp.server import Server
import subprocess
server = Server("Scrapy Tool")
@server.list_tools()
async def get_tools():
    return [{"name": "amazon_scrape", "description": "Scrapt Amazon Produkte"}]
@server.call_tool()
async def amazon_scrape(params):
    query = params["query"]
    result = subprocess.run(['scrapy', 'crawl', 'amazon', '-a', f'query={query}'], capture_output=True, text=True)
    return {"content": result.stdout}
server.run()
```

---

### Supabase Realtime
```yaml
skills:
  supabase_agent:
    realtime: true
    table: "physical_books"
```

---

### Voll-Integration
- Telegram: "Inventur starten"
- OpenClaw → OCR GUI → Supabase → NiceGUI Live-Grid

---

### Docker-Compose (OpenClaw + Supabase + NiceGUI)
```yaml
services:
  openclaw:
    image: openclaw:latest
  supabase:
    image: supabase/postgres
  nicegui:
    build: .
```

---

### Vorteile
| Feature      | Benefit                |
|--------------|------------------------|
| Voice Inventur | Hände-frei scannen    |
| Multi-Agent  | OCR + Scraper + RAG zusammen |
| Offline      | Local LLM              |

---

**Fragen/Feedback:**
- OpenClaw Voice testen oder MCP-Skill für Scrapy gewünscht?
- Weitere Integrations- oder Workflow-Tipps?
