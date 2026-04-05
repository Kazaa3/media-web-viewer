# Implementation Plan — Emergency Hotfix & UI Polish (v1.35.51)

## Overview
Two critical blockers were identified: a Python syntax error in main.py and UI overlap from the Red Diagnostic Bar. This plan addresses both issues and polishes the diagnostic UI.

## 🛠️ Key Goals
- **Syntax Hotfix [DONE]:**
  - Corrected the double @eel.expose decorator in main.py (line 1194). Application now boots successfully.
- **Diagnostic Header Relocation:**
  - Transform the Red Top Bar into a floating bottom-right console.
  - **Position:** bottom: 74px; right: 24px (just above the glassmorphic footer).
  - **Style:** Slightly translucent, rounded corners (border-radius: 8px), modern widget look.
  - **Visibility:** Top menus remain fully accessible.
- **Final Verification:**
  - With the boot fixed, 13 diagnostic items should appear in the queue and be playable.

## 📂 Files to Modify
- `web/js/diagnostics/gui_integrity.js`: Relocate header injection and update CSS.
- `web/js/version.js`: Increment to v1.35.51 for the new layout.

## 🧪 Expected Outcome
- On next boot, the "Diagnostic Mode" bar will float in the bottom-right, not covering tabs.
- All menus will be accessible, and 13 recovery items will be playable.

---

*This plan ensures a clean, accessible UI and resolves the last critical blockers for v1.35.51.*
