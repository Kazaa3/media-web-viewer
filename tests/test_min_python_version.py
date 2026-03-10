import sys

def test_min_python_version():
    """Test gibt die niedrigst mögliche Python-Version zurück, die das Projekt unterstützt."""
    # Annahme: Mindestversion ist in README.md oder environment.yml dokumentiert
    min_version = (3, 10)
    assert sys.version_info >= min_version, f"Python {min_version[0]}.{min_version[1]}+ erforderlich, gefunden: {sys.version_info.major}.{sys.version_info.minor}"
    print(f"Gefundene Python-Version: {sys.version_info.major}.{sys.version_info.minor}")
    return f"Minimal unterstützte Version: {min_version[0]}.{min_version[1]}"

if __name__ == "__main__":
    print(test_min_python_version())
