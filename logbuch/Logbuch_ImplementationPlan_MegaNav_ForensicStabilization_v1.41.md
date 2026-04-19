# Implementation Plan – Mega-Nav & Forensic Stabilization (v1.41)

This plan addresses the UI layout inconsistencies (Mega-Nav vs. Sub-Nav) and the "Greenlet" backend stalls indicated by the keepalive logs.

---

## User Review Required
**IMPORTANT**
- **Mega-Nav Transformation:** I will merge the "Main" and "Secondary" navigation buttons into a single persistent header row as shown in your "Ziel-Bild". This will slightly decrease the available space for the dict logo but provides immediate access to all systems.

**CAUTION**
- **Gevent Patching:** I will enforce gevent-friendly sleep in the main loop. If you have custom backend scripts that use `time.sleep`, they must be updated to use `gevent.sleep` or `eel.sleep` to prevent UI freezing.

---

## Proposed Changes

### UI Architecture Rework (The "Mega-Nav")
- **[MODIFY] app.html**
  - Move all category buttons ("Browser", "Edit", "Options", etc.) into the `#header-nav-buttons` container.
  - Update the layout of `#sub-nav-container` to strictly represent contextual sub-tabs (Queue, Playlist, Visualizer).
- **[MODIFY] ui_nav_helpers.js**
  - Update `switchMainCategory` to correctly handle the selection state across the expanded header.
  - Refine `updateGlobalSubNav` to ensure it only populates relative contextual pills, preventing the "duplicate systems" issue in the screenshots.

### Backend Stability (Greenlet Fix)
- **[MODIFY] main.py**
  - Replace blocking `time.sleep(1.0)` in the keepalive loop with `eel.sleep(1.0)`.
  - Ensure `gevent.monkey.patch_all()` is called at the absolute earliest entry point.

### Diagnostic Integration
- **[NEW] gui_diagnostics.js**
  - Implement a floating, scrollable logging overlay that pulls from `eel.get_ui_logs()`.
  - Bind this overlay to the "LOGS" footer button.
- **[NEW] dom_hud.js**
  - A tiny real-time monitor showing DOM element count and layout stability in the footer.

---

## Open Questions
- In the "Ziel-Bild", the "STATUS" button is green. Should this button also act as a trigger for the new Logging Overlay, or should it remain tied to the technical HUD?
- Do you want the "Mega-Nav" to be scrollable if the window is too small, or should it wrap?

---

## Verification Plan

### Automated Checks
- Check logs for the absence of `[MainLoop] keepalive recovered` warnings.
- Verify `svg_icons.html` path resolution.

### Manual Verification
- Open App: Verify Mega-Nav shows all systems.
- Click "Player": Sub-nav should ONLY show Queue/Playlist/Visualizer.
- Click "LOGS": Verify the new logging overlay appears and populates in real-time.

---

**Analysis (Soll vs. Ist):**
- **Mega-Nav im Header:** Das „Ziel-Bild“ zeigt, dass du alle Systeme (Browser, Edit, Optionen, Parser, etc.) direkt oben im Header neben den Hauptkategorien haben möchtest. Aktuell sind diese bei mir noch getrennt oder fälschlicherweise in der zweiten Zeile (Sub-Nav).
- **Kontextuelle Sub-Nav:** In der zweiten Zeile sollen dann nur noch die echten Unter-Tabs stehen (z. B. Queue, Playlist, Visualizer für den Player).
- **Greenlet/Backend-Stall:** Die Striche in deiner Fußzeile [DB: -- | GUI: --] bestätigen, dass die Kommunikation zum Backend hängt. Ich habe in der main.py eine blockierende time.sleep()-Funktion gefunden, die den Gevent-Event-Loop anhält – das ist die Ursache für die „Greenlet“-Fehler.

---

I will proceed with the Mega-Nav layout overhaul and Greenlet stabilization as outlined above. Please confirm your preference for the STATUS button and Mega-Nav scroll/wrap behavior before final implementation.
