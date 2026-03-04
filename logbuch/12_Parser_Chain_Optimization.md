<!-- Category: Parser -->

Parser Chain Optimization and UI Configuration
Goal Description
The user wants to optimize the entire media parsing chain by making the execution order of the parsers freely configurable directly from the "Optionen" (Options) tab in the UI.

The available parsers that should be sortable/toggleable are:

mutagen (Native Python metadata extractor)
pymediainfo (Fast C-binding wrapper for MediaInfo)
ffmpeg (Subprocess FFmpeg fallback)
container (Fallback if format logic needed based on container/extension)
filename (Fallback to grab basic info from the filename)
Proposed Changes
parsers/format_utils.py
[MODIFY] Update PARSER_CONFIG
Replace the simple "enable_ffmpeg": False with a full list defining the execution order: "parser_chain": ["filename", "mutagen", "pymediainfo"]
Add a function to load/save this configuration to a consistent config file (e.g., config.json) so user choices persist across restarts.
parsers/media_parser.py
[MODIFY] Dynamic Execution Chain
Refactor 
extract_metadata
 to iterate over PARSER_CONFIG["parser_chain"] instead of using the hardcoded if/else fallbacks.
Each internal parser (filename_parser, mutagen_parser, etc.) should be called dynamically based on the current string in the sequence.
The final 16 Bit (lossy) fallback remains at the very end of the dynamic chain.
main.py
[MODIFY] Expose Configuration API
Add new Eel exposed functions: get_parser_config() and save_parser_config(new_chain).
These functions will interface with 
format_utils.py
 to read/write the config.
web/app.html
[MODIFY] Options UI
In the Left Column ("Allgemein & Debug"), replace or augment the "Debug-Flags" section with a "Parser Reihenfolge" (Parser Order) UI.
Create a draggable list (or a simple list with Up/Down buttons + Checkboxes) representing the 5 parsers: Mutagen, Pymediainfo, FFmpeg, Container, Dateiname.
Call eel.save_parser_config when the order is changed.
Verification Plan
Open the Options tab and verify the new Parser Configuration UI exists.
Change the order (e.g., put ffmpeg first) and save.
Rescan a file and verify the logs show the parsers executing in the new order.
Verify the configuration persists (i.e., is read from config.json).
v
