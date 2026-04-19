# Implementation Plan – Context Menu Centralization & Final Visibility Fix (v1.41.148)

## Ziel
Beseitigung des "Top-Left Ghost"-Kontextmenü-Bugs durch vollständige Zentralisierung der Logik, HTML-Deduplication und strikte Sichtbarkeitsregeln.

---

## 1. CSS STANDARDIZATION
- **[MODIFY] main.css**
  - Class Enforcement: `.context-menu` erhält als Basiszustand `display: none !important;`.
  - Style Cleanup: Die "Premium"-Glassmorphismus-Styles werden aus dem Fragment in die externe CSS-Datei ausgelagert.

## 2. HTML DEDUPLICATION
- **[MODIFY] app.html**
  - Placeholder Purge: Alle doppelten `#context-menu-placeholder`-Divs entfernen. Nur ein Platzhalter bleibt am Ende von `<body>`.
- **[MODIFY] context_menu.html**
  - Inline Style Removal: Alle `style`-Attribute vom Root-Div entfernen.
  - Strict ID/Class: Setze `id="context-menu"` und `class="context-menu"`.

## 3. JAVASCRIPT LOGIC CONSOLIDATION
- **[MODIFY] common_helpers.js**
  - Target Consolidation: `showContextMenu` zielt exakt auf `id="context-menu"`.
  - Visibility Toggle: Nutze `.style.setProperty('display', 'block', 'important')` für Sichtbarkeit nur beim Event.
- **[MODIFY] ui_nav_helpers.js**
  - Load Guard: Das Fragment wird nur in den einen, primären Placeholder geladen.

---

## 4. VLC/MPV Logic
- Die spezifische Logik bleibt zentralisiert, wie gewünscht.

---

## Verification Plan
- **Manual Verification:**
  - Initial Load: Viewport ist beim Start leer (kein Menü oben links).
  - Library Check: Rechtsklick auf Medienobjekt → Menü erscheint korrekt.
  - Global Check: Rechtsklick auf Hintergrund → kein Menü.

---

**Review erforderlich vor Umsetzung!**
