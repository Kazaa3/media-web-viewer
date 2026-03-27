
import re

def trace_divs(filepath, start_line, end_line):
    with open(filepath, 'r') as f:
        content = f.read()
    
    level = 0
    lines = content.splitlines()
    for i, line in enumerate(lines):
        line_num = i + 1
        # Remove comments
        clean_line = re.sub(r'<!--.*?-->', '', line)
        
        opens = len(re.findall(r'<div[\s>]', clean_line, re.IGNORECASE))
        closes = len(re.findall(r'</div>', clean_line, re.IGNORECASE))
        
        old_level = level
        level += opens
        level -= closes
        
        if line_num >= start_line and line_num <= end_line:
            print(f"L{line_num} | LVL: {level} | O:{opens} C:{closes} | {line[:80]}")

trace_divs('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 3300, 3400)
