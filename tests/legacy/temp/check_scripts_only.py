from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()
p = 0
for i, line in enumerate(lines):
    old_p = p
    num_open = line.count('(')
    num_close = line.count(')')
    p += num_open - num_close
    if num_open != num_close:
        # print first 50 lines that change the balance
        # actually, just print the final balance for the script sections
        pass

# I'll check all script blocks
# Actually, I'll use THE WHOLE SCRIPT blocks and see if any is unbalanced
import re
scripts = re.findall(r'<script.*?>\n(.*?)<\/script>', content, re.DOTALL)
for i, script in enumerate(scripts):
    pb = script.count('(') - script.count(')')
    if pb != 0:
        print(f"Script #{i} BALANCE: {pb}")
