import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
scripts = re.findall(r'<script.*?>\n(.*?)</script>', content, re.DOTALL)

for i, script in enumerate(scripts):
    print(f"Script #{i} (Length: {len(script)}):")
    snippet = script.strip()[:100].replace('\n', ' ')
    print(f"  Snippet: {snippet}...")
    opens = script.count('{')
    closes = script.count('}')
    print(f"  Braces: {{: {opens}, }}: {closes} (Diff: {opens - closes})")
    opens_p = script.count('(')
    closes_p = script.count(')')
    print(f"  Parens: (: {opens_p}, ): {closes_p} (Diff: {opens_p - closes_p})")
