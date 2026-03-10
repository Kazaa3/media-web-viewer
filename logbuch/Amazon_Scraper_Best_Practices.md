# Amazon-Scraper für Film/Music/Bücher (Supabase/NiceGUI)

## Amazon PA-API 5.0 (Empfohlen)
- Offiziell, kostenlos (Affiliate-Account nötig)
- 1M Requests/Monat free

**Setup:**
```bash
pip install amazon-paapi5-python-sdk
```
**Code:**
```python
from paapi5_python_sdk.api.default_api import DefaultApi
api = DefaultApi(
    access_key='DEIN_ACCESS',
    secret_key='DEIN_SECRET',
    host='webservices.amazon.de',
    region='eu-west-1'
)
def scrape_amazon_products(keywords):
    response = api.search_items(
        partner_tag='DEIN_PARTNER-20',
        keywords=keywords,
        resources=['ItemInfo.Title', 'Images.Primary.Medium', 'Offers.Listings.Price', 'ItemInfo.Classifications']
    )
    products = []
    for item in response.search_result.items:
        data = {
            'title': item.item_info.title.display_value,
            'price': item.offers.listings[0].price.amount if item.offers else None,
            'image': item.images.primary.medium.url,
            'asin': item.asin
        }
        products.append(data)
    supabase.table('media').insert(products).execute()
    return products
scrape_amazon_products('Python Bücher')
```

---

## Scrapy Amazon (Anti-Bot)
- Für dynamische/Reviews
- Rotating Proxies + Headless Chrome (Playwright)

**Setup:**
```bash
pip install scrapy scrapy-rotating-proxies
```
**spider.py:**
```python
import scrapy
class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    def start_requests(self):
        urls = ['https://amazon.de/dp/B08N5WRWNW']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
    def parse(self, response):
        yield {
            'title': response.css('#productTitle::text').get().strip(),
            'price': response.css('.a-price-whole::text').get(),
            'rating': response.xpath('//span[@id="acrPopover"]/text()').get(),
            'asin': response.url.split('/dp/')[1].split('/')[0]
        }
```

---

## NiceGUI Amazon-Tab
```python
ui.input('Amazon Suche (z.B. Python Buch)')
ui.button('Scrapen!', on_click=lambda: asyncio.create_task(scrape_amazon_async(query.value)))
async def scrape_amazon_async(keywords):
    products = scrape_amazon_products(keywords)
    ui.notify(f"{len(products)} Produkte gefunden!")
    load_media()
```

---

## Voll-Liste (inkl. Amazon)
| Typ      | Amazon-API         | Scraper-Fallback |
|----------|--------------------|------------------|
| Film/DVD | PA-API ItemLookup  | Scrapy ASIN      |
| Music/CD | SearchItems('album')| Discogs          |
| Bücher   | BrowseNode('books')| Google Books     |
| Electronics | Variations      | Playwright       |

---

## Empfehlung
- Amazon PA-API für legalen, robusten Batch-Import
- Scrapy für dynamische Daten/Reviews
- Token: Amazon Associates (gratis) → PA-API Keys

---

**Frage:**
Möchtest du zuerst Amazon-Account für PA-API nutzen oder Scrapy Spider für dynamische Daten testen?
