import os
import pytest
import subprocess

# Placeholder test for safe subprocess wrapper (ffprobe fallback)
# Skips if the expected module `tools.ffprobe_wrapper` is not present.

ffw = pytest.importorskip("tools.ffprobe_wrapper", reason="ffprobe wrapper not implemented")


def test_ffprobe_wrapper_uses_list_args(monkeypatch):
    captured = {}

    def fake_run(args, stdout, stderr, check):
        captured['args'] = args
        class Dummy:
            stdout = b'{}'
        return Dummy()

    monkeypatch.setattr(subprocess, 'run', fake_run)

    # call wrapper with a filename that might contain spaces and special chars
    ffw.run_ffprobe('/media/smb/test file (1).mp3')

    assert isinstance(captured.get('args'), list)
    assert '/media/smb/test file (1).mp3' in captured['args']
