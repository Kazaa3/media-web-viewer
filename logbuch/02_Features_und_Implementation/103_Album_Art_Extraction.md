# Album Art aus Audio-Dateien – Workflow für Media-Library

## Album-Cover extrahieren (mutagen)
- Extrahiere Cover aus MP3/FLAC/M4B mit mutagen
- PIL für Thumbnails (500x500px, dann 200x200px für Grid)
- Pfad in DB speichern, Thumbnail in web/thumbnails/ für Eel/Chrome-GUI

### Beispiel (audio_art.py)
```python
from mutagen import File
from PIL import Image
from io import BytesIO
from pathlib import Path
import shutil

def extract_album_art(audio_path, output_dir='covers/'):
    Path(output_dir).mkdir(exist_ok=True)
    audio = File(audio_path)
    if audio is None: return None
    for key in audio:
        if 'APIC' in str(key) or 'cover' in key.lower():
            art_data = audio[key].data
            img = Image.open(BytesIO(art_data))
            thumb_path = Path(output_dir) / f"{Path(audio_path).stem}_cover.jpg"
            img.thumbnail((500, 500), Image.Resampling.LANCZOS)
            img.save(thumb_path, 'JPEG', quality=90)
            return str(thumb_path)
    return None
```

## Batch-Scan für Ordner
```python
def scan_audio_for_art(audio_dir):
    for audio_file in Path(audio_dir).glob('**/*.[mM][pP]3'):
        art_path = extract_album_art(audio_file)
        if art_path:
            # DB updaten: add_media(..., cover_path=art_path)
            pass
```
- Für 1 Mio. Dateien: multiprocessing Pool nutzen

## Integration in Eel/DB/GUI
- @eel.expose für scan_and_extract_art
- Thumbnail nach web/thumbnails/ kopieren
- DB mit cover_path aktualisieren
- JS: Button ruft eel.scan_and_extract_art auf, Grid refresh

## Missing Album Art mit MusicBrainz (musicbrainzngs)
- Suche per Artist/Album aus mutagen-Tags
- Lade Cover-URL, speichere Thumb
- Rate-Limit: 1 Request/Sekunde

### Beispiel (musicbrainz_art.py)
```python
import musicbrainzngs
from mutagen import File
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

musicbrainzngs.set_useragent("MediaLibrary/1.0", "peter@example.com")
musicbrainzngs.set_rate_limit(1, 1)

def fetch_missing_art(audio_path, output_dir='covers/'):
    audio = File(audio_path)
    if audio is None: return None
    artist = audio.get('artist', ['Unknown'])[0]
    album = audio.get('album', ['Unknown'])[0]
    title = audio.get('title', [''])[0]
    try:
        result = musicbrainzngs.search_releases(f'artist:"{artist}" AND release:"{album}"', limit=1)
        if not result['release-list']['release']: return None
        release_mbid = result['release-list']['release'][0]['id']
    except: return None
    images = musicbrainzngs.get_image_list(release_mbid)
    if not images['images']: return None
    front_image = next((img for img in images['images'] if img.get('front')), images['images'][0])
    thumb_url = front_image['thumbnails']['250']
    resp = requests.get(thumb_url)
    img = Image.open(BytesIO(resp.content))
    thumb_path = Path(output_dir) / f"{Path(audio_path).stem}_cover.jpg"
    img.save(thumb_path, 'JPEG', quality=90)
    return str(thumb_path)
```

## Alternativen zu MusicBrainz für Album Art
| API/Lib      | Vorteile                        | Nachteile                | Code-Snippet                |
|--------------|----------------------------------|--------------------------|-----------------------------|
| Discogs      | Hohe Qualität, detaillierte Releases, Thumbs | Token nötig, 1000 Images/Tag | pip install discogs-client |
| Spotify      | Tolle 640px Covers, Playlists    | App-Registrierung, Rate-Limit | pip install spotipy        |
| Last.fm      | Einfach, schnelle Suche          | Niedrige Qualität (300px), API-Key | pip install pylast        |
| Beets        | Alles-in-einem (Tags + Art), MusicBrainz/Discogs-Fallback | CLI-fokussiert              | pip install beets           |
| CoverLovin2  | Automatisiert Downloads (Google Images Fallback) | Weniger präzise              | pip install CoverLovin2     |

