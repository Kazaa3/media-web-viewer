# Logbuch: Screen Overlay Mini-Video (Picture-in-Picture)

**Datum:** 16. März 2026 (16:06 CET)

## Konzept: Mini-Video Overlay

Floating/PiP Player über GUI – kleines Video-Fenster, das über allen Tabs schwebt, dragbar, resizable, always-on-top. Perfekt für Multitasking (Code + Video).

### Features

- [x] Drag & Drop Position
- [x] Resize (100x80 bis 400x300)
- [x] Always-on-Top (über Eel)
- [x] Mute/Unmute Toggle
- [x] Play/Pause/Seek Controls
- [x] Fade-In/Out Animation
- [x] Close/Minimize
- [x] Backend-Stream (MediaMTX HLS/Direct)

### Implementation (Snippet)

#### 1. HTML/CSS Overlay (Eel Frontend)

```html
<!-- Mini-Overlay (draggable, resizable) -->
<div id="mini-video" class="mini-player hidden">
  <div class="mini-drag-handle">
    <span>▣</span> <!-- Drag Icon -->
    <button onclick="toggleMini()">❌</button>
  </div>
  <video id="mini-player" class="mini-video" muted loop playsinline>
    <source src="" type="application/x-mpegURL">
  </video>
  <div class="mini-controls">
    <button onclick="miniPlayPause()">⏸️</button>
    <button onclick="miniMute()">🔇</button>
  </div>
</div>
```

```css
.mini-player {
  position: fixed !important;
  top: 20px !important;
  right: 20px !important;
  width: 240px;
  height: 180px;
  background: #000;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  z-index: 99999 !important;
  cursor: move;
  transition: all 0.3s ease;
}
```

---
*Ergänzt am 16. März 2026 im Rahmen der Expanded Playback Erweiterung.*
