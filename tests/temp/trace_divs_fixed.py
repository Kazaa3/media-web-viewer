
import re

def trace_divs_fixed(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    level = 0
    lines = content.splitlines()
    output = []
    for i, line in enumerate(lines):
        line_num = i + 1
        # Remove comments
        clean_line = re.sub(r'<!--.*?-->', '', line)
        
        opens = len(re.findall(r'<div\b', clean_line, re.IGNORECASE))
        closes = len(re.findall(r'</div>', clean_line, re.IGNORECASE))
        
        level += opens
        level -= closes
        
        output.append(f"L{line_num} | LVL: {level} | O:{opens} C:{closes} | {line[:80]}")
    
    with open('/tmp/trace_divs_fixed.txt', 'w') as f:
        f.write('\n'.join(output))
    
    print(f"Final level: {level}")

trace_divs_fixed('/home/xc/#Coding/gui_media_web_viewer/web/app.html')
