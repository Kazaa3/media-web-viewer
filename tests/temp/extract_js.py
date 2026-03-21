import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
# Find all <script> content
matches = re.finditer(r'<script.*?>\n?(.*?)\n?<\/script>', content, re.DOTALL)

with open('/tmp/app_full.js', 'w') as f:
    for m in matches:
        code = m.group(1).strip()
        if code:
            f.write(code + '\n;\n') # add ; to separate blocks
