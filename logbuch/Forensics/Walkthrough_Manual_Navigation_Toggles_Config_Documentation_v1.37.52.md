# Walkthrough - Manual Navigation Toggles & Config Documentation (v1.37.52)

## Zusammenfassung
Die Navigationselemente wurden vervollständigt und die gewünschten Erklärungen in die Konfiguration eingebaut. Die Steuerung der oberen Leisten ist jetzt vollständig und flexibel.

---

## 1. Neue Manuelle Toggle-Buttons (Header)
- In der oberen Leiste (neben dem Sidebar-Button) wurden zwei neue Steuerelemente hinzugefügt:
  - **Zen-Mode Toggle (Blaues Icon):** Blendet die gesamte Haupt-Navigationsleiste (Header) aus. Der Content rutscht sofort nach oben (Offset = 0).
  - **Sub-Nav Toggle (Oranges Icon):** Blendet die kontextuelle Pill-Leiste (Warteschlange/Lyrics) aus/ein und passt den Offset entsprechend an.
- Damit kann der vertikale Platz jederzeit manuell maximiert werden – ohne Änderung der Config.

---

## 2. Kommentare in der Navigation Registry
- In `src/core/config_master.py` wurden die Flags der `ui_visibility_matrix` dokumentiert:

```python
# --- UI VISIBILITY MATRIX (v1.37.52 Restoration) ---
# Controls which bars are rendered per category to prevent menu-clutter.
# master_header:        Haupt-Navigationsleiste oben (Kategorien/Fenster-Switch).
# contextual_pill_nav:  Kontext-Untermenüs (Pills für Queue, Playlist, Lyrics).
# module_tab_nav:       Interne Listen-Steuerung (z.B. Raster vs. Liste in Library).
```

---

## 3. Synchronisation
- **Media/Player:** Der Header ist in der Config wieder auf `True` gesetzt und beim ersten Start sichtbar, kann aber über den neuen "Zen"-Button jederzeit ausgeblendet werden.
- **Geometry Engine:** Die JS-Logik reagiert sofort auf die Toggle-Buttons und berechnet den Pixel-Offset (0, 32, 40 oder 72px) dynamisch neu.

---

Bitte Anwendung neu laden. Sie haben jetzt volle Kontrolle über die oberen Leisten und deren Platzverbrauch.