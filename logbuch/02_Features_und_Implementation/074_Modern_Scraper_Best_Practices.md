# Moderne Scraper für Film/Music/Buch (Supabase/NiceGUI)

## Film-Scraper (TMDB/IMDb)
- **Cinemagoer:**
```python
from cinemagoer import Cinemagoer
ia = Cinemagoer()
def scrape_movie(title, year=None):
    movies = ia.search_movie(title, year=year)
    movie = movies[0]
    ia.update(movie)
    data = {
        'title': movie['title'],
        'year': movie.get('year'),
        'rating': movie.get('rating'),
        'genres': movie.get('genres'),
        'poster': ia.get_data('data', movie.movieID, 'main')['poster']
    }
    supabase.table('media').insert(data).execute()
    return data
# Batch
movies = ['Inception', 'Oppenheimer']
for m in movies:
    scrape_movie(m)
```
- **OMDB:** pip install omdbapi (schnell, kostenlos)

---

## Music-Scraper
- **Discogs:**
```python
import discogs_client
d = discogs_client.DiscogsClient('token')
def scrape_music(artist, album):
    results = d.search(f'{album} {artist}', type='release')
    release = results[0]
    data = {
        'artist': release.artists[0].name,
        'album': release.title,
        'year': release.year,
        'cover': release.images[0].url_full if release.images else None
    }
    return data
```
- **MusicBrainz:** musicbrainzngs + CoverArt

---

## Buch-Scraper
- **Google Books:**
```python
from google_books_search import GoogleBooksSearch
def scrape_book(isbn_or_title):
    books = GoogleBooksSearch(query=isbn_or_title, order_by='relevance', lang='de')
    book = books.results[0]
    data = {
        'title': book.title,
        'authors': book.authors,
        'thumbnail': book.thumbnail
    }
    return data
```

---

## Multi-Scraper in NiceGUI
```python
async def scrape_all(url_or_query, media_type):
    if media_type == 'movie':
        data = scrape_movie(url_or_query)
    elif media_type == 'music':
        artist, album = url_or_query.split(' - ')
        data = scrape_music(artist, album)
    elif media_type == 'book':
        data = scrape_book(url_or_query)
    supabase.table('media').insert(data).execute()
    ui.notify(f"Gefunden: {data['title']}")
    load_media()
# GUI
with ui.row():
    ui.select(['movie', 'music', 'book'], value='movie').props('dense').bind_value(ui.input('Query (z.B. Inception)'), 'value')
    ui.button('Scrapen!', on_click=lambda: asyncio.create_task(scrape_all(query.value, typ.value)))
```

---

## Voll-Batch (1M Files)
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
async def batch_scrape(queries, scraper_type):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [loop.run_in_executor(executor, scrape_movie if scraper_type=='movie' else ..., q) for q in queries]
        results = await asyncio.gather(*tasks)
    return results
```
- Pipeline: Datei → Fingerprint (AcousticID) → Scraper → Embeddings → Supabase → RAG-Suche

---

## Empfehlung
- Starte mit dem Scraper-Typ, der für deine App am wichtigsten ist (Film/Music/Buch)
- Test: scrape_movie('Dune 2021') → DB + Grid

---

**Frage:**
Welchen Typ möchtest du zuerst integrieren (Film/Music/Buch)?
