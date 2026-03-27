"""
Console Output Check Unit Test (DE/EN)

DE:
Testet, ob eine Funktion korrekte Ausgaben in die Konsole schreibt.
EN:
Tests if a function writes correct output to the console.

Usage:
    pytest tests/test_check_console_output.py
"""

import pytest
import sys
from io import StringIO

# Example function to test
def print_feature_modal(data):
    print(f"Category: {data['category']}")
    print(f"Status: {data['status']}")
    print(f"Title: {data['title']}")
    print(f"Summary: {data['summary']}")

feature_modal_data = {
    "category": "Feature",
    "status": "COMPLETED",
    "title": "Modal",
    "summary": "Test summary for modal feature."
}

class TestConsoleOutput:
    def test_print_feature_modal_console(self):
        """
        DE:
        Prüft, ob die Funktion die erwarteten Ausgaben in die Konsole schreibt.
        EN:
        Checks if the function writes the expected output to the console.
        """
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        print_feature_modal(feature_modal_data)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        assert "Category: Feature" in output
        assert "Status: COMPLETED" in output
        assert "Title: Modal" in output
        assert "Summary: Test summary for modal feature." in output
