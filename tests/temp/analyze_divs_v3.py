
import re

def analyze_divs(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Better regex: find <div... or <div> but NOT </div>
    # Also ignore commented out divs if possible, but let's keep it simple for now.
    
    level = 0
    lines = content.splitlines()
    for i, line in enumerate(lines):
        # Remove comments for counting
        clean_line = re.sub(r'<!--.*?-->', '', line)
        
        opens = len(re.findall(r'<div[\s>]', clean_line, re.IGNORECASE))
        closes = len(re.findall(r'</div>', clean_line, re.IGNORECASE))
        
        level += opens
        level -= closes
        
        if level < 0:
            print(f"ERROR: Negative level {level} at line {i+1}")
            # print context
            for j in range(max(0, i-5), min(len(lines), i+6)):
                prefix = ">>>" if j == i else "   "
                print(f"{prefix} {j+1}: {lines[j]}")
            return
    
    print(f"Final level: {level}")

analyze_divs('/home/xc/#Coding/gui_media_web_viewer/web/app.html')
