# Test: M4B mit allen Parser-Tools

import os
import json
from src.parsers import media_parser

TEST_M4B = "media/Adam Grant - Geben und Nehmen.m4b"

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

file_type = os.path.splitext(TEST_M4B)[1].lower()

# Alle Tools im Full-Mode testen
results = {}
tags, times = media_parser.extract_metadata(
    os.path.abspath(TEST_M4B),
    file_type=file_type,
    filename=os.path.basename(TEST_M4B),
    mode="full",
    PARSER_CONFIG=PARSER_CONFIG
)

for tool in times:
    results[tool] = {k: v for k, v in tags.items() if tool in k or tool == "mutagen"}

with open("tests/artifacts/reports/m4b_all_tools_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("M4B-Test mit allen Tools abgeschlossen: tests/artifacts/reports/m4b_all_tools_results.json")
