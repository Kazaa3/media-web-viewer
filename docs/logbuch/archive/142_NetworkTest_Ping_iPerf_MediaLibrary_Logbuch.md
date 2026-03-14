# Logbuch: Ping + iPerf Netzwerk-Test für Media-Library

## Datum: 10. März 2026

---

## Thema: Netzwerk-Diagnose (Supabase/Scrapy/OpenClaw) – Python Subprocess + iperf3-lib

### Installation
```bash
pip install iperf3 subprocess32
sudo apt install iperf3
```

---

### 1. Ping Test
```python
import subprocess
import platform
import asyncio

async def ping_host(host, count=4):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, str(count), host]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        rtt = [float(line.split('time=')[1].split(' ms')[0]) for line in lines if 'time=' in line]
        return {
            'host': host,
            'success': True,
            'avg_rtt': sum(rtt)/len(rtt) if rtt else 0,
            'min_rtt': min(rtt) if rtt else 0,
            'max_rtt': max(rtt) if rtt else 0
        }
    return {'host': host, 'success': False, 'error': result.stderr}

# Test
print(asyncio.run(ping_host('supabase.co')))
print(asyncio.run(ping_host('8.8.8.8')))
```

---

### 2. iPerf3 Bandbreite Test
```python
import iperf3

def iperf_test(server_host, port=5201, duration=10):
    client = iperf3.Client()
    client.duration = duration
    client.server_hostname = server_host
    result = client.run()
    return {
        'tcp_bandwidth_mbps': result.sent_Mbps,
        'tcp_retransmits': result.retransmits,
        'jitter_ms': result.jitter_ms,
        'lost_percent': result.lost_percent
    }

# Server starten (anderes Terminal)
# iperf3 -s -p 5201

print(iperf_test('localhost'))
```

---

### 3. Voll-Netzwerk-Diagnose
```python
async def full_network_test(hosts=['supabase.co', '8.8.8.8', '1.1.1.1']):
    results = []
    for host in hosts:
        ping_result = await ping_host(host)
        iperf_result = iperf_test(host) if ping_result['success'] else {'error': 'Ping failed'}
        results.append({**ping_result, **iperf_result})
    client.table('network_tests').insert(results).execute()
    return results

@eel.expose
async def test_network():
    return await full_network_test()
```

---

### NiceGUI Network Dashboard
```python
ui.button('Netzwerk Test starten', on_click=lambda: asyncio.create_task(test_network()))
network_table = ui.aggrid([])

async def update_network():
    data = client.table('network_tests').select('*').order('created_at').limit(10).execute()
    network_table.clear()
    network_table.add_rows(data.data)
ui.timer(5.0, update_network)
```

---

### Output Beispiel
- supabase.co: avg RTT 45ms, TCP 250Mbps
- 8.8.8.8: avg RTT 22ms, TCP 950Mbps

---

### Use-Cases
- Scrapy Speed: Bandbreite prüfen
- Webcam OCR: RTT für Live-Stream
- Supabase Sync: Latency Monitor

---

**Fragen/Feedback:**
- iperf3 server auf NAS oder Supabase Ping bevorzugt?
- Weitere Netzwerk-Test- oder Dashboard-Beispiele gewünscht?
