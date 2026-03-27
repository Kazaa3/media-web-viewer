# MPV.js WASM Integration & Nomenklatur-Standardisierung – Walkthrough

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## 1. Backend Security: COOP/COEP für WASM
- **COOP/COEP aktiviert:**
  - Bottle-Server liefert jetzt die Header:
    - `Cross-Origin-Opener-Policy: same-origin`
    - `Cross-Origin-Embedder-Policy: require-corp`
  - Ermöglicht SharedArrayBuffer für High-Performance-WASM (mpv.js)

## 2. ISO Streaming Route
- **/iso-stream/**-Route implementiert:
  - Unterstützt HTTP Range Requests für effizientes Streaming großer ISO-Dateien
  - Optimiert für direkte Übergabe an mpv-wasm im Browser

## 3. WASM Bridge & Frontend
- **mpv-player.js:**
  - Initialisiert libmpv WASM-Umgebung
  - Brückt Keyboard-Events (Pfeile, Enter) für DVD/Blu-ray-Menüs
  - API: play, pause, seek, menu, overlay
- **UI-Integration:**
  - `<canvas id="mpv-canvas">` + Overlay im Hauptplayer
  - ISO-Dateien triggern automatisch den mpv-wasm-Flow

## 4. Nomenklatur-Standardisierung
- **Muster:**
  - "Source Format zu Target Protocol" (z.B. "FFmpeg fMP4 zu MSE")
- **Projektweit umgesetzt:**
  - UI, Logbuch, Code-Kommentare, Kontextmenüs

---

## 5. Hinweise & Ausblick
- **Binaries:** mpv.wasm/mpv.js müssen im Verzeichnis `web/js/mpv-wasm/` bereitgestellt werden
- **Zukunft:**
  - Erweiterung auf UHD/3D, Multi-Audio, Untertitel
  - Automatische Erkennung und Umschaltung je nach Dateityp

---

**Siehe diese Walkthrough-Datei für alle Details zu Änderungen, Testfällen und zukünftigen Deployments.**
