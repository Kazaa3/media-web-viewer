# Fehlende i18n-Testbereiche und empfohlene Testdateien

## Identifizierte Lücken in der Testabdeckung

1. **Filter-Chips und Selects mit i18n (Library-Tab):**
   - Buttons mit `class="filter-chip"` und `data-i18n` (z.B. `filter_all`, `filter_audio`, `cat_album`, ...)
   - Select/Option mit `data-i18n` (z.B. `filter_sub_all`, `filter_audiobooks`, ...)

2. **Playlist-Tab:**
   - Buttons mit `data-i18n` (`pl_save`, `pl_load`, `pl_shuffle`, `pl_clear`, `pl_move_up`, `pl_move_down`)

3. **Edit-Tab:**
   - Input mit `data-i18n="[placeholder]edit_search_library_placeholder"`
   - Buttons mit `data-i18n` (`edit_btn_rename`)
   - Headings mit `data-i18n` (`edit_title`, `edit_subtitle`, `edit_form_title`)

4. **Kontextmenü (`custom-context-menu`, `context-menu-item`):**
   - Prüfen, ob `data-i18n` auf Menüeinträgen vorhanden ist (ggf. dynamisch)

5. **Toasts/Popups:**
   - `#toast-container`, `.toast` (ggf. dynamisch mit `data-i18n`)

6. **Tooltips:**
   - `title`-Attribute, ggf. `data-i18n` auf Buttons (z.B. `fb-refresh-btn`)

---

## Empfohlene nächste Testdateien

- `test_library_filters_i18n.py` (Filterchips, Selects)
- `test_playlist_buttons_i18n.py` (Playlist-Tab)
- `test_edit_tab_i18n.py` (Edit-Tab, Inputs, Buttons)
- `test_context_menu_i18n.py` (Kontextmenü, falls `data-i18n`)
- `test_toast_popup_i18n.py` (Toasts/Popups, falls `data-i18n`)
- `test_tooltips_i18n.py` (Buttons mit `title`/`data-i18n`)

---

**Empfehlung:**
Mit der Erstellung und Erweiterung dieser Testdateien kann die i18n-Abdeckung für alle relevanten UI-Elemente sichergestellt werden. Die Umsetzung erfolgt modular pro Bereich/Datei.
