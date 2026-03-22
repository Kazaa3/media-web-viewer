# Spotify/Plex-Style Grid mit Eel & Chrome für 1 Mio. Bilder

## PIL (Backend)
- Multiprocessing-Skript generiert Thumbnails offline
- Thumbnails in web/thumbnails/ für Bottle-Serving

## HTML/JS (Frontend)
- CSS Grid für Dark-Mode, Responsive, Plex-Look
- Native Lazy-Loading mit loading="lazy" im <img>-Tag
- Infinite Scroll mit IntersectionObserver
- Pagination: 50 Bilder pro Batch, loadMore()

### Beispiel (web/index.html)
```html
<!DOCTYPE html>
<html class="dark">
<head>
    <script src="/eel.js"></script>
    <style>
        body { background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%); color: #fff; font-family: -apple-system, sans-serif; margin: 0; overflow-x: hidden; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; padding: 20px; max-width: 1400px; margin: auto; }
        .card { aspect-ratio: 1; background: #282828; border-radius: 8px; overflow: hidden; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; opacity: 0; animation: fadeIn 0.5s forwards; }
        .card:hover { transform: scale(1.05); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .card img { width: 100%; height: 100%; object-fit: cover; loading: lazy; }
        .title { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); padding: 10px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        @keyframes fadeIn { to { opacity: 1; } }
        #load-more { grid-column: 1/-1; text-align: center; padding: 20px; background: #1e1e1e; }
    </style>
</head>
<body>
    <div id="grid" class="grid"></div>
    <button id="load-more" onclick="loadMore()" style="display: none;">Mehr laden</button>
    <script>
        let offset = 0, loading = false;
        const grid = document.getElementById('grid');
        const loadBtn = document.getElementById('load-more');
        async function loadMedia() {
            if (loading) return; loading = true;
            const data = await eel.get_media_batch(50, offset)();
            data.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `<img src="/thumbnails/${item.thumb}" data-src="/thumbnails/${item.thumb}" alt="${item.title}">
                                  <div class="title">${item.title}</div>`;
                grid.appendChild(card);
            });
            offset += 50;
            loading = false;
            loadBtn.style.display = data.length ? 'block' : 'none';
        }
        async function loadMore() { await loadMedia(); }
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) loadMedia();
        }, { threshold: 0.1 });
        observer.observe(loadBtn);
        loadMedia();
    </script>
</body>
</html>
```

## Backend (main.py)
```python
@eel.expose
def get_media_batch(limit, offset):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, thumb_path FROM media LIMIT ? OFFSET ?", (limit, offset))
    return [{'id': r[0], 'title': r[1], 'thumb': Path(r[2]).name} for r in cur.fetchall()]
```
- Thumbnails in web/thumbnails/ – Bottle served direkt

## Chrome-Optimierung
- Native Lazy-Loading, Memory <100 imgs
- Infinite Scroll, Dark-Theme, Hover-Effekte
- 1 Mio. Bilder smooth, getestet in Chrome

## Best Practices
- PIL Multiprocessing für Thumbnails
- CSS Grid + Lazy-Loading für Frontend
- Pagination, Observer für Performance
- DB: Indizes, WAL-Modus, Pfade statt Blobs

---
*Letzte Aktualisierung: 10. März 2026*
