#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Scapy Integration Test
# Eingabewerte: Scapy library
# Ausgabewerte: Packet-Status, Layer-Stacking
# Testdateien: Keine
# Kommentar: Testet grundlegende Scapy-Integration.
"""
Scapy Integration Test Suite (DE/EN)
====================================

DE:
Testet grundlegende Scapy-Integration und Paket-Erstellung.

EN:
Tests basic Scapy integration and packet creation.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import pytest
import sys
import os

# Ensure scapy can be imported
try:
    from scapy.all import IP, ICMP, Ether
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

@pytest.mark.skipif(not SCAPY_AVAILABLE, reason="Scapy not installed")
class TestScapyBasic:
    """
    DE:
    Testet grundlegende Scapy-Integration und Paket-Erstellung.

    EN:
    Tests basic Scapy integration and packet creation.
    """
    def test_scapy_import(self):
        """
        DE:
        Prüft, ob Scapy importierbar ist und Grundklassen existieren.

        EN:
        Verifies Scapy is importable and basic classes exist.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Import oder Klasse fehlt.
        """
        from scapy.all import Packet
        pkt = Packet()
        assert pkt is not None

    def test_packet_creation(self):
        """
        DE:
        Testet das Erstellen eines einfachen IP/ICMP-Pakets.

        EN:
        Tests creating a simple IP/ICMP packet.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Paket nicht korrekt.
        """
        pkt = IP(dst="8.8.8.8") / ICMP()
        assert pkt.dst == "8.8.8.8"
        # Check summary contains key elements instead of exact string
        summary = pkt.summary()
        assert "IP" in summary
        assert "ICMP" in summary
        assert "> 8.8.8.8" in summary

    def test_layer_stacking(self):
        """
        DE:
        Testet Layer-Stacking-Logik (Ethernet über IP, etc.).

        EN:
        Tests layer stacking logic (Ethernet over IP, etc.).
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Layer fehlt.
        """
        pkt = Ether() / IP()
        assert pkt.haslayer(IP)
        assert pkt.haslayer(Ether)

if __name__ == "__main__":
    if not SCAPY_AVAILABLE:
        print("Scapy is not installed. Please run 'pip install scapy'")
        sys.exit(1)
    pytest.main([__file__])
