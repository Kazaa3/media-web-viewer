import os
import re

app_path = "/home/xc/#Coding/gui_media_web_viewer/web/app.html"
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

open_divs = len(re.findall(r'<div\b', content))
close_divs = len(re.findall(r'</div\b', content))
print(f"Total Divs: {open_divs} / {close_divs}")

layout_start = content.find('id="main-split-container"')
footer_start = content.find('class="player-container"')

if layout_start == -1 or footer_start == -1:
    print(f"Indices: layout={layout_start}, footer={footer_start}")
else:
    layout_chunk = content[layout_start:footer_start]
    open_chunk = len(re.findall(r'<div\b', layout_chunk))
    close_chunk = len(re.findall(r'</div\b', layout_chunk))
    print(f"Layout Chunk Divs (Open/Close): {open_chunk} / {close_chunk}")

# Check tabs
tab_calls = re.findall(r"switchTab\(['\"]([^'\"]+)['\"]", content)
unique_tabs = set(tab_calls)
for tab_id in unique_tabs:
    if tab_id == "${tabId}": continue
    exists = f'id="{tab_id}"' in content
    print(f"Tab '{tab_id}' exists: {exists}")
