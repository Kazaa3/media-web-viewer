from pathlib import Path
from collections import defaultdict

categories = defaultdict(list)

for file in sorted(Path(".").glob("*.md")):
    with open(file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        if "<!-- Category:" in first_line:
            cat = first_line.split("Category: ")[1].split(" -->")[0]
            categories[cat].append(file.name)

print("✅ KATEGORIEN-ÜBERSICHT\n")
for cat in ["Untersuchungen", "Tests", "Parser", "UI/UX", "Planung"]:
    count = len(categories[cat])
    print(f"{cat}: {count} Dateien")

print(f"\n📊 Gesamt: {sum(len(v) for v in categories.values())} Dateien kategorisiert")