### Discogs Beispiel
```python
import discogs_client
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

d = discogs_client.DiscogsClient('MediaLibrary/1.0', user_token='DEIN_TOKEN')

def fetch_discogs_art(artist, album, output_dir='covers/'):
    Path(output_dir).mkdir(exist_ok=True)
    results = d.search(f'{album} {artist}', type='release', per_page=1)
    if not results:
        return None
    release = results[0]
    if release.images:
        img_url = release.images[0].url_full
        resp = requests.get(img_url)
        img = Image.open(BytesIO(resp.content))
        thumb_path = Path(output_dir) / f"{album.replace(' ', '_')}_cover.jpg"
        img.thumbnail((500, 500))
        img.save(thumb_path, 'JPEG', quality=90)
        return str(thumb_path)
    return None
```

### Spotify Beispiel
```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='ID', client_secret='SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def fetch_spotify_art(artist, album):
    results = sp.search(q=f'artist:{artist} album:{album}', type='album', limit=1)
    if results['albums']['items']:
        return results['albums']['items'][0]['images'][0]['url']
```

### Batch & Fallback-Strategie
```python
def get_art(audio_path):
    art = extract_album_art(audio_path)
    if not art:
        audio = File(audio_path)
        artist, album = audio['artist'][0], audio['album'][0]
        art = (fetch_discogs_art(artist, album) or
               fetch_spotify_art(artist, album) or
               fetch_lastfm_art(artist, album))
    return art
```

## Multiprocessing & Rate-Limiting für Album Art & Thumbnails
- multiprocessing.Pool für parallele Verarbeitung
- ratemate für API-Limits (MusicBrainz, Discogs, Spotify)
- PIL/Mutagen sind thread-safe, APIs brauchen Delay

### Beispiel (batch_art.py)
```python
import multiprocessing as mp
from functools import partial
import time
from ratemate import RateLimit  # pip install ratemate
import musicbrainzngs
from pathlib import Path

def process_single_file(args):
    audio_path, output_dir = args
    api_limit = RateLimit(max_count=1, per=1)
    api_limit()  # Rate-Limit hit!
    art_path = extract_album_art(audio_path, output_dir)
    if not art_path:
        audio = File(audio_path)
        artist, album = audio.get('artist', [''])[0], audio.get('album', [''])[0]
        art_path = fetch_missing_art(audio_path, output_dir)
    if art_path:
        create_thumbnail(art_path, f"{art_path}_thumb.jpg")
        # DB insert
    return audio_path, art_path

def batch_process_audio(audio_dir, output_dir='covers/', workers=mp.cpu_count()):
    musicbrainzngs.set_rate_limit(1, 1)
    audio_files = list(Path(audio_dir).rglob('*.[mM][pP]3')) + list(Path(audio_dir).rglob('*.flac'))
    args = [(p, output_dir) for p in audio_files]
    with mp.Pool(workers) as pool:
        results = pool.map(process_single_file, args)
    success = sum(1 for _, art in results if art)
    print(f"Fertig: {success}/{len(results)} Covers gefunden!")

if __name__ == "__main__":
    batch_process_audio('/volume1/ABC/01 Medien/', workers=4)
```

### PIL-Thumbs ohne API
```python
def batch_thumbs_mp(image_dir, thumb_dir, size=(200,200)):
    images = list(Path(image_dir).glob('*.jpg'))
    args = [(p, thumb_dir, size) for p in images]
    with mp.Pool() as pool:
        pool.map(process_image, args)
```

## API-spezifische Tipps
| API        | Multiprocessing-Tipp           |
|------------|-------------------------------|
| MusicBrainz| set_rate_limit(1,1) + ratemate|
| Discogs    | Token + 40/min, Pool mit 1-2  |
| Spotify    | Client-Credentials, asyncio   |

## Eel-Expose für On-Demand
```python
@eel.expose
def process_file_batch(file_paths):
    with mp.Pool(4) as pool:
        results = pool.map(process_single_file, [(p, 'covers/') for p in file_paths])
    return results
```
- JS: eel.process_file_batch(['/song1.mp3', '/song2.mp3'])() → Progress-Update

## Best Practices
- Für 1 Mio.: Logging, Resume, Checkpoint-DB
- ratemate für API-Limits, time.sleep nur als Fallback

---
*Letzte Aktualisierung: 10. März 2026*
