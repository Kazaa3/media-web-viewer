# Moderne DB + GUI für Multimedia/RAG-App (2026-Standard)

## Stack-Überblick
| Layer     | Tool/Tech           |
|-----------|---------------------|
| Frontend  | NiceGUI (Vue3/Tailwind, realtime) |
| Backend   | FastAPI + Celery (Scraping/Processing) |
| DB        | Supabase Postgres + pgvector (Embeddings, Realtime) |
| AI        | Ollama RAG (Chroma) + Scraper (Playwright/Selenium) |
| Deploy    | Docker + Railway/Neon |

---

## Supabase: Moderne Postgres-DB
- Realtime-Subscriptions, Vector-Search (pgvector), Auth, Storage
- Perfekt als Plex/Spotify-Backend

**Local Setup:**
```bash
docker-compose up  # supabase start
```
**Python Client:**
```python
from supabase import create_client, Client
import os
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)
data, count = supabase.table('media').select("*").eq('type', 'audio').execute()
```
**Vector RAG:**
```python
supabase.rpc('match_documents', {'query_embedding': embedding, 'match_threshold': 0.78})
```
**Schema:**
```sql
CREATE TABLE media (
    id UUID PRIMARY KEY,
    path TEXT,
    type TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    ai_tags TEXT[]
);
```

---

## NiceGUI: Moderne Web-GUI
- Vue3/Tailwind, realtime, charts, DB-Tables
- Spotify/Plex-Look, responsive

**Code:**
```python
from nicegui import ui, app
import asyncio
from supabase import Client
client = Client(SUPABASE_URL, SUPABASE_KEY)
async def load_media(type_filter='all'):
    data = client.table('media').select("*").eq('type', type_filter).execute()
    with ui.grid(columns=6).classes('gap-4'):
        for item in data.data:
            ui.card().classes('w-full h-48 shadow-xl hover:scale-105 transition-all bg-gradient-to-br from-slate-900 to-slate-700').on('click', lambda: open_media(item))
            ui.image(item['thumbnail'] or '/placeholder.jpg').classes('w-full h-40 object-cover rounded-t-lg')
            ui.label(item['title']).classes('text-white p-2 font-semibold')
def open_media(item):
    ui.dialog().open()
    with ui.card():
        ui.html(f"<video src='{item['path']}' controls class='w-full'></video>")
        ui.button('Scrap Metadata', on_click=lambda: scrape_web(item['url']))
ui.timer(1.0, load_media, once=False)
with ui.tabs().classes('w-full').props('vertical swipeable'):
    ui.tab('Media')
    ui.tab('Scraper')
    ui.tab('RAG')
    with ui.tab_panel():
        load_media()
        ui.button('Filter Audio', on_click=lambda: load_media('audio'))
ui.run(title='Multimedia RAG App', dark=True)
```

---

## Scraper + RAG
**Scraper:**
```python
import asyncio
from playwright.async_api import async_playwright
async def scrape_web(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        metadata = await page.eval_on_selector('meta[property="og:title"]', 'el => el.content')
        client.table('media').insert({'url': url, 'metadata': metadata}).execute()
```
**RAG Wissensdatenbank:**
```python
from chromadb import Client as ChromaClient
chroma = ChromaClient()
collection = chroma.get_or_create_collection("knowledge")
```

---

## Deploy (1-Klick)
**Railway/Docker:**
```dockerfile
FROM python:3.12
COPY . /app
RUN pip install nicegui supabase
CMD ["nicegui", "--host", "0.0.0.0"]
```
**Neon Postgres:** Free Tier, AI-ready Vector-DB

---

## Warum dieser Stack "top modern"?
| Feature    | Supabase + NiceGUI |
|------------|--------------------|
| Realtime   | Postgres Changes live |
| AI/RAG     | pgvector + Ollama |
| GUI        | Tailwind/Vue3, responsive |
| Scraper    | Playwright async |
| Scale      | Serverless, 1M+ Records |

---

## Start
- pip install nicegui supabase
- supabase init
- Code kopieren → localhost:8080

---

**Frage:**
Möchtest du Supabase Account nutzen oder Docker local starten?
