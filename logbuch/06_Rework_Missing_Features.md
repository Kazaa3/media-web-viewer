<!-- Category: Planung -->

Rework & Missing Features Implementation Plan
This plan follows the TODOs placed in 
main.py
 by the user.

Proposed Changes
1. Test Tab Rework (
main.py
 & 
web/app.html
)
The user requested a detailed Test UI including Categories, Inputs, Outputs, Files, Pass-count, and Comments.

[MODIFY] 
main.py
Modify the 
get_test_suites()
 function. Instead of just returning filenames, it will return a detailed dictionary for each test suite (e.g., 
benchmark_parsers.py
, 
test_media_item_logic.py
, GUI Tests).
Each test suite will include the following predefined metadata:
category (Testkategorien)
inputs (Eingabewerte)
outputs (Ausgabewerte)
test_files (Testdateien)
comment (Kommentar)
Modify the 
run_tests()
 function to parse the detailed output from pytest and extract the number of passed/failed tests (Aufzählung der Passes) so it can be sent to the GUI.
[MODIFY] 
web/app.html
Redesign the 
tests
 tab UI from a simple list of checkboxes into a rich grid or list of cards.
Each test card will display its title along with badges for its Category.
It will list Inputs, Outputs, Target Files, and Comments.
The test output area will be updated to prominently display the number of passes, fails, and errors extracted from the pytest output, above the raw logs.
The GUI Tests checkbox will be integrated into this new card-based layout as well.
2. Python Datenanalyse & Scraping Stubs (
data/
 / scripts/)
The user added # pYTHON Datenanalyse and # Python Scraping. I will add placeholder scripts or folders to establish a structure for these features.

[NEW] scripts/data_analysis.py
A stub script for future Python data analysis features.
[NEW] scripts/web_scraper.py
A stub script for future Python scraping features.
3. Logbook Restore & Unchecked Tasks (
web/app.html
 & 
task.md
)
The comments # logbuch ist verloren gegangen. heir die .mds and # un abgehakte punkte wieder hinzufügen suggest restoring the content of the logbook or task lists.

[MODIFY] 
web/app.html
Under the "Features" popup, ensure all markdown files in the logbuch/ folder are properly listed and clickable.
Add remaining unchecked points to 
task.md
 or a dedicated UI section so they aren't lost.
Verification Plan
Automated Tests
Run npm run dev or python main.py to start the Eel server and ensure there are no syntax errors.
Run the actual pytest test suites via pytest tests/ to confirm the test execution and output parsing logic works.
Manual Verification
Start the application window and go to the "Tests" tab.
Verify that the tests are now displayed as rich cards with "Testkategorien", "Eingabewerte", "Ausgabewerte", "Testdateien", and "Kommentar".
Click "Ausgewählte Tests ausführen" and verify that the "Aufzählung der passes" successfully parses the pytest output to show how many tests passed.
Open the Features list and verify that Logbuch entries work and no tasks are lost.

Comment
Ctrl+Alt+M
