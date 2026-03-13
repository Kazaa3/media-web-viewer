import subprocess
import importlib
import pytest

def test_ffprobe_parser_uses_list_args_and_no_shell(monkeypatch):
    try:
        from src.parsers import ffprobe_parser as fp  # type: ignore
    except Exception:
        pytest.skip("ffprobe_parser not present")
    called = {}

    def fake_run(*args, **kwargs):
        called["args"] = args
        called["kwargs"] = kwargs
        class P:
            returncode = 0
            stdout = "{}"
            stderr = ""
        return P()
    monkeypatch.setattr(subprocess, "run", fake_run)
    fp.parse("/tmp/weird;rm -rf /", None, None, None, mode="lightweight")
    assert "args" in called
    # first positional arg should be the command list
    cmd = called["args"][0]
    assert isinstance(cmd, list), "subprocess.run called with a non-list command"
    # ensure not using shell=True
    assert called["kwargs"].get("shell", False) is False