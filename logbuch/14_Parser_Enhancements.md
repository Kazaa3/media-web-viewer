<!-- Category: Parser -->

Parser Enhancements
 Update 
format_utils.py
 to reorder the parser chain: ["filename", "container", "mutagen", "pymediainfo", "ffmpeg"]
 Implement lightweight and full modes in 
media_parser.py
Pass mode parameter to all parsers.
In full mode, ensure all parsers run (skip the needs_more_info check limitation).
 Add mode support to 
filename_parser.py
Implement regex to extract track number if filename starts with digits (e.g., "02 Title" -> Track 2).
 Create new 
container_parser.py
Parse MKV streams (since MKV doesn't use standard ID3 tags).
Extract metadata from nested AAC streams.
 Enhance 
mutagen_parser.py
Add signature to accept mode.
In full mode, extract all raw tags into tags['full_tags'].
Implement chapter parsing.
 Enhance 
pymediainfo_parser.py
Add signature to accept mode.
In full mode, extract all raw track attributes into tags['full_tags'].
Implement chapter parsing.
 Update 
ffmpeg_parser.py
Add signature to accept mode.
Gather all raw output if in full mode.
Parser Settings Tab
 Modify 
web/app.html
Add "Parser" tab button.
Create "Parser" tab content area.
Move parser chain drag/drop UI from "Optionen" to "Parser" tab.
Add toggle switch for "Erweiterter Parser-Modus" (lightweight/full).
Add logic to load/save parser_mode flag.
 Modify 
parsers/format_utils.py
Support parser_mode in configuration saving/loading.
 Modify 
main.py
Ensure 
MediaItem
 instantiation pulls the parser_mode from the config.
Fix bug where eel.start() exited prematurely, causing the frontend UI (toggles/parser list) to fail loading data.
