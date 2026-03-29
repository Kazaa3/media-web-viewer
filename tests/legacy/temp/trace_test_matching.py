
import re

with open('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
lvl = 0
for i, line in enumerate(lines, 1):
    # Remove script tags and comments for cleaner trace if needed, 
    # but the test script DOES NOT remove them! So I shouldn't either.
    opens = len(re.findall(r'<div\b', line, re.IGNORECASE))
    closes = len(re.findall(r'</div\b', line, re.IGNORECASE))
    lvl += (opens - closes)
    if lvl < 0:
        print(f"L{i} | LVL: {lvl} | O:{opens} C:{closes} | {line[:50]}")
        # Stop after first negative to find first leak
        break

print(f"Final level with test regex: {lvl}")
