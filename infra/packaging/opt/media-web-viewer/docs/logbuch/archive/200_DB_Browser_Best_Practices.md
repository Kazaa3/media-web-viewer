# DB im Browser: sqlite-web & NiceGUI

## 1. sqlite-web (Plex-ähnlich, sofort)
- **Install:**
```bash
pip install sqlite-web
sqlite_web media_library.db --port 5001  # http://localhost:5001
```
- **Features:** Tabellen browsen/sortieren, SQL-Editor, JSON/CSV-Export, Add/Drop Columns
- **Docker:**
```bash
docker run -p 8080:8080 -v $(pwd)/media_library.db:/data.db coleifer/sqlite-web
```
- **Eel-Integration:**
```html
<a href="http://localhost:5001">DB öffnen</a>
```

---

## 2. NiceGUI DB-Viewer (Custom, Eel-Style)
- **Install:**
```bash
pip install nicegui sqlite3 pandas
```
- **Code:**
```python
from nicegui import ui
import sqlite3
import pandas as pd
DB_PATH = 'media_library.db'
async def refresh_table():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM media LIMIT 100", conn)
    table.clear()
    with table:
        ui.table(df.to_dict('records'), columns=df.columns.tolist(),
                 row_key='id', pagination={'pageSize': 20},
                 selection='single', on_row_click=edit_row)
    conn.close()
def edit_row(e):
    row = e.selected[0]
    ui.notify(f"Edit ID: {row['id']}")
with ui.card():
    ui.button('Refresh', on_click=refresh_table)
    ui.button('SQL Query', on_click=lambda: ui.input('SQL').run())
table = ui.table([], columns=[])
refresh_table()
ui.run(title='Media DB Viewer', port=8081)
```
- **Features:** Live-Sort/Filter, Pagination, Edit-Modals, Spotify-Grid-Style

---

## 3. Eel + sqlite-web Hybrid
- **main.py:**
```python
@eel.expose
def open_db_browser():
    import subprocess
    subprocess.Popen(['sqlite_web', DB_PATH, '--port', '5001', '--host', '0.0.0.0'])
    return "DB-Browser gestartet: localhost:5001"
```
- **JS:**
```javascript
eel.open_db_browser()
```

---

## 4. Voll-Integration (1-Klick)
- **db_viewer.html (Eel):**
```html
<button onclick="eel.open_db_browser()">DB im Browser öffnen</button>
<iframe id="db-frame" style="width:100%;height:70vh;display:none;"></iframe>
<script>
    eel.open_db_browser()(url => {
        document.getElementById('db-frame').src = url;
        document.getElementById('db-frame').style.display = 'block';
    });
</script>
```
- Embed sqlite-web direkt!

---

## Performance (1M Rows)
| Tool        | Pagination | Edit | Speed  |
|-------------|------------|------|--------|
| sqlite-web  | Ja (50/1000)| Voll | Blitz  |
| NiceGUI     | Ja (Custom)| Modal| Gut    |
| DB4S        | Ja         | Voll | Offline|

---

## Empfehlung
- Starte mit **sqlite-web**: pip install sqlite_web; sqlite_web media_library.db → localhost:5001
- NiceGUI für Custom-Viewer (Eel-Style)

---

**Frage:**
Möchtest du zuerst sqlite-web nutzen oder einen NiceGUI-Viewer custom bauen?
