# Documentation: isVideoItem Function — Category Map (v1.35.61)

## Purpose
The `isVideoItem(item)` function robustly determines if a media item should be classified as video, using both category and file extension checks. This is essential for accurate filtering, playback routing, and UI diagnostics in the Media Web Viewer.

---

## Category Map (videoCategories)
The following categories are recognized as video types:

- Film
- Serie
- ISO/Image
- Video
- Musikvideos
- Animes
- Cartoons
- Movie
- TV Show
- Movies
- TV Shows
- Animation
- Animations
- Documentary
- Dokumentation
- Concert
- Konzerte
- Sports
- Sport
- Clips
- Shorts
- Trailers

This list covers singular/plural, English/German, and common subtypes for international and legacy compatibility.

---

## Function Logic
```javascript
function isVideoItem(item) {
    if (!item) return false;
    // 1. Check Category
    const videoCategories = [
        'Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos', 'Animes', 'Cartoons', 'Movie', 'TV Show',
        'Movies', 'TV Shows', 'Animation', 'Animations', 'Documentary', 'Dokumentation', 'Concert',
        'Konzerte', 'Sports', 'Sport', 'Clips', 'Shorts', 'Trailers'
    ];
    if (item.category && videoCategories.includes(item.category)) return true;

    // 2. Check Extension
    const path = item.path || item.relpath || "";
    const videoExtensions = ['.mp4', '.mkv', '.iso', '.webm', '.avi', '.mov', '.ts', '.m2ts', '.vob', '.m4v', '.mpg', '.mpeg', '.flv', '.wmv'];
    const lowerPath = path.toLowerCase();
    return videoExtensions.some(ext => lowerPath.endsWith(ext));
}
```

---

## Usage
- Used throughout the app for context menus, playback routing, and queue filtering.
- Ensures all relevant video types are detected, including edge cases and internationalized categories.

---

*This function is up-to-date as of v1.35.61 and should be referenced for all video-type detection logic in the project.*
