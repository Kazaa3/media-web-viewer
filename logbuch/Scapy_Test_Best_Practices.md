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
- Nutze pytest für einfache und wiederholbare Tests.
- Vermeide echte Netzwerkpakete im CI/CD; nutze Simulation.
- Layer-Stacking und Paket-Parsing sind ideale Einstiegstests.
- Für fortgeschrittene Checks: sniff(), send(), sr() nur mit Vorsicht und ggf. Mocking.

## Integration in Media Web Viewer
- Testdatei: `tests/test_scapy_basic.py` enthält Basis-Checks.
- Erweiterbar für Integrationstests mit anderen Netzwerkmodulen.

---
*Letzte Aktualisierung: 10. März 2026*