# Align GUI Categories and Branch-Specific Filtering (v1.45.350)

## Zielsetzung
Die Top-Level-GUI-Kategorien (AUDIO, MULTIMEDIA, EXTENDED) werden inhaltlich und technisch mit der branch_architecture_registry und der Backend-Filterlogik synchronisiert. Die Labels und die tatsächliche Item-Filterung sind damit konsistent und nachvollziehbar.

---

## Content-Gruppierung (Soll-Zustand)
- **AUDIO:** Nur Audio-Items
- **MULTIMEDIA:** Audio + Video + Bilder
- **EXTENDED:** Audio + Video + Bilder + Ebooks (+ ISO)

---

## Änderungen & Komponenten

**[Component] CONFIGURATION RE-ALIGNMENT**
- `config_master.py`:
    - branch_architecture_registry aktualisiert: multimedia enthält jetzt auch bilder, extended enthält video_iso und epub.
    - navigation_orchestrator Level 1 Labels werden auf professionelle, inhaltlich korrekte Namen geprüft und ggf. angepasst.

**[Component] BACKEND FILTERING LOGIC**
- `models.py`:
    - Funktionsnamen vereinheitlicht: get_allowed_categories/get_allowed_internal_cats.
    - get_allowed_internal_cats mappt Aliase korrekt für branch enforcement.
- `main.py`:
    - _apply_library_filters prüft explizit auf bilder (images) und epub (ebooks) in supported_by_branch.
    - Sicherstellung, dass Items nur dann erscheinen, wenn sie zur Capability Stage des Branches passen.

---

## Entscheidungsnotiz
- Die Level 1 Labels können auf Wunsch um Deskriptoren wie "MULTIMEDIA (+IMG)" oder "EXTENDED (+ISO/EBOOKS)" erweitert werden.
- EXTENDED kann entweder wirklich ALLES enthalten (inkl. 'all') oder gezielt um weitere Formate ergänzt werden.

---

## Verifikationsplan
- **Automatisierte Tests:**
    - get_library mit verschiedenen active_branch-Parametern aufrufen und Item-Typen prüfen.
    - main.py-Logs auf "branch mismatch" prüfen.
- **Manuelle Prüfung:**
    - App starten, zwischen AUDIO, MULTIMEDIA, EXTENDED wechseln.
    - Sidebar-Dropdown zeigt die korrekten Capability-IDs.
    - Items erscheinen/verschwinden branch-spezifisch.

---

**Status:**
- Architektur und GUI sind jetzt konsistent und branch-aware. Labels und Filterung sind synchronisiert.
