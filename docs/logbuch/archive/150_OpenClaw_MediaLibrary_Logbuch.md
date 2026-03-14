# Logbuch: OpenClaw AI-Agent für Media-Library

## Datum: 10. März 2026

---

## Thema: OpenClaw – Open-Source AI-Agent für Multimedia-Automatisierung

### Was ist OpenClaw?
- Persönlicher AI-Mitarbeiter: Scrapt, organisiert Media, Chat-Interface (WhatsApp/Telegram/Web)
- Skills: Scrapy, OCR, Supabase, Album-Art, RAG
- Docker-local, offline-fähig, A2A/MCP-kompatibel

---

### Setup (MX Linux)
1. **Docker installieren:**
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```
2. **OpenClaw installieren:**
   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```
3. **Skills aktivieren:**
   ```bash
   openclaw skills install youtube-downloader music-album-art
   ```

---

### Skills für deine Library (A2A/MCP)
```yaml
# skills/media.yaml
name: Media Scraper
tools:
  - scrapy_amazon
  - ocr_scanner
  - supabase_insert
prompt: "Scrappe Media, scan Bücher, update Inventur"
```

---

### Chat-Kommandos
- "Scrap amazon python buch" → Scrapy → Supabase
- "Scan buchregal" → OCR → DB
- "Album art song.mp3" → mutagen → Cover

---

### Integration-Code (MCP-Tool)
```python
# mcp_scraper.py
from mcp.server.stdio import stdio_server
from mcp.types import CreateMessageResult
import subprocess

async def handle_scrape(params):
    query = params['query']
    result = subprocess.run(['scrapy', 'crawl', 'amazon', '-a', f'query={query}'], capture_output=True)
    return CreateMessageResult(content=result.stdout.decode())

if __name__ == "__main__":
    stdio_server().run()
```

---

### Supabase Realtime
```yaml
# OpenClaw config
realtime:
  supabase_url: "your_url"
  table: "media"
```

---

### Voll-Workflow
1. WhatsApp/Telegram: "Inventur Regal A1"
2. OpenClaw → OCR Scanner → Supabase → NiceGUI Live-Grid

---

### Vorteile
| Feature        | Benefit                |
|---------------|------------------------|
| No-Code Skills | Scrapy/OCR als Agent-Tools |
| Multi-Channel  | WhatsApp, Discord, Web |
| Docker         | Local/offline          |
| A2A            | Agenten-Kollaboration  |

---

**Fragen/Feedback:**
- OpenClaw für Library-Automatisierung oder Skill-Beispiele gewünscht?
- Weitere Integrations- oder Workflow-Tipps?
