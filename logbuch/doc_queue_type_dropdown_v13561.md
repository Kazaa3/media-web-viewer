# Documentation: Media Type Dropdown for Queue Filtering (v1.35.61)

## Purpose
This dropdown enables real-time filtering of the player queue by media type, providing a premium, glassmorphic UI and seamless user experience.

---

## UI Markup
```html
<div style="display: flex; gap: 10px; align-items: center;">
    <select id="queue-type-filter" onchange="if(typeof changeQueueFilter === 'function') changeQueueFilter(this.value)"
        style="padding: 6px 12px; font-size: 11px; font-weight: 700; border-radius: 8px; background: var(--bg-primary); border: 1px solid var(--border-color); color: var(--text-primary); cursor: pointer; outline: none; transition: border-color 0.2s;">
        <option value="all">Alle Medien</option>
        <option value="audio">Nur Audio</option>
        <option value="video">Nur Video</option>
        <option value="iso">Nur ISO/Abbilder</option>
        <option value="transcoded">Nur Transcoded</option>
    </select>
</div>
```

---

## Integration
- **Location:** Top-right of the Queue Pane, next to "Liste leeren".
- **Options:**
  - Alle Medien (all)
  - Nur Audio (audio)
  - Nur Video (video)
  - Nur ISO/Abbilder (iso)
  - Nur Transcoded (transcoded)
- **Styling:**
  - Glassmorphic, modern, and accessible.
  - Uses CSS variables for theme consistency.
- **Logic:**
  - Calls `changeQueueFilter(value)` on change.
  - Filtering is handled in `audioplayer.js` via `filterQueueByType()` and `renderPlaylist()`.

---

## Usage
- Select a filter to instantly update the queue view without reloading the app.
- Ensures high-fidelity diagnostic and user experience for all media types.

---

*This dropdown is part of the v1.35.61 diagnostic and filtering upgrade.*
