import re

content = open('/home/xc/#Coding/gui_media_web_viewer/web/app.html').read()

current_level = 0
for i, line in enumerate(content.splitlines()):
    delta_opens = len(re.findall(r'<div', line))
    delta_closes = len(re.findall(r'</div>', line))
    new_level = current_level + delta_opens - delta_closes
    if delta_opens != delta_closes:
        if i >= 2320 and i <= 3800:
             print(f"Line {i+1}: {line.strip()} | Level {current_level} -> {new_level}")
    current_level = new_level
