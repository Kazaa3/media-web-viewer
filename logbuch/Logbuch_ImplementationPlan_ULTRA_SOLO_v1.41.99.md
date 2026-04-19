# Implementation Plan – v1.41.99 ULTRA-SOLO

This plan delivers a high-speed singleton startup and a guaranteed sub-navigation population.

---

## User Review Required
**IMPORTANT**
- **Zero-Latency Singleton:** I am removing the slow psutil process walk. From now on, the app will use a single, ultra-fast `fuser` command to clear its port (8345) and then start immediately. This will fix the "ultra long" startup.

**CAUTION**
- **Sub-Menu Restoration:** I found that the sub-menu was being redefined locally in every call. I am moving the navigation map to a global constant to prevent any race conditions or data loss during fragment loading.

---

## Proposed Changes

### Startup Engine (Zero-Latency)
- **[MODIFY] main.py**
  - **Port Burner:** Implement a high-speed `subprocess.run(["fuser", "-k", "8345/tcp"])` at the very beginning of the file.
  - **Structural Cleanup:** Unify the scattered `if __name__ == "__main__"` blocks and configuration checks into a single, efficient entry point.

### Navigation Logic (Atomic)
- **[MODIFY] ui_nav_helpers.js**
  - **Global Map:** Move `subNavMap` outside of `updateGlobalSubNav` to make it a persistent global constant.
  - **Force population:** Ensure that whenever the main menu (STATUS, Player, etc.) is clicked, the sub-nav is immediately and forcefully updated using the global map.

### Layout Enforcements
- **[MODIFY] main.css**
  - **Geometry Guard:** Add `!important` flags to the `#sub-nav-container` and `.sub-pill-btn` classes to ensure no other styles can hide them.

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Startup Speed:** Verify the app starts in < 2 seconds.
- **Persistence:** Click "STATUS", then "Player", then "STATUS" again. Verify pills appear every time.
- **Ghost Check:** Verify that starting the app twice results in the second instance successfully killing the first one.
