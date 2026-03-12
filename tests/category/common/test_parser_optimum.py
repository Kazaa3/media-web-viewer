# Test: Parser-Optimum-JSON für alle Tools

import os
import json
from src.parsers import media_parser

TEST_FILES = [
    "media/Adam Grant - Geben und Nehmen.m4b",
    "media/Coldplay - Viva La Vida.opus",
    "media/Kid Cudi vs. Crookers - Day 'n' Night.opus",
    "media/Limp Bizkit - My Generation.opus",
    "media/Youth Of The Nation - P.O.D.opus",
    # Füge weitere Testdateien hinzu
]

PARSER_CONFIG = {
    "enable_ebml_parser": True,
    "enable_mkvparse_parser": True,
    "enable_enzyme_parser": True,
    "enable_pycdlib_parser": True,
    "enable_pymkv_parser": True,
    "enable_tinytag_parser": True,
    "enable_eyed3_parser": True,
    "enable_music_tag_parser": True,
}

RESULTS = {}

for file_path in TEST_FILES:
    abs_path = os.path.abspath(file_path)
    file_type = os.path.splitext(file_path)[1].lower()
    tags, times = media_parser.extract_metadata(
        abs_path,
        file_type=file_type,
        filename=os.path.basename(file_path),
        mode="full",
        PARSER_CONFIG=PARSER_CONFIG
    )
    # Optimum: Alle relevanten Felder pro Tool
    optimum = {}
    for tool in times:
        optimum[tool] = {k: v for k, v in tags.items() if tool in k}
    RESULTS[file_path] = optimum

with open("tests/artifacts/reports/parser_optimum_results.json", "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, indent=2, ensure_ascii=False)

print("Optimum-JSON für alle Tools geschrieben: tests/parser_optimum_results.json")
