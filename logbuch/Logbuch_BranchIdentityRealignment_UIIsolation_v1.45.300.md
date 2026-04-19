# Branch Identity Realignment & UI/Data Isolation (v1.45.300)

## Zielsetzung
Die technische Branch-Logik wird von den UI-Kategorien entkoppelt. Branches steuern nur noch, welche Medientypen sichtbar sind – die UI-Struktur (Tabs, Workstation) bleibt immer gleich.

---

## Highlights der Umsetzung (v1.45.300)

### Branch Renaming & Registry Cleanup
- In `config_master.py` wurden die Branch-IDs umbenannt:
    - `media` → `audio`
    - `library` → `multimedia`
    - `database` → `extended`
- Die `branch_architecture_registry` mappt jetzt:
    - `audio`: audio_native, audio_transcode
    - `multimedia`: audio_* + video_native/hd/pal
    - `extended`: all (Audio, Video, ISO, Bilder, Epub)
- Die `branch_identity_registry` enthält neue, sprechende Labels (z.B. "Build: Audio Only").

### Identity Restoration in Models
- Die `BRANCH_MAP` in `models.py` spiegelt die neuen technischen IDs wider.
- `get_branch_label` liefert die neuen Build-Level-Namen korrekt aufgelöst.

### Filtering & Exposure
- `main.py`: `get_branch_identity` nutzt die neuen Branch-IDs als Default.

### UI: Navigation Helpers
- `ui_nav_helpers.js`: Die Kategorien media, library, database triggern immer das Workstation-Layout – unabhängig vom aktiven Branch.
- Die Branches beeinflussen NICHT mehr die Tabs oder Sub-Tabs.

---

## Entscheidungsnotiz
- Die Namen `audio`, `multimedia`, `extended` sind als Build-Branches gesetzt. Alternativen wie MWV-Light/Pro/Full sind möglich, aber aktuell nicht umgesetzt.

---

## Verifikationsplan
- **Automatisierte Tests:**
    - Branch Filtering Test: Der audio-Branch filtert Video-Items korrekt aus.
    - Identity Resolution: `get_branch_label('audio')` liefert den richtigen Build-Namen.
- **Manuelle Prüfung:**
    - Kategorienwechsel in der UI aktiviert immer das Workstation-Layout, auch wenn der Branch auf Audio limitiert ist.

---

**Status:**
- Architektur ist jetzt klar getrennt: Branches steuern nur die Mediensichtbarkeit, die UI bleibt konsistent.
