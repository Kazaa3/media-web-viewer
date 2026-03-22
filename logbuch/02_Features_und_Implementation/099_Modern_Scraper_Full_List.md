# Vollständige Scraper-Liste für Supabase/NiceGUI-App

## Kategorieübersicht
| Kategorie   | Scraper/Lib      | Features                | Install                  | GitHub/Pypi                  |
|-------------|------------------|-------------------------|--------------------------|------------------------------|
| Film/TV     | Cinemagoer       | IMDb/TMDB, Poster, Cast | pip install cinemagoer   | github.com/cinemagoer/cinemagoer |
|             | OMDB             | Schnell, kostenlos      | pip install omdbapi      | pypi.org/project/omdbapi     |
|             | TMDB-Scraper     | Offizielle TMDB, TV     | pip install tmdbv3api    | Apify                        |
| Music       | Discogs          | Releases, Covers, Labels| pip install discogs-client| Token                        |
|             | MusicBrainz      | Metadaten + Covers      | pip install musicbrainzngs| Dein Favorit                 |
|             | AcousticID       | Fingerprint → MusicBrainz| pip install pyacoustid   | Audio-ID                     |
| Buch/Ebook  | Google Books     | ISBN/Titel, Thumbs      | pip install google-books-search|                            |
|             | ISBNdb           | Voll-Buchdaten          | Apify                    | ISBN-fokussiert              |
|             | OpenLibrary      | Free API, Covers        | pip install openlibrary  | Public Domain                |
| Podcasts    | ListenNotes      | Suche + Episoden        | pip install listennotes  | API-Key                      |
|             | PodcastIndex     | RSS + Transcripts       | requests                 | Free API                     |
| Web/Generic | Playwright       | JS-Rendering, Anti-Bot  | pip install playwright   | Modern Selenium              |
|             | Scrapy           | Crawler-Framework       | pip install scrapy       | Pro-Level                    |
|             | BeautifulSoup    | HTML-Parsing            | pip install bs4 lxml     | Basis                        |

---

## Master-Scraper Funktion
```python
SCAPER_MAP = {
    'movie': cinemagoer_movie,
    'music': discogs_music,
    'book': google_books,
    'tv': tmdbv3api_tv,
    'podcast': listennotes_search
}
async def universal_scraper(query, media_type):
    scraper = SCAPER_MAP.get(media_type)
    if scraper:
        data = await scraper(query)
        supabase.table('media').insert(data).execute()
        return data
    return "Unbekannter Typ"
# NiceGUI
ui.select(['movie', 'music', 'book', 'tv', 'podcast'], label='Typ')
ui.input('Query')
ui.button('Scrapen!', on_click=lambda: asyncio.create_task(universal_scraper(query.value, typ.value)))
```

---

## Batch-Multi-Scraper
```python
import asyncio
queries = [
    ('Inception', 'movie'),
    ('Beatles Abbey Road', 'music'),
    ('1984 Orwell', 'book')
]
async def batch_scrape_all():
    tasks = [universal_scraper(q, t) for q, t in queries]
    results = await asyncio.gather(*tasks)
    return results  # Realtime Grid-Update
```

---

## Pro-Tipps
- Playwright für dynamische Sites (Netflix/YouTube)
- Scrapy Cluster für 1M+ Batch
- Rate-Limits: Async + Proxy (BrightData)

---

## Empfehlung
- Nächster Schritt: Cinemagoer + Discogs kombinieren für Film/Music-Meta
- Playwright für Web-Videos/Podcasts

---

**Frage:**
Soll Cinemagoer + Discogs kombiniert werden, oder Playwright für Web-Videos/Podcasts integriert werden?
