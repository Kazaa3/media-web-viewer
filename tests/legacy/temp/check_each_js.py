import re
from pathlib import Path
import subprocess

content = Path('web/app.html').read_text(encoding='utf-8')
matches = re.finditer(r'<script.*?>\n?(.*?)\n?<\/script>', content, re.DOTALL)

for i, m in enumerate(matches):
    code = m.group(1).strip()
    if not code: continue
    
    with open(f'/tmp/script_{i}.js', 'w') as f:
        f.write(code)
    
    res = subprocess.run(['node', '--check', f'/tmp/script_{i}.js'], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR in Script #{i}:")
        print(res.stderr)
