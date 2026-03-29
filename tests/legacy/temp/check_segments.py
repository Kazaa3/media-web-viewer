
import re

def check_segment(filepath, start_line, end_line):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    segment = "".join(lines[start_line-1:end_line])
    # Remove comments
    segment = re.sub(r'<!--.*?-->', '', segment)
    
    opens = len(re.findall(r'<div\b', segment, re.IGNORECASE))
    closes = len(re.findall(r'</div>', segment, re.IGNORECASE))
    
    print(f"Segment {start_line}-{end_line} | Opens: {opens} | Closes: {closes} | Balance: {opens - closes}")

print("Checking Options views:")
check_segment('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 3231, 3578) # General
check_segment('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 3580, 3706) # Tools
check_segment('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 3708, 3997) # Environment
check_segment('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 3231, 3999) # Whole Options Tab
