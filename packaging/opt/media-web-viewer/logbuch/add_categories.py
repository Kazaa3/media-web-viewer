from pathlib import Path

# Kategorie-Zuordnung
categories = {
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

current_dir = Path(".")

for file in sorted(current_dir.glob("*.md")):
    # Extrahiere Nummer aus Dateinamen
    name = file.stem
    prefix = name.split("_")[0] if "_" in name else ""

    if prefix in categories:
        content = file.read_text(encoding='utf-8')

        # Prüfe, ob Kategorie bereits vorhanden
        if "<!-- Category:" in content:
            continue

        category = categories[prefix]

        # Füge Kategorie am Anfang hinzu
        new_content = f"<!-- Category: {category} -->\n\n{content}"

        file.write_text(new_content, encoding='utf-8')
        print(f"✓ {file.name} -> {category}")

print("\n✅ Alle Dateien mit Kategorien versehen!")
