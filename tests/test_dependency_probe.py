#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Environment Dependency Probe
# Eingabewerte: Python Import-Module
# Ausgabewerte: Fehlende Pakete + JSON Report
# Testdateien: Keine
# Kommentar: Prüft kritische Python-Abhängigkeiten und protokolliert fehlende Module für Troubleshooting.

import importlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, UTC
from pathlib import Path

CRITICAL_DEPENDENCIES = {
    "eel": "eel",
    "bottle": "bottle",
    "bottle-websocket": "bottle_websocket",
    "mutagen": "mutagen",
    "pymediainfo": "pymediainfo",
    "m3u8": "m3u8",
    "python-vlc": "vlc",
    "psutil": "psutil",
    "future": "future",
    "python3-tk": "tkinter",
    "gevent": "gevent",
    "gevent-websocket": "geventwebsocket",
}

SUBPROCESS_TOOLS = {
    "ffmpeg": ["ffmpeg", "-version"],
    "vlc": ["vlc", "--version"],
}

BROWSER_CANDIDATES = {
    "chrome": ["google-chrome-stable", "google-chrome"],
    "firefox": ["firefox", "firefox-esr"],
    "chromium": ["chromium-browser", "chromium"],
}


def probe_dependencies() -> dict:
    missing: list[dict[str, str]] = []
    available: list[dict[str, str]] = []

    for package_name, module_name in CRITICAL_DEPENDENCIES.items():
        try:
            importlib.import_module(module_name)
            available.append({"package": package_name, "module": module_name})
        except Exception as exc:
            missing.append(
                {
                    "package": package_name,
                    "module": module_name,
                    "error": str(exc),
                }
            )

    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "available": available,
        "missing": missing,
        "missing_count": len(missing),
    }


def probe_subprocess_tools() -> dict:
    checks: list[dict[str, str | int | bool]] = []
    failed = 0

    for tool_name, cmd in SUBPROCESS_TOOLS.items():
        resolved = shutil.which(cmd[0])
        if not resolved:
            checks.append(
                {
                    "tool": tool_name,
                    "command": " ".join(cmd),
                    "ok": False,
                    "error": f"Executable '{cmd[0]}' not found in PATH",
                }
            )
            failed += 1

            continue

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=8,
            )
            output = (result.stdout or result.stderr or "").splitlines()
            first_line = output[0].strip() if output else ""

            checks.append(
                {
                    "tool": tool_name,
                    "command": " ".join(cmd),
                    "resolved_path": resolved,
                    "ok": result.returncode == 0,
                    "returncode": result.returncode,
                    "version_hint": first_line,
                }
            )
            if result.returncode != 0:
                failed += 1
        except subprocess.TimeoutExpired:
            checks.append(
                {
                    "tool": tool_name,
                    "command": " ".join(cmd),
                    "resolved_path": resolved,
                    "ok": False,
                    "error": "Timeout while executing command",
                }
            )
            failed += 1
        except Exception as exc:
            checks.append(
                {
                    "tool": tool_name,
                    "command": " ".join(cmd),
                    "resolved_path": resolved,
                    "ok": False,
                    "error": str(exc),
                }
            )
            failed += 1

    return {
        "checks": checks,
        "failed_count": failed,
    }


