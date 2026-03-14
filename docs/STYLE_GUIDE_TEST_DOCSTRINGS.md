# Test Docstring Style Guide

## Google-Style Bilingual Docstrings

- All test classes and functions should use Google-style docstrings.
- Provide both German (DE) and English (EN) descriptions.
- Example:

```python
class ExampleTest(unittest.TestCase):
    """
    DE:
    Testet die Beispiel-Funktion.

    EN:
    Tests the example function.
    """
    def test_example(self):
        """
        DE:
        Prüft, ob Beispiel korrekt funktioniert.

        EN:
        Verifies correct example behavior.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Fehler.
        """
        pass
```

## Docstring Structure

- Class docstring: Short summary (DE/EN)
- Method docstring: Purpose, Returns, Raises (DE/EN)
- Use consistent indentation and formatting.

---

> Reference this guide for all test docstring conventions. Combine with header variants from STYLE_GUIDE_TEST_HEADERS.md.
