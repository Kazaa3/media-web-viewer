import re

content = open('/home/xc/#Coding/gui_media_web_viewer/web/app.html').read()

views = [
    ('options-general-view', 'options-tools-view'),
    ('options-tools-view', 'options-environment-view'),
    ('options-environment-view', 'id="regex-provider-chain-orchestrator-panel"')
]

for start_marker, end_marker in views:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    slice = content[start_idx:end_idx]
    opens = len(re.findall(r'<div', slice))
    closes = len(re.findall(r'</div>', slice))
    print(f"View: {start_marker} -> Opens: {opens}, Closes: {closes}, Diff: {opens - closes}")
