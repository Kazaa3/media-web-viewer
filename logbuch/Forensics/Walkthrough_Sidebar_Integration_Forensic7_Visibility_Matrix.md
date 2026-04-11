# Walkthrough - Sidebar Integration in Forensic 7 Visibility Matrix

## Zusammenfassung
Das linke Menü (Sidebar) ist jetzt als 7. Flag (`sidebar_visible`) fest in die globale Visibility-Matrix integriert. Die Steuerung ist pro Kategorie individuell und wird bei jedem Kategoriewechsel automatisch durchgesetzt.

---

## 1. Neuer Toggle-Flag: sidebar_visible
- In `config_master.py` steuert `sidebar_visible` für jede Kategorie, ob das linke Menü beim Wechsel automatisch ein- oder ausgeblendet wird:

```python
# 7. sidebar_visible: Sidebar beim Wechsel automatisch aus-/einblenden.
"ui_visibility_matrix": {
    "media": { ..., "sidebar_visible": False }, # Startet eingeklappt (Zen-Mode)
    "library": { ..., "sidebar_visible": True }, # Startet ausgeklappt
    ...
}
```

---

## 2. Automatische Steuerung
- Die Navigations-Logik in `ui_nav_helpers.js` erzwingt diesen Zustand bei jedem Kategoriewechsel:
  - **Player/Media:** Sidebar klappt automatisch ein (maximaler Platz für Content).
  - **Bibliothek:** Sidebar klappt automatisch aus (leichtere Navigation).
- Die manuelle Steuerung über den Footer-Button bleibt möglich, wird aber beim nächsten harten Kategoriewechsel durch die Matrix überschrieben.

---

## 3. Syntax-Fix
- Ein Syntaxfehler in der Python-Config (doppelte Klammer) wurde behoben. Die Anwendung bootet jetzt wieder fehlerfrei.

---

## 4. Alle Flags im Überblick (Forensic 7 Matrix)
Die Flags sind weiterhin vorhanden und präzise dokumentiert:

```python
# --- UI VISIBILITY MATRIX (v1.37.52 Hardening) ---
# 1. master_header:        Haupt-Navigationsleiste oben.
# 2. contextual_pill_nav:  Untermenüs (Pills wie Queue, Playlist).
# 3. module_tab_nav:       Interne Modul-Tabs.
# 4. footer_visible:       Schwebende Media-Leiste unten.
# 5. sidebar_allowed:      Erlaubt die Sidebar für diese Kategorie.
# 6. diagnostics_hud_allowed: Erlaubt den Tech-HUD.
# 7. sidebar_visible:      Sidebar beim Wechsel automatisch aus-/einblenden.
```

Sie finden diese Definitionen in `src/core/config_master.py` ab Zeile 243.

---

## Hinweise
- Die Logik in `ui_nav_helpers.js` erzwingt diese Flags jetzt autoritativ. Wenn z.B. `module_tab_nav` für eine Kategorie auf `False` steht, wird dieser Bereich zuverlässig ausgeblendet.
- **Wunsch:** Soll ein Default-Wert für `contextual_pill_nav` oder `module_tab_nav` in einer bestimmten Kategorie angepasst werden? (z.B. in der Library wieder einschalten?)

---

Bitte testen Sie das Verhalten: Beim Tab-Wechsel sollte die Sidebar exakt wie in der Matrix hinterlegt reagieren.