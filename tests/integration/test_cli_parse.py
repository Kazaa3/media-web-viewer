import os
import pytest

# Unit test placeholder for mwv-cli parse command.
# Skips if `cli` module is not yet implemented; when implemented this test
# verifies that `cli.main(['parse', path, '--output', out])` calls
# `extract_metadata()` with the given path and writes JSON output.

cli = pytest.importorskip("cli", reason="mwv-cli not implemented yet")

def test_cli_parse_calls_extract_metadata(monkeypatch, tmp_path):
    called = {}

    def fake_extract_metadata(path, *args, **kwargs):
        called['path'] = path
        return {'mock': 'metadata'}

    monkeypatch.setattr(cli, 'extract_metadata', fake_extract_metadata)

    out_file = tmp_path / "meta.json"
    argv = ['parse', '/some/media/file.mp3', '--output', str(out_file)]

    # assume cli.main accepts argv list
    cli.main(argv)

    assert called.get('path') == '/some/media/file.mp3'
    assert out_file.exists()
    content = out_file.read_text()
    assert 'mock' in content
