# discogs-artwork: Album Cover Scraper für deine Toolbox

## Repo: tassche/discogs-artwork
- [GitHub: tassche/discogs-artwork](https://github.com/tassche/discogs-artwork)

---

## Features
- Einfaches Download von Album-Artwork via Discogs API
- Throttling: 1 Request/Sekunde, max. 1000 Images/Tag/IP
- Caching: Bilder werden lokal gespeichert (Standard: ~/.covers)
- Batch-fähig, Threading (ArtworkWorker)

---

## Hauptfunktionen
- `get_random(artist, album, year=None)`: Zufälliges Release, Bild downloaden
- `get_largest(artist, album, year=None)`: Größtes verfügbares Bild downloaden
- `get_cache(artist, album, year=None, alt=get_random)`: Artwork aus Cache holen, sonst downloaden

**Exceptions:**
- DiskError, ImageNotFoundError, ReleaseNotFoundError, ResourceError

---

## Beispiel (example.py)
```python
from artwork import get_largest
try:
    path = get_largest('Arcade Fire', 'Funeral', year=2004)
    print('Artwork gespeichert:', path)
except Exception as e:
    print('Fehler:', e)
```

---

## Terminal-Ausgabe
```
DEBUG:opening http://api.discogs.com/database/search?year=2004&release_title=Funeral&type=master&artist=Arcade+Fire took 0.366 seconds
DEBUG:6 releases found for Funeral by Arcade Fire
DEBUG:opening http://api.discogs.com/releases/2482966 took 0.382 seconds
DEBUG:1 primary images found in release 2482966 and 0 secondary images
DEBUG:opening http://api.discogs.com/image/R-2482966-1286497707.jpeg took 1.35 seconds
DEBUG:artwork saved as Arcade Fire - 2004 - Funeral.jpeg
DEBUG:retrieving image took 2.59 seconds
```

---

## Integration-Tipps
- Batch-Download: Loop über Album/Artist-Liste
- Caching: Vermeidet API-Limits, ideal für große Libraries
- Fehlerhandling: Exceptions abfangen, Logging nutzen
- Threading: ArtworkWorker für parallele Downloads

---

## Empfehlung
- Perfekt für Media-Library, Supabase/NiceGUI, Eel-Integration
- Kombinierbar mit Discogs/MusicBrainz für Metadaten + Cover

---

**Frage:**
Soll discogs-artwork als Batch-Tool für Cover-Download integriert werden?
