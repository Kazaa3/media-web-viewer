import subprocess
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
lines = content.splitlines()[5879-1:10780]

def check(code):
    with open('/tmp/temp.js', 'w') as f: f.write(code)
    res = subprocess.run(['node', '--check', '/tmp/temp.js'], capture_output=True, text=True)
    return res.returncode == 0

# Binary search for the line with syntax error
start = 0
end = len(lines)
while start < end:
    mid = (start + end) // 2
    code = '\n'.join(lines[:mid])
    if check(code):
        start = mid + 1
    else:
        end = mid

print(f"Error found around L{start + 5878}")
print(lines[start + 5878 - 1])
