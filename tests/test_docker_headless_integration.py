import os
import pytest

# Gated integration test: runs only when ENABLE_INTEGRATION=1

pytestmark = pytest.mark.skipif(os.environ.get('ENABLE_INTEGRATION') != '1', reason='Integration tests gated')


def test_headless_container_parse_smoke(tmp_path):
    # This test is a placeholder for a CI job which will build/run the
    # headless docker image and mount fixtures. The CI job should:
    # - run the container in MODE=cli or MODE=headless
    # - mount tests/fixtures into the container
    # - run `mwv-cli parse <fixture>` and assert metadata JSON produced
    # Implementers: invoke docker build/run in CI and assert artifact outputs.
    assert True
