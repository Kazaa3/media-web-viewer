import re

def find_extra_opener(text):
    stack = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Remove strings
        line_clean = line
        line_clean = re.sub(r'\'(.*?)\'', '', line_clean)
        line_clean = re.sub(r'"(.*?)"', '', line_clean)
        line_clean = re.sub(r'`(.*?)`', '', line_clean)
        
        for j, char in enumerate(line_clean):
            if char == '[':
                stack.append((i+1, j+1, line.strip()))
            elif char == ']':
                if stack:
                    stack.pop()

    for line_no, col, line_text in stack:
         print(f'Line {line_no}: UNMATCHED OPENING BRACKET: {line_text}')

with open('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 'r', encoding='utf-8') as f:
    find_extra_opener(f.read())
