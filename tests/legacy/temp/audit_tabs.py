import re
from pathlib import Path

def check_div_balance(html_content, start_marker, end_marker=None):
    # Find the section between start_marker and either end_marker or the next major tab comment
    start_idx = html_content.find(start_marker)
    if start_idx == -1:
        return f"Marker {start_marker} not found"
    
    if end_marker:
        end_idx = html_content.find(end_marker, start_idx)
    else:
        # Look for the next <!-- ===================== ... TAB START ... ===================== -->
        next_tab_match = re.search(r"<!-- ===================== .* TAB START ===================== -->", html_content[start_idx + len(start_marker):])
        if next_tab_match:
            end_idx = start_idx + len(start_marker) + next_tab_match.start()
        else:
            end_idx = len(html_content)
            
    section = html_content[start_idx:end_idx]
    opens = len(re.findall(r"<div", section))
    closes = len(re.findall(r"</div", section))
    return opens, closes, opens - closes

html_path = Path("web/app.html")
content = html_path.read_text()

tabs = [
    ('Video Player', 'multiplexed-media-player-orchestrator-panel'),
    ('Library', 'coverflow-library-view'),
    ('Item', 'indexed-sqlite-repository-tab'),
    ('File', 'filesystem-crawler-tab'),
    ('Edit', 'crud-metadata-tab'),
    ('Options', 'system-configuration-persistence-panel'),
    ('Parser', 'regex-provider-chain-orchestrator-panel'),
    ('Debug', 'debug-flag-persistence-panel'),
    ('Tests', 'qa-validation-traceability-test-suite-panel'),
    ('Reporting', 'executive-analytical-reporting-dashboard-panel'),
    ('Logbuch', 'localized-markdown-documentation-journal-panel')
]

for name, div_id in tabs:
    marker = f'id="{div_id}"'
    result = check_div_balance(content, marker)
    if isinstance(result, str):
        print(f"{name:15}: {result}")
    else:
        opens, closes, balance = result
        status = "OK" if balance == 0 else "!!! BROKEN !!!"
        print(f"{name:15}: Opens={opens:3}, Closes={closes:3}, Balance={balance:3} -> {status}")
