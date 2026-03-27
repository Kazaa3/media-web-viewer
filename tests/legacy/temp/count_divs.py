import re

content = open('/home/xc/#Coding/gui_media_web_viewer/web/app.html').read()
# Find Options tab start
start_index = content.find('id="system-configuration-persistence-panel"')
# Find Parser tab start
end_index = content.find('id="regex-provider-chain-orchestrator-panel"')

options_content = content[start_index:end_index]

opens = len(re.findall(r'<div', options_content))
closes = len(re.findall(r'</div>', options_content))

print(f"Opens: {opens}")
print(f"Closes: {closes}")
print(f"Diff: {opens - closes}")
