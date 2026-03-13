#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    Basic sanity tests for scapy integration.
    """

    def test_scapy_import(self):
        """Verify scapy is importable and basic classes exist."""
        from scapy.all import Packet
        pkt = Packet()
        assert pkt is not None

    def test_packet_creation(self):
        """Test creating a simple IP/ICMP packet."""
        pkt = IP(dst="8.8.8.8") / ICMP()
        assert pkt.dst == "8.8.8.8"
        # Check summary contains key elements instead of exact string
        summary = pkt.summary()
        assert "IP" in summary
        assert "ICMP" in summary
        assert "> 8.8.8.8" in summary

    def test_layer_stacking(self):
        """Test layer stacking logic (Ethernet over IP, etc.)."""
        pkt = Ether() / IP()
        assert pkt.haslayer(IP)
        assert pkt.haslayer(Ether)

if __name__ == "__main__":
    if not SCAPY_AVAILABLE:
        print("Scapy is not installed. Please run 'pip install scapy'")
        sys.exit(1)
    pytest.main([__file__])
