# Dynamic Context Menu Logic: 'Open With' Implementation

## Overview
This logbook entry documents the design, implementation, and integration of dynamic context menu logic for file-type dependent "Open With" actions in the Media Library App. The goal is to enable users to right-click on media files and select context-aware actions, such as opening files with appropriate applications based on their extension or category.

## Motivation
- Enhance user experience by providing relevant actions for each media file.
- Support workflows for audio, video, image, and document files with tailored menu options.
- Enable extensibility for future integration of additional tools and actions.

## Design Principles
- **File-Type Detection:** Use file extension and category metadata to determine available actions.
- **Menu Generation:** Dynamically generate context menu items based on file type.
- **Extensibility:** Allow easy addition of new actions and applications.
- **Frontend-Backend Coordination:** Ensure menu logic is accessible from the frontend and can trigger backend actions via Eel/Bottle APIs.

## Implementation Steps
1. **File Metadata Extraction:**
   - Extract file extension and category from media item metadata (see `item.category`, `extStr` in app.html).
2. **Menu Logic (Frontend):**
   - Implement a context menu handler in JavaScript (script.js) that listens for right-click events on media items.
   - Generate menu items based on detected file type (e.g., "Open with VLC" for video, "Open with Audacity" for audio).
3. **Action Dispatch:**
   - On menu item selection, dispatch the action to the backend via Eel-exposed functions.
   - Backend validates and executes the requested action (e.g., launching an external application).
4. **UI Feedback:**
   - Provide visual feedback for action success/failure.

## Example Menu Generation Logic
```js
function getContextMenuItems(file) {
    const ext = file.extension.toLowerCase();
    const category = file.category || 'Unknown';
    const items = [];
    if (['mp4', 'mkv', 'avi'].includes(ext)) {
        items.push({ label: 'Open with VLC', action: 'open_vlc' });
        items.push({ label: 'Open with Premium Player', action: 'open_premium' });
    } else if (['mp3', 'flac', 'wav'].includes(ext)) {
        items.push({ label: 'Open with Audacity', action: 'open_audacity' });
    } else if (['jpg', 'png', 'gif'].includes(ext)) {
        items.push({ label: 'Open with Image Viewer', action: 'open_image_viewer' });
    }
    items.push({ label: 'Show Details', action: 'show_details' });
    return items;
}
```

## Integration Points
- **Frontend:** app.html, script.js (context menu handler, menu rendering)
- **Backend:** main.py, Eel-exposed functions for launching applications

## Testing & Validation
- Manual and automated tests for menu generation and action dispatch.
- Selenium E2E tests for context menu interaction and action execution.

## Future Enhancements
- Add support for custom user-defined actions.
- Integrate with OS-level "Open With" dialogs.
- Provide menu customization in settings.

---
**Status:**
- Context menu logic for file-type dependent actions is planned and ready for implementation.
- No existing code found; new system will be integrated as described above.

---
**Date:** 17. März 2026
**Author:** GitHub Copilot
