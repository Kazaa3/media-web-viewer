#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Backend Connection Test
# Eingabewerte: Eel-Server
# Ausgabewerte: Connection-Status
# Testdateien: Keine
# Kommentar: Testet Eel Backend-Connection.
"""
Backend Connection Test Suite (DE/EN)
=====================================

DE:
Testet die Verbindung zum Eel-Backend und prüft die Ping-Funktion.

EN:
Tests connection to the Eel backend and verifies the ping function.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure project root is in path

import src.core.main as main

class TestBackendConnection(unittest.TestCase):
    """
    DE:
    Testet die Backend-Verbindung und Ping-Funktion.

    EN:
    Tests backend connection and ping function.
    """
    def test_ping_response(self):
        """
        DE:
        Prüft, ob main.ping() den erwarteten Wert zurückgibt.

        EN:
        Verifies that main.ping() returns the expected value.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Antwort nicht wie erwartet.
        """
        # We need to make sure ping exists in main.py
        if hasattr(main, 'ping'):
            response = main.ping()
            self.assertEqual(response.get('status'), 'ok')
            self.assertEqual(response.get('message'), 'pong')
        else:
            self.fail("src/core/main.py does not have a ping function yet.")

if __name__ == '__main__':
    print("Running Backend Connection Tests...")
    unittest.main()
