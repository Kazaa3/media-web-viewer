import pytest

def test_pyscreeze_import_and_api():
    try:
        import pyscreeze
    except Exception:
        pytest.skip("pyscreeze not installed")
    # basic API sanity checks (do not perform real screenshot in unit gate)
    assert hasattr(pyscreeze, "screenshot")
    assert hasattr(pyscreeze, "locateOnScreen") or hasattr(pyscreeze, "locate")