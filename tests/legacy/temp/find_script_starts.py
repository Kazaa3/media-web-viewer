import re
from pathlib import Path

content = Path('web/app.html').read_text(encoding='utf-8')
for i, m in enumerate(re.finditer(r'<script.*?>', content)):
    print(f"Script #{i} starts at L{content[:m.start()].count('\n') + 1}")
