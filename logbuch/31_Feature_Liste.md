<!-- Category: Planung -->

Task: Fix Missing Items in GUI
 Investigate why media items are not showing in the GUI
 Inspect 
main.py
 for Eel exposure and data fetching
 Inspect web/ directory for frontend loading logic
 Check if 
media_library.db
 has data
 Fix the display issue
 Correct Chapter Sorting (Natural sorting: 1, 2, 10 instead of 1, 10, 2)
 Fix Chapter Sorting in all Parsers (FFmpeg, Mutagen, MediaInfo)
 Consolidate Sorting in 
media_parser.py
 (Primary: Time, Secondary: Natural Title)
 Verify Chapter Sorting in Sidebar UI with "Power Hour", "Geben und Nehmen"
 Accurate Hörbuch Categorization (.m4b always Hörbuch, folder detection)
 Restore Sidebar Metadata (Codec, Container, Tag Format)
 Implement Dynamic Test Suite in GUI (List all tests/*.py)
 Backend discovery and execution
 Frontend dynamic tab update
 Implement Feature Status Window (Consolidated dashboard in GUI)
 Extended Media Types (Audio, Video, Document, Ebook, Series, Film)
 Add mandatory Unit Tests for GUI components
 Verify the fix and new features
 'Tests' Tab implementieren (Backend + Frontend)
 Checkboxen für Test-Suiten (DB, MediaItem, Parser)
 Backend eel.run_tests für Pytest-Ausführung
 Anzeige der Ergebnisse im GUI
 Fix: Backend-Crash bei Testausführung (Refactoring MediaItem to 
models.py
)
 Kapitel-Tests (Reihenfolgen-Check) implementiert
 Verifizierung der Testausführung im GUI
 Projekt-Dokumentation (README.md) aktualisieren
