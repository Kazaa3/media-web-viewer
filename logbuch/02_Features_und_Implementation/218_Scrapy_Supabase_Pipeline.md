# Scrapy → Supabase: Voll-Pipeline für Amazon (Batch, Realtime)

## 1. JSON-Export (Einfach)
**settings.py:**
```python
FEEDS = {
    'scraped_amazon.json': {
        'format': 'json',
        'overwrite': True,
        'indent': 2
    }
}
```
**Run:**
```bash
scrapy crawl amazon -s FEEDS='{"scraped_amazon.json": {"format": "json"}}'
```
**JSON → Supabase:**
```python
import json
from supabase import Client
with open('scraped_amazon.json', 'r') as f:
    products = json.load(f)
client.table('media').insert(products).execute()
print(f"{len(products)} Produkte importiert!")
```

---

## 2. Supabase Pipeline (Direkt, realtime)
**pipelines.py:**
```python
from itemadapter import ItemAdapter
from supabase import create_client, Client
class SupabasePipeline:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.client.table('media').upsert(data).execute()
        spider.logger.info(f"Upserted: {data['title']}")
        return item
    def close_spider(self, spider):
        self.client.close()
```
**settings.py:**
```python
ITEM_PIPELINES = {
    'multimedia_scraper.pipelines.SupabasePipeline': 300,
}
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = 0.5
```
**Run:**
```bash
scrapy crawl amazon  # → Direkt Supabase!
```

---

## 3. NiceGUI Launcher + Monitor
```python
@eel.expose
async def launch_amazon_scraper(query):
    os.chdir('multimedia_scraper')
    process = subprocess.Popen([
        'scrapy', 'crawl', 'amazon', '-a', f'query={query}'
    ])
    ui.notify('Scraper läuft... Realtime in DB!')
    return process.pid
```
- Realtime Grid: Supabase postgres_changes → Auto-Refresh

---

## Voll-Amazon Spider (Erweitert)
**spiders/amazon_spider.py:**
```python
import scrapy
class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f'https://www.amazon.de/s?k={query}'] if query else []
    def parse(self, response):
        for product in response.css('.s-result-item'):
            yield {
                'title': product.css('h2 span::text').get(),
                'price': product.css('.a-price-whole::text').get(),
                'asin': response.urljoin(product.css('h2 a::attr(href)').get()).split('dp/')[1].split('/')[0],
                'image': product.css('img::attr(src)').get(),
                'rating': product.css('[aria-label*="out of"]::text').get()
            }
```
**Test:**
```bash
scrapy crawl amazon -a query="Python Buch"
```

---

## Empfehlung
- Pipeline aktivieren für direkte Supabase-Integration (realtime, batch-safe)
- JSON-Test für einfache Imports

---

**Frage:**
Soll die Supabase-Pipeline aktiviert werden oder zuerst ein JSON-Test laufen?
