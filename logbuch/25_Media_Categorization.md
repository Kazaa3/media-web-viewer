<!-- Category: UI/UX -->

# Media Categorization

## Automatic Detection
The system automatically categorizes media based on:
- **File Extensions**: `.m4b` is always treated as a **Hörbuch** (audiobook), while `.mp3`, `.flac`, `.wav` are generally **Audio**.
- **Folder Structure**: If a parent directory contains "audiobooks", "hörbuch", etc., the items are categorized accordingly.

## Support for New Types
The backend is prepared to handle:
- **Audio** (Music, Podcasts)
- **Album**
- **Compilation**
- **Single**
- **Hörbuch** (Audiobooks)

Missing:
- **Video** (Movies, Clips)
- **Serie** (TV Shows)
- **Dokument / E-Book** (.pdf, .epub)

## Sidebar Integration
The category is displayed as a badge in the sidebar and influences which player features (like chapter navigation) are prioritized.
