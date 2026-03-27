import re

def find_extra_bracket_whole_file(text):
    stack = []
    lines = text.split('\n')
    
    in_s_quote = False
    in_d_quote = False
    in_backtick = False
    in_comment = False
    
    for i, line in enumerate(lines):
        # Rough check
        line_clean = line
        # Simple string removal
        line_clean = re.sub(r'\'(.*?)\'', '', line_clean)
        line_clean = re.sub(r'"(.*?)"', '', line_clean)
        line_clean = re.sub(r'`(.*?)`', '', line_clean)
        
        for char in line_clean:
            if char == '[': stack.append(i+1)
            elif char == ']':
                if not stack:
                    print(f'Line {i+1}: UNMATCHED CLOSING BRACKET: {line.strip()}')
                else:
                    stack.pop()

with open('/home/xc/#Coding/gui_media_web_viewer/web/app.html', 'r', encoding='utf-8') as f:
    find_extra_bracket_whole_file(f.read())
