<!-- Category: Parser -->

Parser Settings Tab
We have successfully implemented the new Parser tab in the graphical interface, allowing users to configure how metadata extraction operates in real-time.

Changes Made
New Tab Layout (
web/app.html
):

Added a dedicated "Parser" button next to "Optionen" in the top navigation bar.
Created the <div id="parser-tab"> area to house the parser-specific settings.
Parser Architecture Re-homing:

Moved the existing drag-and-drop parser priority list from the "Optionen" tab into the new "Parser" tab.
This provides a cleaner separation of concerns where technical debug flags live in "Optionen" while metadata scanning methodology lives in "Parser".
"Full Mode" Integration:

Added a new toggle switch explicitly for Erweiterter Parser-Modus (Full Mode) in the Parser tab.
When the DOM saves the parser configuration via JavaScript (
saveParserChainUI
), it now fetches the checked state of that toggle and serializes it as parser_mode: "full" | "lightweight".
Settings Synchronization (Python Backend):

Modified 
load_parser_config()
 to pass the parser_mode flag string back to the GUI upon load.
Modified PARSER_CONFIG inside 
parsers/format_utils.py
 to natively track {"parser_mode": "lightweight"} as a configurable setting defaulting to lightweight.
Modified 
main.py
 where new 
MediaItem
 instances are generated. The initialization now looks up parser_mode directly from PARSER_CONFIG and passes it synchronously to the media_parser.extract_metadata execution.
Validation Results
Scanning new files now respects the toggle switch set by the user in the Parser tab. Leaving it off results in the needs_more_info optimizations kicking in for fast indexing, and turning it on safely evaluates all files sequentially and populates their internal JSON structure with full_tags. The UI handles configuring and saving both the chain order and the toggle simultaneously via the





 Parser Settings Tab
The user wants a new tab specifically dedicated to configuring the Parser. This tab ("Parser") should allow the user to see and adjust parser flags, which in our current architecture correlates to the mode parameter (lightweight vs. full) and the order/enablement of the parser chain itself, currently living under the "Optionen" tab.

User Review Required
Does the user want me to move the existing parser configuration (chain order, activation) from the "Optionen" tab into the new "Parser" tab, along with the new mode toggle flag?

Proposed Changes
Configuration and Orchestration
[MODIFY] 
app.html
Navigation: Add a new <button> for the Parser tab in .tab-buttons (e.g., <button class="tab-btn" onclick="switchTab('parser', this)">Parser</button>).
Tab Content: Add a new <div id="parser-tab" class="tab-content"> area.
Migration: Move the "Parser-Architektur" section (the drag & drop list of parsers) from the options-tab into the new parser-tab.
New Toggle: Add a new toggle switch in the parser-tab for "Erweiterter Parser-Modus" (dictating lightweight vs. full mode).
This toggle will trigger an Eel callback to save the global parser_mode configuration.
JavaScript Configuration: Ensure the 
saveParserChainUI
 and a new saveParserModeUI correctly sync with the Python backend.
[MODIFY] 
format_utils.py
Expand PARSER_CONFIG dictionary to manage an external parser_mode variable (defaulting to "lightweight").
Example: {"parser_chain": [...], "parser_mode": "lightweight"}
Ensure 
load_parser_config()
 and 
save_parser_config()
 read/write this new key properly to parser_config.json.
[MODIFY] 
main.py
Global Settings: Ensure that 
MediaItem
 initialization dynamically looks up PARSER_CONFIG.get("parser_mode", "lightweight") and passes it down into media_parser.extract_metadata(..., mode=mode).
Update config routes so that Eel can correctly serialize and update the mode.
Verification Plan
Automated Tests
N/A
Manual Verification
Run application and click the "Parser" tab.
Verify the parser list (drag/drop) works and saves successfully in its new home.
Toggle the "Erweiterten Modus" (Full mode) switch to true. Read the logs/network/DB to ensure it saves.
Scan media and select a file, confirming that full_tags is evaluated based on the state of that switch. "Konfiguration Speichern" button.
