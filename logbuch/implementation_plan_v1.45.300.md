# Implementation Plan: Branch Identity Realignment & UI/Data Isolation (v1.45.300)

## Zielsetzung
Die Branches steuern ausschließlich, welche Medientypen (Audio, Video, Bilder, Epubs, ISO) im Player und in der Item-Liste erscheinen. Die UI-Struktur (Tabs, Unterreiter, Workstation-Layout) bleibt davon vollständig unberührt und ist immer verfügbar, wenn die Kategorie gewählt wird.

---

## Korrektur der Branch-IDs
- Die technischen Branch-IDs werden umbenannt, um ihre Funktion (Content-Support) klar zu machen:
    - `audio` (nur Audio-Support)
    - `multimedia` (Audio + Video + Bilder)
    - `extended` (Alles inkl. ISO, Epubs)
- Die alten IDs wie `media`, `library`, `database` werden nicht mehr verwendet.

---

## Architektur-Änderungen

**[Component] CONFIG: BRANCH REGISTRY CLEANUP**
- `config_master.py`: Die `branch_architecture_registry` verwendet jetzt die neuen IDs (`audio`, `multimedia`, `extended`) und mappt sie auf die jeweiligen Medientypen.
- Die `branch_identity_registry` enthält sprechende Labels wie "Build: Audio Only".

**[Component] MODELS: IDENTITY RESTORATION**
- `models.py`: Die `BRANCH_MAP` spiegelt die neuen technischen IDs wider.
- `get_branch_label` löst die neuen Build-Level-Namen korrekt auf.

**[Component] CORE: FILTERING & EXPOSURE**
- `main.py`: `get_branch_identity` nutzt die neuen Branch-IDs als Default.

**[Component] UI: NAV HELPERS**
- `ui_nav_helpers.js`: Die Kategorien (Tabs) wie AUDIO, MULTIMEDIA, EXTENDED triggern immer das Workstation-Layout – unabhängig vom aktiven Branch.
- Die Branches beeinflussen NICHT mehr Tabs oder Unterreiter.

---

## Entscheidungsnotiz
- Die Namen `audio`, `multimedia`, `extended` sind für die Build-Branches gesetzt. Alternativen wie MWV-Light/Pro/Full sind möglich, aber aktuell nicht vorgesehen.

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
- Warten auf Freigabe der Branch-Bereinigung.
