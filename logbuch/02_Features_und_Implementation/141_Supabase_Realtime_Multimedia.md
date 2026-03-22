# Supabase: Realtime Multimedia-App mit Scrapy

## Supabase Setup (Local/Cloud)

### Local Docker (5 Min)
```bash
npm install -g supabase
supabase init
supabase start
```
**Credentials:**
- SUPABASE_URL=localhost:54321
- SUPABASE_ANON_KEY=eyJ...

### Python Client
```bash
pip install supabase
```
```python
from supabase import create_client, Client
client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
data = {'title': 'Test Track', 'type': 'audio', 'path': '/song.mp3'}
client.table('media').insert(data).execute()
```

---

## Scrapy → Supabase Pipeline (Perfekt)
**pipelines.py:**
```python
from itemadapter import ItemAdapter
from supabase import create_client
class SupabaseRealtimePipeline:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.client.table('media').upsert(data).execute()
        spider.logger.info(f"✅ Live: {data.get('title', 'Unknown')}")
        return item
```
**settings.py:**
```python
ITEM_PIPELINES = {'yourproject.pipelines.SupabaseRealtimePipeline': 800}
```
**Run:**
```bash
scrapy crawl amazon
```
- Live in Supabase → NiceGUI Grid auto-updates!

---

## Realtime Subscription (Python)
```python
from supabase.lib.realtime_client import RealtimeSubscribeStates
def on_change(payload):
    print(f"🆕 New media: {payload['new']}")
channel = client.channel('media_db')
channel.on_postgres_changes(
    event='INSERT',
    schema='public',
    table='media',
    callback=on_change
).subscribe()
```
- Live-Updates: Scraper läuft → GUI refresht!

---

## Moderne Schema (Multimedia + RAG)
**Supabase SQL Editor:**
```sql
create extension vector;
create table media (
    id uuid primary key default uuid_generate_v4(),
    title text,
    artist text,
    type text check (type in ('audio', 'video', 'pdf', 'web')),
    path text,
    metadata jsonb,
    embedding vector(1536),
    scraped_at timestamptz default now()
);
create index on media using ivfflat (embedding vector_cosine_ops) with (lists = 100);
```

---

## Voll-NiceGUI + Supabase
```python
from nicegui import ui
from supabase import Client
client = Client(SUPABASE_URL, SUPABASE_KEY)
async def load_live_media():
    data = client.table('media').select('*').order('scraped_at', desc=True).limit(50).execute()
    ui.grid(columns=6).clear()
    for item in data.data:
        ui.card().classes('shadow-lg hover:shadow-xl')
        ui.image(item['thumbnail'] or 'placeholder.jpg')
        ui.label(item['title'])
ui.timer(2.0, load_live_media)
ui.run(port=8080)
```
- Scrapy läuft → DB live → GUI auto!

---

## Empfehlung
- supabase start für lokale Entwicklung
- Cloud-Account für Deployment

---

**Frage:**
Möchten Sie supabase start (local) oder Cloud-Account nutzen?
