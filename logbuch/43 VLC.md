## VLC Tab Integration (Media Library)

### 🎵 VLC Tabs & Playlists → Deine App
**VLC Tabs**: Playlist | Media Library | History. Deine App kann **VLC-Playlists importieren** und im **Eel/Vue-Player** abspielen!

### 1. VLC Playlist Export (m3u8/XSPF)
**VLC → Datei** (Rechtsklick Playlist → "Playlist speichern"):
View > Playlist → Rechtsklick > "Als Playlist speichern"
Format: .m3u8 (UTF-8) oder .xspf (XML/JSON-ähnlich)
​
​

text
**Beispiel m3u8:**
#EXTM3U
#EXTINF:-1,Song Title
/media/01 - Sommernacht.mp3
#EXTINF:-1,Next Track
/media/02 - Regenzeit.mp3

text

### 2. Python: m3u8 → Dein Dict-Format
```python
import m3u8  # pip install m3u8

def import_vlc_playlist(m3u_file: str) -> list[dict]:
    playlist = m3u8.load(m3u_file)
    media_list = []
    for segment in playlist.segments:
        path = segment.absolute_uri
        # Dein Parser!
        meta = parse_file(path)  
        media_list.append(to_dict(meta))
    return media_list  # → SQLite/json.dumps()
Integration in main.py:

python
@app.route('/import_vlc')
def vlc_import():
    m3u_path = request.query.m3u
    media = import_vlc_playlist(m3u_path)
    save_to_db(media)
    return json.dumps(media)
3. Python-vlc Bindings (direkt steuern)
bash
pip install python-vlc  # VLC extern starten[3]
python
import vlc

def play_in_vlc(media_list: list):
    instance = vlc.Instance()
    player = instance.media_list_player_new()
    
    media_list_vlc = []
    for media in media_list:
        m = instance.media_new(media['path'])
        media_list_vlc.append(m)
    
    player.set_media_list(media_list_vlc)
    player.play()  # Öffnet VLC-Fenster!
Eel-Button: "extern_vlc": play_in_vlc(current_playlist)

4. Web-Interface (VLC 3.x+)
VLC Web-Tab (http://localhost:8080):

text
Tools > Preferences > Interface > Web
→ JSON-API für Playlist/Media Library[4]
Python Request:

python
import requests
vlc_api = requests.get("http://localhost:8080/requests/playlist.json")
playlist = vlc_api.json()  # → Dein Dict!
5. Bidirektional: App ↔ VLC
text
Deine App (JSON) ─── m3u8/XSPF ─── VLC Playlist Tab
     ↑                                       ↓
  python-vlc     ←─── python-vlc ───── VLC extern
     │
  Import/Export Button in Vue.js GUI
Features:

✅ Import VLC .m3u8 → Media-Dict

✅ Export App-Playlist → VLC-kompatibel

✅ Extern VLC starten (python-vlc)

✅ VLC Web-API (JSON Playlist sync)

6. Implementation (5 Minuten)
requirements.txt +1:

text
m3u8
python-vlc
Vue-Button:

xml
<button @click="importVLCPlaylist('/path/playlist.m3u8')">
  📥 VLC Playlist laden
</button>
Perfekt für deine Multi-Format Library (MP3/FLAC/M4B → VLC)
