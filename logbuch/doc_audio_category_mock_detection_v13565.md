# Documentation: Audio Category & Mock Detection Logic (v1.35.65)

## Purpose
This logic is used throughout the Media Web Viewer to identify audio items and mock entries for filtering, diagnostics, and queue management.

---

## Audio & Mock Detection Logic
The following JavaScript snippet was used to determine if an item is an audio type or a mock:

```javascript
    i.is_mock === true ||
    i.category === 'Audio' ||
    i.category === 'Album' ||
    i.category === 'Hörbuch' ||
    i.category === 'Klassik' ||
    i.category === 'Podcast' ||
    i.category === 'Compilation' ||
    i.category === 'Single' ||
    i.category === 'Radio'
```

---

## Explanation
- **i.is_mock === true**: Detects mock/test items injected for diagnostics or UI testing.
- **i.category === ...**: Matches common audio-related categories, including internationalized and genre-specific types:
  - Audio
  - Album
  - Hörbuch (Audiobook)
  - Klassik (Classical)
  - Podcast
  - Compilation
  - Single
  - Radio

---

## Usage
- Used in queue filtering, diagnostic hydration, and UI badge logic.
- Ensures that only relevant audio or mock items are included/excluded as needed for diagnostics or user playback.

---

*This logic is current as of v1.35.65 and should be referenced for all audio/mock detection in the project.*
