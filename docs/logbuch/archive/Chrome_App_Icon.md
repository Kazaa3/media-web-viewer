# Chrome: Custom Icon für Media Web Viewer

## Ziel
Dem Media Web Viewer eine eigene Icon-Grafik (z.B. "dict"-Logo) als Chrome-App-Icon zuweisen, damit die Anwendung im Browser und als Desktop-Verknüpfung eindeutig erkennbar ist.

## Vorgehen
1. **Favicon im HTML:**
Im `<head>` von `web/app.html` einbinden:
```html
<link rel="icon" type="image/png" href="/web/assets/dict_icon.png">
```
2. **Manifest für Chrome-App:**
Optional kann ein `manifest.json` im `web/`-Ordner ergänzt werden:
```json
{
  "name": "Media Web Viewer",
  "short_name": "dict",
  "icons": [
    {
      "src": "/web/assets/dict_icon.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ],
  "start_url": "/web/app.html",
  "display": "standalone"
}
```
3. **Icon-Datei:**
- Die Datei `dict_icon.png` sollte im Ordner `web/assets/` liegen.
- Empfohlene Größe: 192x192 oder 256x256 Pixel.

## Status
- Favicon und Manifest ergänzen
- Chrome zeigt das Icon als App-Logo und in der Taskleiste

---
Letzte Aktualisierung: 11. März 2026
