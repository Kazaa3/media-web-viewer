# 🛠 Status & Repair Phase

Create scripts/gui_validator.py for depth trace and audit

Resolve structural corruption in app.html (escaped nested script tags)

Fix appendUiTrace ReferenceError and UI leakage

Synchronize App Naming ("dict" v1.34) across GUI

Develop Selenium-based GUI test suite (tests/gui_test.py)

Repair DIV/Brace imbalances and structural leakage

Identify premature closure in General Options (line 3277 - FIXED)

HTML Struktur-Reperatur & Stabilisierung (Left to Right)
#1 Player Tab (Audit & Fix)
#2 Library Tab (Audit & Fix)
#3 Item Tab (Audit & Fix)
#4 Datei Tab (Audit & Fix)
#5 Edit Tab (Audit & Fix)
#6 Options Tab (Audit & Fix)
Sub-tab 1: Allgemein
Sub-tab 2: Tools
Sub-tab 3: Architektur (Environment)
Persistent Navi (Fixed Header)
#7 Parser Tab (Audit & Fix)
#8 Debug Tab (Audit & Fix)
#9 Tests Tab (Audit & Fix)
#10 Reporting Tab (Audit & Fix)
Buttons statt Select (Navi)
#11 Logbuch Tab (Audit & Fix)
#12 Playlist Tab (Audit & Fix)
#13 Video Tab (Audit & Fix)
UI Refactoring (Unterreiter & Modale)

Options Sub-Navi vereinheitlichen
Reporting Sub-Navi (Buttons statt Select)
Architektur-View (Menu-Visibility fix)
Modale sauber trennen & kommentieren
i18n & Tab-Namens-Check

Modulare "Low Context" Selenium Tests

tests/gui/ Verzeichnis anlegen
test_tabs.py, test_subtabs.py, test_modals.py implementieren
Verifikation & Walkthrough

Fix gui_validator.py to handle multi-line tags and comments

Application State Verification

Verify Database Schema - insure new columns exist in media.db
Fix critical Pyre/IDE Lints in main.py and models.py
Run app and check for startup/ Eel connection errors

⚓ Anchors (Completed)
Database Evolution
Update db.py to support new columns (ISBN, IMDb, ParentID, etc.)
Update db.insert_media to return row ID for linking
Core Model Refactor
Implement Item/Object split in models.py (via media_type)
Add Remote ID extraction and Amazon cover support to MediaItem
Update to_dict for serialization of new fields
Scanning Logic
Implement two-pass scan_media in main.py for hierarchical grouping
Implement parent-child linking based on folder structure

📝 Open Points (To Do)
Categorization Upgrade
Expand subtypes in format_utils.py (Sammeltypen, Klassik, etc.)
ISBN Scanning API
Implement normalize_isbn and api_scan_isbn in main.py
Integrate metadata fetching from OpenLibrary in api_scan_isbn (Partly done)
Frontend Integration
Add "Scan ISBN" button and barcode scan handler in app.html
Update Media Cards to display Object vs Item relationship (Hierarchy)
Add support for Remote ID links (Amazon, IMDb) in Metadata view

🧪 Verification
Run scan_media and verify record types (file vs container)
Verify ISBN scan with a real ISBN code
Check DB for correct parent_id assignments


# UI-Status: Reporting, Video & Player Tab

### Reporting Tab
- Enthält 5 Sub-Tabs (Unterreiter) für verschiedene Auswertungen/Funktionen.
- Sub-Tabs müssen auf Konsistenz und Funktion geprüft werden.

### Video Tab
- Verwendet einen eigenen Player (unterscheidet sich von Player-Tab).
- Besitzt eine Sidebar (linke Seite) für Navigation oder Metadaten.
- Footer für Player-Steuerung fehlt komplett.
- Player-Integration und Layout prüfen/vereinheitlichen.

### Player Tab
- Sidebar auf der linken Seite (ähnlich wie Video-Tab).
- Rechts daneben eine Item-Liste (z.B. Songs, Medienobjekte).
- Player-Footer (Steuerung, Fortschrittsbalken etc.) fehlt vollständig.
- UI-Elemente und Player-Logik auf Vollständigkeit und Konsistenz prüfen.

---

**ToDo:**
- Reporting-Sub-Tabs testen und ggf. refaktorieren.
- Video- und Player-Tab: Sidebar, Item-Liste und Footer-Elemente ergänzen/vereinheitlichen.
- Unterschiedliche Player-Implementierungen dokumentieren und ggf. harmonisieren.
