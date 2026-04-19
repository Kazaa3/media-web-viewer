# Walkthrough – Emergency Relocation of GUI Recovery Tools (v1.41.141-FIX)

## Zusammenfassung
Die Notfall-Tools zur GUI-Wiederherstellung wurden erfolgreich in die sichtbare UI-Ebene verlegt. Der [FLASH]-Button und das Life-Sign-Overlay sind jetzt immer zugänglich, selbst wenn die Hauptnavigation oder Fragmente ausfallen.

---

## 1. Sichtbarer [FLASH] Button
- **Position:**
  - Der [FLASH]-Button befindet sich jetzt direkt neben dem "dict"-Logo ganz links im Header.
  - Er bleibt sichtbar, unabhängig davon, ob die technischen HUD- oder Navigations-Cluster geladen sind.

## 2. Forcierte Sichtbarkeit der Secondary Cluster
- **Emergency Style:**
  - Ein `<style>`-Block erzwingt, dass die rechtsbündigen Secondary Cluster (Diagnostik, Sidebar-Toggles) immer sichtbar bleiben (`opacity: 1 !important; visibility: visible !important; width: auto !important;`).

## 3. Life-Sign Elevation
- **emergency-life-sign:**
  - Das Life-Sign-Overlay ist jetzt ein direktes Kind von `<body>`, sodass es auch bei Ausfall des Headers angezeigt werden kann.

---

## Recovery-Anleitung
1. **Button finden:**
   - Suche den pulsierten roten [FLASH]-Button neben dem "dict"-Logo oben links.
2. **[FLASH] klicken:**
   - Der Klick triggert das `forceLife()`-Skript:
     - Entfernt alle Blackout-Klassen von der Seite.
     - Zeigt das "Life Detected"-Recovery-Panel im Viewport an.
     - Reaktiviert alle Navigations-Buttons.

---

**Hinweis:**
Wenn der [FLASH]-Button nicht erscheint oder nicht reagiert, liegt ein kritischer Browser- oder Script-Blocker-Fehler vor. In diesem Fall bitte die Browser-Konsole auf fatale Fehler prüfen.

---

**Die Notfall-Tools sind jetzt forensisch und funktional immer erreichbar.**
