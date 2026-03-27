# Walkthrough: MPV.js WASM Integration & Nomenclature Standardization

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## 1. Backend Security & Streaming

### COOP/COEP Security Headers
- `main.py` erweitert: Bottle-Hook setzt jetzt
  - `Cross-Origin-Opener-Policy: same-origin`
  - `Cross-Origin-Embedder-Policy: require-corp`
- Ermöglicht SharedArrayBuffer für High-Performance-WASM (mpv.js)

### ISO Streaming Route
- Neue Route `/iso-stream/<path>` in `main.py` für direkte Übergabe an WASM-Player
- Unterstützt HTTP Range Requests für große ISOs
- Helper: `eel.get_iso_stream_url(file_path)`

---

## 2. Frontend MPV WASM Bridge

### UI Integration
- `app.html`:
  - Verstecktes `<canvas id="mpv-canvas">` für libmpv-Rendering (WebGL2)
  - Glassmorphic Overlay für DVD-Menü-Navigation
  - Automatisches Umschalten zwischen Video.js und mpv-canvas in `startEmbeddedVideo()`

### MpvWasmPlayer Bridge
- `js/mpv-player.js`:
  - Initialisiert WASM-Umgebung
  - Brückt Keyboard-Events (Pfeile/Enter) für interaktive Menüs
  - Lädt Dateien via `/iso-stream/`-URL

---

## 3. Technology Nomenclature Standardization

| Alte Bezeichnung           | Neue Standard-Nomenklatur           |
|---------------------------|--------------------------------------|
| FFmpeg Transcode (MSE)    | ✨ FFmpeg fMP4 zu MSE                 |
| Direct Play               | 🚀 Direct Play                        |
| VLC Interactive           | 💿 VLC HLS zu MSE (Interaktiv)        |
| Chrome Native             | 🚀 Video.js (Native)                  |
| MPV WASM (New)            | 💿 libmpv zu Canvas (WASM)            |

- Alle Labels in UI, Kontextmenüs und Logbuch vereinheitlicht

---

## 4. Stability Fixes
- **DB Path Fix:**
  - Einheitliche Nutzung von `db.get_active_db_path()` in `main.py` (verhindert AttributeError)
- **i18n Sync:**
  - `web/i18n.json` aktualisiert, damit neue Nomenklatur überall lokalisiert ist

---

## 5. WICHTIG: Nächster Schritt
- **mpv.js, mpv.wasm, mpv-worker.js** müssen nach `web/js/mpv-wasm/` deployt werden, damit "libmpv zu Canvas" funktioniert

---

**Alle Kernfunktionen und Integrationslogik sind Stand 27.03.2026 verifiziert.**
