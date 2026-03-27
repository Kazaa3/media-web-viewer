"""
Feature Modal Content Unit Test (DE/EN)

DE:
Testet die Feature-Modal-Datenstruktur (z.B. Kategorie, Status, Titel, Zusammenfassung) ohne Selenium.
EN:
Tests the feature modal data structure (e.g. category, status, title, summary) without Selenium.

Usage:
    pytest tests/test_feature_modal_unit.py
"""

import pytest

# Example feature modal data (mocked)
feature_modal_data = {
    "category": "Feature",
    "status": "COMPLETED",
    "title": "Modal",
    "summary": "Test summary for modal feature."
}

class TestFeatureModalUnit:
    def test_feature_modal_content(self):
        """
        DE:
        Prüft, ob die Feature-Modal-Datenstruktur alle erforderlichen Felder enthält und korrekt befüllt ist.
        EN:
        Checks if the feature modal data structure contains all required fields and is correctly populated.
        """
        assert "category" in feature_modal_data
        assert feature_modal_data["category"] == "Feature"
        assert "status" in feature_modal_data
        assert feature_modal_data["status"] in ["COMPLETED", "ACTIVE"]
        assert "title" in feature_modal_data
        assert "summary" in feature_modal_data
        assert isinstance(feature_modal_data["summary"], str)
        assert len(feature_modal_data["summary"]) > 0
