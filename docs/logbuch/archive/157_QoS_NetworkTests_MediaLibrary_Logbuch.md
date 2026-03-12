# QoS Netzwerk-Tests für Media-Library (Backend/Frontend, One-Way RTT)

## Datum: 10. März 2026

---

## Thema: Quality of Service (QoS) Tests mit iperf3 & Ping – Backend/Frontend, One-Way RTT

### Installation
```bash
pip install iperf3 subprocess32
sudo apt install iperf3
```

---

### 1. Ping QoS Test (Frontend → Backend)
```python
import subprocess
import platform
import asyncio

def ping_qos(host, count=10):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, str(count), host]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        rtt = [float(line.split('time=')[1].split(' ms')[0]) for line in lines if 'time=' in line]
        return {
            'host': host,
            'avg_rtt': sum(rtt)/len(rtt) if rtt else 0,
            'min_rtt': min(rtt) if rtt else 0,
            'max_rtt': max(rtt) if rtt else 0,
            'packet_loss': result.stdout.count('Request timeout') / count
        }
    return {'host': host, 'error': result.stderr}

# Frontend → Backend
frontend_result = ping_qos('backend.local')
backend_result = ping_qos('frontend.local')
print('Frontend → Backend:', frontend_result)
print('Backend → Frontend:', backend_result)
```

---

### 2. iperf3 QoS Test (Bandwidth, Jitter, One-Way RTT)
```python
import iperf3

def iperf_qos(server_host, port=5201, duration=10):
    client = iperf3.Client()
    client.duration = duration
    client.server_hostname = server_host
    client.port = port
    result = client.run()
    return {
        'tcp_bandwidth_mbps': result.sent_Mbps,
        'tcp_retransmits': result.retransmits,
        'jitter_ms': result.jitter_ms,
        'lost_percent': result.lost_percent,
        'one_way_rtt_ms': getattr(result, 'min_rtt', None)  # falls verfügbar
    }

# Backend → Frontend
iperf_result = iperf_qos('frontend.local')
print('iperf3 Backend → Frontend:', iperf_result)
```

---

### 3. One-Way RTT Test (Python UDP)
```python
import socket
import time

def one_way_rtt_test(server_ip, port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start = time.time()
    sock.sendto(b'ping', (server_ip, port))
    # Server muss Zeitstempel zurücksenden
    data, addr = sock.recvfrom(1024)
    server_time = float(data.decode())
    rtt = server_time - start
    return {'one_way_rtt_ms': rtt * 1000}
```

---

### 4. QoS Dashboard (NiceGUI/Eel)
```python
@eel.expose
def run_qos_tests():
    results = {
        'ping_frontend_backend': ping_qos('backend.local'),
        'ping_backend_frontend': ping_qos('frontend.local'),
        'iperf_backend_frontend': iperf_qos('frontend.local'),
        # ... ggf. one_way_rtt_test
    }
    return results

ui.button('QoS Test starten', on_click=lambda: run_qos_tests())
ui.aggrid([]).bind_data_from(run_qos_tests)
```

---

### Use-Cases
- Supabase Sync: Backend/Frontend Latency
- Scrapy: Bandbreite für Scraping
- Webcam OCR: One-Way RTT für Live-Stream

---

**Fragen/Feedback:**
- Weitere QoS-Test- oder Dashboard-Beispiele gewünscht?
