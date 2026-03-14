"""
Change Log Level Console Test (DE/EN)

DE:
Testet, ob das Log-Level über die Konsole geändert werden kann und die Änderung im Debug & DB-Modul wirksam wird.
EN:
Tests if the log level can be changed via console and the change is effective in the Debug & DB module.

Usage:
    pytest tests/test_change_log_level_console.py
"""

import pytest
import logging

class TestChangeLogLevelConsole:
    def test_change_log_level(self, capsys):
        """
        DE:
        Setzt das Log-Level auf DEBUG, prüft die Ausgabe, setzt zurück auf INFO.
        EN:
        Sets log level to DEBUG, checks output, resets to INFO.
        """
        logger = logging.getLogger("debug_db")
        # Ensure logger has a StreamHandler for console output
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
            logger.addHandler(handler)
        else:
            for h in logger.handlers:
                if not isinstance(h, logging.StreamHandler):
                    logger.addHandler(logging.StreamHandler())

        logger.setLevel(logging.INFO)
        logger.info("Info message")
        logger.debug("Debug message should not appear")
        out1 = capsys.readouterr().out
        assert "Info message" in out1
        assert "Debug message" not in out1

        logger.setLevel(logging.DEBUG)
        logger.debug("Debug message should appear")
        out2 = capsys.readouterr().out
        assert "Debug message should appear" in out2

        logger.setLevel(logging.INFO)
        logger.info("Info message again")
        out3 = capsys.readouterr().out
        assert "Info message again" in out3
