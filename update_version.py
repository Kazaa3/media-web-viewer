#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update project version across all configured sync locations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


SEMVER_PATTERN = r"^\d+\.\d+\.\d+$"
SEMVER_INLINE_PATTERN = r"\d+\.\d+\.\d+"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_location_regex(line_pattern: str) -> re.Pattern[str] | None:
    if "${version}" not in line_pattern:
        return None

    static_parts = line_pattern.replace("${version}", "").strip()
    if not static_parts:
        return None

    regex_src = re.escape(line_pattern).replace(re.escape("${version}"), SEMVER_INLINE_PATTERN)
    return re.compile(regex_src)


def apply_location_update(content: str, line_pattern: str, target_version: str) -> tuple[str, int, str]:
    expected = line_pattern.replace("${version}", target_version)
    if expected in content:
        return content, 0, "already"

    location_regex = build_location_regex(line_pattern)
    if location_regex is None:
        return content, 0, "ambiguous"

    new_content, replacements = location_regex.subn(expected, content)
    if replacements > 0:
        return new_content, replacements, "updated"

    return content, 0, "missing"


def validate_version(version: str, pattern: str) -> bool:
    try:
        compiled = re.compile(pattern)
    except re.error:
        compiled = re.compile(SEMVER_PATTERN)
    return compiled.match(version) is not None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update all version references configured in VERSION_SYNC.json"
    )
    parser.add_argument(
        "--new-version",
        required=True,
        help="Target version in semantic format (e.g. <version>)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing files",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    root = Path(__file__).resolve().parent
    version_file = root / "VERSION"
    sync_file = root / "VERSION_SYNC.json"
        # Example usage for version 1.01:
        # python update_version.py --new-version 1.01

    if not version_file.exists():
        print(f"❌ Missing VERSION file: {version_file}")
        return 1

    if not sync_file.exists():
        print(f"❌ Missing VERSION_SYNC.json file: {sync_file}")
        return 1

    sync_config = load_json(sync_file)
    version_pattern = sync_config.get("version_format", {}).get("pattern", SEMVER_PATTERN)

    target_version = args.new_version.strip()
    if not validate_version(target_version, version_pattern):
        print(f"❌ Invalid version format: {target_version}")
        print(f"   Expected pattern: {version_pattern}")
        return 1

    current_version = version_file.read_text(encoding="utf-8").strip()
    print(f"📌 Current VERSION: {current_version}")
    print(f"🎯 Target VERSION:  {target_version}")

    changes: list[tuple[Path, int]] = []
    warnings: list[str] = []
    errors: list[str] = []

    # Update VERSION file first
    if current_version != target_version:
        if not args.dry_run:
            version_file.write_text(target_version + "\n", encoding="utf-8")
        changes.append((version_file, 1))

    # Update VERSION_SYNC.json top-level version + metadata date
    config_changed = False
    if sync_config.get("version") != target_version:
        sync_config["version"] = target_version
        config_changed = True

    metadata = sync_config.get("metadata")
    if isinstance(metadata, dict):
        today = date.today().isoformat()
        if metadata.get("last_updated") != today:
            metadata["last_updated"] = today
            config_changed = True

    if config_changed:
        if not args.dry_run:
            save_json(sync_file, sync_config)
        changes.append((sync_file, 1))

    # Apply all location updates
    for location in sync_config.get("sync_locations", []):
        rel_file = location.get("file")
        line_pattern = location.get("line_pattern", "")
        required = bool(location.get("required", True))

        if not rel_file:
            continue

        path = root / rel_file
        if not path.exists():
            message = f"{rel_file}: file not found"
            if required:
                errors.append(message)
            else:
                warnings.append(message)
            continue

        content = path.read_text(encoding="utf-8")
        updated, replaced_count, status = apply_location_update(content, line_pattern, target_version)

        if status == "ambiguous":
            message = f"{rel_file}: skipped ambiguous pattern '{line_pattern}'"
            if required:
                errors.append(message)
            else:
                warnings.append(message)
            continue

        if status == "missing":
            message = f"{rel_file}: no replaceable match for '{line_pattern}'"
            if required:
                errors.append(message)
            else:
                warnings.append(message)
            continue

        if replaced_count > 0:
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8")
            changes.append((path, replaced_count))

    print("\n📊 Update summary")
    if changes:
        for path, count in changes:
            print(f"   ✅ {path.relative_to(root)} (changes: {count})")
    else:
        print("   ℹ️  No file updates needed")

    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"   - {warning}")

    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for error in errors:
            print(f"   - {error}")
        return 1

    if args.dry_run:
        print("\n🧪 Dry-run only: no files were written")

    print("\n✅ Version update completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
