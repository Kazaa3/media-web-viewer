import re
from pathlib import Path

def check_div_balance(html_content, start_marker):
    start_idx = html_content.find(start_marker)
    if start_idx == -1:
        return f"Marker {start_marker} not found"
    
    # Look for the start of the next tab section or the end of the file
    # Major tab sections start with <!-- TAB: ... START --> or <!-- ===================== ... TAB START ===================== -->
    patterns = [
        r"<!-- TAB: .* START -->",
        r"<!-- ===================== .* TAB START ===================== -->",
        r"<!-- TAB: .* END -->",
        r"<!-- ===================== .* TAB END ===================== -->"
    ]
    
    potential_ends = []
    for pattern in patterns:
        matches = re.finditer(pattern, html_content[start_idx + 1:])
        for match in matches:
            potential_ends.append(start_idx + 1 + match.start())
            break # Just need the first one after the start
            
    if potential_ends:
        end_idx = min(potential_ends)
    else:
        end_idx = len(html_content)
        
    section = html_content[start_idx:end_idx]
    
    # To be more accurate, we should avoid counting divs inside fixed code blocks or similar
    # But for a quick audit, simple count is usually enough to spot imbalances
    opens = len(re.findall(r"<div", section))
    closes = len(re.findall(r"</div", section))
    return opens, closes, opens - closes

html_path = Path("web/app.html")
content = html_path.read_text()

tabs = [
    ('Player', 'state-orchestrated-active-queue-list-container'),
    ('Library', 'coverflow-library-panel'),
    ('Item', 'indexed-sqlite-media-repository-panel'),
    ('File', 'filesystem-crawler-directory-panel'),
    ('Edit', 'metadata-writer-crud-panel'),
    ('Playlist', 'json-serialized-sequence-buffer-panel'),
    ('VLC/Video', 'multiplexed-media-player-orchestrator-panel'),
    ('Options', 'system-configuration-persistence-panel'),
    ('Parser', 'regex-provider-chain-orchestrator-panel'),
    ('Debug', 'debug-flag-persistence-panel'),
    ('Tests', 'quality-assurance-regression-suite-panel'),
    ('Reporting', 'reporting-dashboard-panel'),
    ('Logbuch', 'localized-markdown-documentation-journal-panel')
]

print(f"{'Tab Name':15} | {'Opens':5} | {'Closes':6} | {'Balance':7} | {'Status'}")
print("-" * 60)
for name, div_id in tabs:
    marker = f'id="{div_id}"'
    result = check_div_balance(content, marker)
    if isinstance(result, str):
        print(f"{name:15} | {result}")
    else:
        opens, closes, balance = result
        status = "OK" if balance == 0 else "!!! BROKEN !!!"
        if balance > 0:
            status = "!!! BROKEN (UNCLOSED) !!!"
        elif balance < 0:
            status = "!!! BROKEN (EXTRA CLOSE) !!!"
            
        print(f"{name:15} | {opens:5} | {closes:6} | {balance:7} | {status}")