def probe_browsers() -> dict:
    checks: list[dict[str, str | int | bool]] = []
    failed = 0
    available = 0

    for browser_name, candidates in BROWSER_CANDIDATES.items():
        resolved_exec = None
        for candidate in candidates:
            resolved = shutil.which(candidate)
            if resolved:
                resolved_exec = resolved
                break

        if not resolved_exec:
            checks.append(
                {
                    "tool": browser_name,
                    "command": f"{candidates[0]} --version",
                    "ok": False,
                    "error": f"No executable found in PATH ({', '.join(candidates)})",
                }
            )
            failed += 1
            continue

        try:
            result = subprocess.run(
                [resolved_exec, "--version"],
                capture_output=True,
                text=True,
                timeout=8,
            )
            output = (result.stdout or result.stderr or "").splitlines()
            first_line = output[0].strip() if output else ""
            ok = result.returncode == 0
            checks.append(
                {
                    "tool": browser_name,
                    "command": f"{resolved_exec} --version",
                    "resolved_path": resolved_exec,
                    "ok": ok,
                    "returncode": result.returncode,
                    "version_hint": first_line,
                }
            )
            if ok:
                available += 1
            else:
                failed += 1
        except subprocess.TimeoutExpired:
            checks.append(
                {
                    "tool": browser_name,
                    "command": f"{resolved_exec} --version",
                    "resolved_path": resolved_exec,
                    "ok": False,
                    "error": "Timeout while executing command",
                }
            )
            failed += 1
        except Exception as exc:
            checks.append(
                {
                    "tool": browser_name,
                    "command": f"{resolved_exec} --version",
                    "resolved_path": resolved_exec,
                    "ok": False,
                    "error": str(exc),
                }
            )
            failed += 1

    return {
        "checks": checks,
        "failed_count": failed,
        "available_count": available,
        "required_any": True,
    }


def write_report(report: dict, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def run(output_file: Path) -> bool:
    report = probe_dependencies()
    subprocess_report = probe_subprocess_tools()
    browser_report = probe_browsers()
    report["subprocess"] = subprocess_report
    report["browsers"] = browser_report
    write_report(report, output_file)

    print("\n🔎 Dependency Probe Report")
    print(f"   Python: {report['python_executable']}")
    print(f"   Report: {output_file}")

    print("\n⚙️  Subprocess Tool Checks")
    for check in subprocess_report["checks"]:
        if check.get("ok"):
            print(f"   ✅ {check['tool']}: {check.get('version_hint', '')}")
        else:
            print(f"   ❌ {check['tool']}: {check.get('error', 'command failed')} (cmd: {check['command']})")

    if subprocess_report["failed_count"] > 0:
        print(f"\n❌ Subprocess checks failed: {subprocess_report['failed_count']}")
    else:
        print("\n✅ Subprocess checks passed")

    print("\n🌐 Browser Checks (chrome/firefox/chromium)")
    for check in browser_report["checks"]:
        if check.get("ok"):
            print(f"   ✅ {check['tool']}: {check.get('version_hint', '')}")
        else:
            print(f"   ❌ {check['tool']}: {check.get('error', 'command failed')} (cmd: {check['command']})")

    if browser_report["available_count"] > 0:
        print(f"\n✅ Browser checks passed (Fallback aktiv, verfügbar: {browser_report['available_count']}/3)")
        browser_required_ok = True
    else:
        print("\n❌ Browser checks failed: kein unterstützter Browser verfügbar")
        browser_required_ok = False

    if report["missing_count"] == 0 and subprocess_report["failed_count"] == 0 and browser_required_ok:
        print("✅ Alle kritischen Abhängigkeiten vorhanden")
        return True

    print(f"❌ Fehlende Abhängigkeiten: {report['missing_count']}")
    for item in report["missing"]:
        print(f"   - {item['package']} (import: {item['module']}) -> {item['error']}")

    print("\n📦 Installiere fehlende Pakete z. B. mit:")
    print("   pip install -r requirements.txt")
    print("   pip install psutil future")
    print("\n🧩 Prüfe Systemtools z. B. mit:")
    print("   sudo apt install ffmpeg vlc python3-tk")
    print("\n🌐 Browser installieren (mind. einen):")
    print("   sudo apt install chromium-browser   # oder: chromium")
    print("   sudo apt install firefox-esr        # optional")
    print("   # Chrome: google-chrome-stable aus Google-Repo installieren")
    return False


if __name__ == "__main__":
    report_path = Path("logs/dependency_probe_report.json")
    success = run(report_path)
    sys.exit(0 if success else 1)
