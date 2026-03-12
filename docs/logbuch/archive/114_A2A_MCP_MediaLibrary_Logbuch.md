# Logbuch: A2A + MCP für Media-Library

## Datum: 10. März 2026

---

## Thema: Agent-to-Agent (A2A) & Model Context Protocol (MCP) – Multi-Agent KI-Integration

### Konzept
- **A2A:** KI-Agenten kommunizieren direkt, teilen Tools/Kontext
- **MCP:** Standard für Tool-Discovery, Kontext-Sharing, Multi-Agent-Workflows
- **Use-Case:** Audio-to-Album-Art, Scraper, RAG, Inventur – alles als Agenten

---

### Setup
1. **Installieren:**
   - `pip install python-a2a mcp`
2. **MCP-Server:**
   - Tools bereitstellen (z.B. Audio-Art, Scraper, RAG)
3. **A2A-Agent:**
   - Multi-Tool-Agent (MediaAgent) verbindet MCP-Tools
4. **Integration:**
   - Eel/Supabase: Ergebnisse in DB speichern, UI live

---

### Codebeispiel
#### MCP-Server (Audio-Art)
```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import mutagen

async def handle_a2a_request(params):
    audio_path = params.get('audio_path')
    art = extract_album_art(audio_path)
    return types.CreateMessageResult(content=f"Art: {art}")

async def run_mcp_server():
    server_params = StdioServerParameters(command=["python", "audio_server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await session.list_tools()

import asyncio
asyncio.run(run_mcp_server())
```

#### A2A Multi-Agent
```python
from python_a2a import A2AServer, FastMCPAgent

mcp_config = {
    "audio_art": {"command": ["python", "mcp_audio_server.py"]},
    "scraper": {"command": ["scrapy", "crawl", "amazon"]},
    "rag": {"url": "http://localhost:8080/rag"}
}

class MediaAgent(A2AServer, FastMCPAgent):
    def __init__(self):
        FastMCPAgent.__init__(self, mcp_servers=mcp_config)
    async def process_media_query(self, query):
        art_result = await self.call_mcp_tool("audio_art", "extract", audio_path="/song.mp3")
        amazon_data = await self.call_mcp_tool("scraper", "search", query="Python Buch")
        rag_answer = await self.call_mcp_tool("rag", "query", question="Beste Bücher?")
        return self.combine_results(art_result, amazon_data, rag_answer)

agent = MediaAgent()
```

#### Eel/Supabase Integration
```python
@eel.expose
async def agent_query(query):
    result = await agent.process_media_query(query)
    client.table('agent_results').insert(result).execute()
    return result
```

---

### Vorteile
| Feature      | Benefit                |
|--------------|------------------------|
| Multi-Agent  | Audio + Scraper + RAG parallel |
| Tool Discovery | Agents finden MCP-Tools auto |
| Realtime     | MCP SSE für Live-Updates |
| Scale        | MCP-Server clusterbar   |

---

### Demo
- Audio → A2A ruft MCP → Art + Preise → Supabase
- `python-a2a` installieren oder MCP-Server zuerst starten

---

**Fragen/Feedback:**
- Weitere Agenten-Workflows oder Tool-Integration gewünscht?
