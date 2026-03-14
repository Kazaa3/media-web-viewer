# Scrapy Spider für Amazon/eBay (Anti-Bot, Scale)

## Projekt Setup (5 Min)
```bash
pip install scrapy scrapy-rotating-proxies pandas
scrapy startproject multimedia_scraper
cd multimedia_scraper
```
**scrapy.cfg (Proxies):**
```text
[settings]
DEFAULT_REQUESTS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
ROTATING_PROXY_LIST_PATH = 'proxies.txt'
```

---

## Amazon Spider (spiders/amazon_spider.py)
```python
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.de']
    start_urls = ['https://www.amazon.de/s?k=python+buch']
    custom_settings = {
        'FEEDS': {'amazon_products.json': {'format': 'json'}},
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }
    def parse(self, response):
        products = response.css('#searchResults .s-result-item')
        for product in products[:10]:
            yield {
                'title': product.css('h2 a::text').get(),
                'price': product.css('.a-price-whole::text').get(),
                'asin': product.css('h2 a').attrib.get('href').split('/dp/')[1].split('/')[0],
                'image': product.css('img::attr(src)').get(),
                'rating': product.css('.a-icon-alt::text').get()
            }
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

---

## pipelines.py (Supabase Sync)
```python
class SupabasePipeline:
    def process_item(self, item, spider):
        supabase.table('media').upsert(dict(item)).execute()
        return item
```

---

## Run
```bash
scrapy crawl amazon -o products.json
```

---

## eBay Spider (spiders/ebay_spider.py)
```python
class EbaySpider(scrapy.Spider):
    name = 'ebay'
    start_urls = ['https://www.ebay.de/sch/i.html?_nkw=python+buch']
    def parse(self, response):
        products = response.css('.srp-results .s-item')
        for product in products:
            yield {
                'title': product.css('h3.s-item__title::text').get(),
                'price': product.css('.s-item__price::text').get(),
                'ebay_id': product.css('::attr(data-itemid)').get(),
                'image': product.css('img::attr(src)').get()
            }
```

---

## Voll-Eel/NiceGUI Launcher
```python
@eel.expose
def run_scrapy_spider(store, query):
    os.chdir('multimedia_scraper')
    cmd = f'scrapy crawl {store} -a query="{query}" -o scraped.json'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    load_scraped_data()
```

---

## Pro-Tips 2026
- Proxies: ScrapeOps/BrightData
- Headless: scrapy-playwright für JS
- Scale: Scrapyd + Cluster

---

## Empfehlung
- Starte: scrapy crawl amazon → JSON → Supabase
- Amazon oder eBay Spider erweitern?

---

**Frage:**
Soll Amazon oder eBay Spider als nächstes erweitert werden?
