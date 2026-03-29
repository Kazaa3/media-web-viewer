<!-- Title_DE: Scapy-Test Best Practices -->
<!-- Title_EN: Scapy Test Best Practices -->
<!-- Summary_DE: Tipps und Beispiele für Netzwerk- und Paket-Tests mit Scapy in Media Web Viewer. -->
<!-- Summary_EN: Tips and examples for network and packet testing with Scapy in Media Web Viewer. -->
<!-- Category: Tests -->
<!-- Status: ACTIVE -->

# Scapy-Test Best Practices

## Überblick
Scapy ist ein leistungsfähiges Python-Toolkit für Netzwerk- und Paket-Tests. In Media Web Viewer kann Scapy für grundlegende Netzwerk-Checks, Paketgenerierung und Integrationstests genutzt werden.

## Anwendungsfälle
- **Sanity-Check:** Prüfe, ob Scapy importierbar ist und grundlegende Klassen funktionieren.
- **Paketgenerierung:** Erstelle und analysiere IP-, TCP-, UDP-, ICMP-Pakete.
- **Layer-Stacking:** Teste Zusammensetzung von Ethernet/IP/ICMP/TCP/UDP.
- **Integration:** Kombiniere mit pytest für automatisierte Netzwerk-Tests.

## Beispiel-Test
```python
import pytest
from scapy.all import IP, ICMP, Ether

def test_scapy_import():
    pkt = IP(dst="8.8.8.8") / ICMP()
    assert pkt.dst == "8.8.8.8"
    assert "ICMP" in pkt.summary()

def test_layer_stacking():
    pkt = Ether() / IP() / ICMP()
    assert pkt.haslayer(IP)
    assert pkt.haslayer(Ether)
```

## Best Practices
## Fortgeschrittene Netzwerk- und Integrationstests
### Mocking von Netzwerkverkehr
Für CI/CD und sichere Tests empfiehlt sich das Mocken von send/sniff/sr:
```python
import pytest
from unittest.mock import patch
from scapy.all import IP, ICMP, send

def test_send_mock():
    pkt = IP(dst="8.8.8.8") / ICMP()
    with patch("scapy.all.send") as mock_send:
        send(pkt)
        mock_send.assert_called_once()
```

### Integration mit anderen Modulen
Scapy kann mit eigenen Netzwerkmodulen oder APIs kombiniert werden:
```python
import pytest
from scapy.all import IP, TCP
from my_network_module import analyze_packet

def test_packet_integration():
    pkt = IP(dst="192.168.1.1") / TCP(dport=80)
    result = analyze_packet(pkt)
    assert result == "HTTP"
```

### Sniffing und Analyse (nur lokal/mit Mocking)
```python
from scapy.all import sniff
import pytest

def test_sniff_mock(monkeypatch):
    def fake_sniff(*args, **kwargs):
        return ["dummy_packet"]
    monkeypatch.setattr("scapy.all.sniff", fake_sniff)
    packets = sniff(count=1)
    assert packets == ["dummy_packet"]
```

### Hinweise
- Für Integrationstests: Netzwerkfunktionen mocken, um CI/CD zu ermöglichen.
- Kombinierbar mit pytest, unittest.mock und monkeypatch.
## Integration in Media Web Viewer
- Testdatei: `tests/test_scapy_basic.py` enthält Basis-Checks.
- Erweiterbar für Integrationstests mit anderen Netzwerkmodulen.

---
*Letzte Aktualisierung: 10. März 2026*