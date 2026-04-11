
import re

def analyze_divs_verbose(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    level = 0
    lines = content.splitlines()
    for i, line in enumerate(lines):
        # Remove comments
        clean_line = re.sub(r'<!--.*?-->', '', line)
        
        opens = len(re.findall(r'<div[\s>]', clean_line, re.IGNORECASE))
        closes = len(re.findall(r'</div>', clean_line, re.IGNORECASE))
        
        level += opens
        level -= closes
        
        if i % 100 == 0:
            print(f"Line {i}: Level {level}")
        
        if level < -10: # Allow some drift but stop if it's crazy
             print(f"STOP: Crazy level {level} at line {i+1}")
             break
    
    print(f"Final line {len(lines)}: Level {level}")

analyze_divs_verbose('/home/xc/#Coding/gui_media_web_viewer/web/app.html')
