
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Environment Handler Test
# Eingabewerte: env_handler.py, environment.yml
# Ausgabewerte: Status, Log-Ausgaben, Fehler
# Testdateien: env_handler.py, tests/test_env_handler.py
# ERWEITERUNGEN (TODO): [ ] Erweiterte Validierung, Mocking
# KOMMENTAR: Prüft die Validierung und Funktion des Environment Handlers
# VERWENDUNG: python tests/test_env_handler.py

"""
KATEGORIE:
----------
Environment Handler Test

ZWECK:
------
Prüft die Validierung und Funktion des Environment Handlers.

EINGABEWERTE:
-------------
- env_handler.py
- environment.yml

AUSGABEWERTE:
-------------
- Status, Log-Ausgaben, Fehler

TESTDATEIEN:
------------
- env_handler.py
- tests/test_env_handler.py

ERWEITERUNGEN (TODO):
---------------------
- [ ] Erweiterte Validierung, Mocking

VERWENDUNG:
-----------
    python tests/test_env_handler.py
"""

import os
import unittest

from test_env_handler import test_env_handler


class TestEnvHandler(unittest.TestCase):

    def test_env_handler(self):
        self.assertTrue(test_env_handler())


if __name__ == '__main__':
    unittest.main()