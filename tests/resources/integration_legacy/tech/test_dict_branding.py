import json
from pathlib import Path

def test_dict_branding_in_i18n():
    """Verify that 'dict' is the official app title in all supported languages."""
    i18n_path = Path(__file__).resolve().parent.parent.parent.parent / "web" / "i18n.json"
    assert i18n_path.exists(), f"i18n.json not found at {i18n_path}"
    
    with open(i18n_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for lang in ['de', 'en']:
        assert lang in data, f"Language '{lang}' missing in i18n.json"
        assert 'app_title' in data[lang], f"app_title missing in '{lang}'"
        assert data[lang]['app_title'] == "dict", f"Branding mismatch in '{lang}': expected 'dict', got '{data[lang]['app_title']}'"

def test_dict_branding_in_main_py():
    """Verify that 'dict' is mentioned in the main entry point as branding."""
    main_path = Path(__file__).resolve().parent.parent.parent.parent / "src" / "core" / "main.py"
    assert main_path.exists()
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the branding comment at the top
    assert "#dict" in content or "dict - Desktop Media Player" in content, "Branding 'dict' missing in main.py"

if __name__ == "__main__":
    try:
        test_dict_branding_in_i18n()
        print("✅ i18n branding: OK")
        test_dict_branding_in_main_py()
        print("✅ main.py branding: OK")
    except AssertionError as e:
        print(f"❌ Branding test failed: {e}")
        exit(1)
