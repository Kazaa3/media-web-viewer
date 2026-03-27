#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Environment Packages Fallback Regression
# Eingabewerte: get_environment_info() mit simuliertem pip-Fehler
# Ausgabewerte: Nicht-leere installed_packages via Fallback
# Testdateien: main.py
# Kommentar: Verhindert Regression "No packages found" im Options-Tab bei pip-Fehlern.

from types import SimpleNamespace

import src.core.main as main

def test_installed_packages_fallback_when_pip_returns_non_zero(monkeypatch):
    """If pip list fails, environment info must still return package data via fallback."""

    class FakeDist:
        def __init__(self, name, version):
            self.metadata = {"Name": name}
            self.version = version

    def fake_run(cmd, capture_output=True, text=True, timeout=None, **kwargs):
        first = str(cmd[0]) if cmd else ""
        if first.endswith("python") and "pip" in cmd and "list" in cmd:
            return SimpleNamespace(returncode=1, stdout="", stderr="pip failed")
        if first == "conda":
            return SimpleNamespace(returncode=1, stdout="", stderr="conda missing")
        return SimpleNamespace(returncode=0, stdout="Python 3.14.2", stderr="")

    monkeypatch.setattr("subprocess.run", fake_run)
    monkeypatch.setattr(
        "importlib.metadata.distributions",
        lambda: [FakeDist("fallback-demo", "1.0.0"), FakeDist("another-demo", "2.0.0")]
    )

    main._ENV_INFO_CACHE["data"] = None
    main._ENV_INFO_CACHE["ts"] = 0.0

    try:
        info = main.get_environment_info(force_refresh=True)

        assert isinstance(info.get("installed_packages"), list)
        assert info.get("package_count", 0) >= 1

        names = {pkg.get("name") for pkg in info.get("installed_packages", [])}
        assert "fallback-demo" in names
    finally:
        main._ENV_INFO_CACHE["data"] = None
        main._ENV_INFO_CACHE["ts"] = 0.0
