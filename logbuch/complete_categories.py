from pathlib import Path

categories = {
    "00_README": "Übersicht",
    "01": "Untersuchungen",
    "02": "Tests",
    "03": "UI/UX",
    "04": "Untersuchungen",
    "05": "Untersuchungen",
    "06": "Planung",
    "07": "Parser",
    "08": "Parser",
    "09": "Parser",
    "10": "Untersuchungen",
    "11": "UI/UX",
    "12": "Parser",
    "13": "Parser",
    "14": "Parser",
    "15": "UI/UX",
    "16": "UI/UX",
    "17": "Untersuchungen",
    "18": "Planung",
    "19": "Parser",
    "20": "Parser",
    "21": "Tests",
    "22": "Parser",
    "23": "Tests",
    "24": "Tests",
    "25": "UI/UX",
    "26": "Untersuchungen",
    "27": "Parser",
    "28": "UI/UX",
    "29": "Planung",
    "30": "Tests",
    "31": "Planung",
    "32": "Planung",
    "33": "Planung",
    "34": "Planung"
}

count = 0
for file in sorted(Path(".").glob("*.md")):
    name = file.stem
    prefix = name.split("_")[0] if "_" in name else name

    if prefix not in categories:
        continue

    content = file.read_text(encoding='utf-8')

    if "<!-- Category:" in content:
        continue

    category = categories[prefix]
    new_content = f"<!-- Category: {category} -->\n\n{content}"
    file.write_text(new_content, encoding='utf-8')
    count += 1
    print(f"✓ {file.name} -> {category}")

print(f"\n✅ {count} neue Kategorien hinzugefügt")

# Verifiziere
with_cat = len([f for f in Path(".").glob("*.md") if "<!-- Category:" in f.read_text()])
print(f"📊 Gesamt Dateien mit Kategorie: {with_cat}")
