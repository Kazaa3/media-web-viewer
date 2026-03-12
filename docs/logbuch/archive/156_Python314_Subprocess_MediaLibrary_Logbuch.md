# Logbuch: Python 3.14.2 Subprocess Handler – Best Practices für Scrapy/iPerf/FFmpeg

## Datum: 10. März 2026

---

## Thema: Moderne Subprocess-Manager (async, realtime, error-handling) für Media-Library

### 1. Einfacher Handler (run)
```python
import subprocess

def safe_run(cmd, timeout=30, capture_output=True):
    try:
        result = subprocess.run(
            cmd,
            timeout=timeout,
            capture_output=capture_output,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Timeout'}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': e.stderr, 'code': e.returncode}
```

---

### 2. Realtime Output (async Popen)
```python
import subprocess
import asyncio
from typing import AsyncGenerator

async def stream_subprocess(cmd: list) -> AsyncGenerator[str, None]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded = line.decode('utf-8').rstrip()
        yield decoded
    await process.wait()
```

---

### 3. Subprocess Manager Class
```python
class SubprocessManager:
    def __init__(self):
        self.processes = {}
    async def run_named(self, name: str, cmd: list, timeout=60):
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        self.processes[name] = process
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
            return {
                'success': process.returncode == 0,
                'stdout': stdout.decode(),
                'stderr': stderr.decode()
            }
        except asyncio.TimeoutError:
            process.terminate()
            return {'error': 'Timeout'}
    def kill_all(self):
        for proc in self.processes.values():
            proc.terminate()
```

---

### Eel/Supabase Integration
```python
@eel.expose
async def run_scrapy_live(query):
    cmd = ['scrapy', 'crawl', 'amazon', '-a', f'query={query}']
    async for line in stream_subprocess(cmd):
        client.table('scrapy_log').insert({'line': line, 'timestamp': 'now()'}).execute()
        eel.live_log(line)()  # JS Callback
    return "Fertig!"
```

---

### Python 3.14 t-strings (zukünftig)
```python
subprocess.run(t"ping -c 3 {host}")  # Auto-split safe!
```

---

### Use-Cases
- Scrapy: Live-Output → Supabase
- iPerf: Network-Test realtime
- FFmpeg: MKV-Prozess monitor

---

**Fragen/Feedback:**
- SubprocessManager oder async stream bevorzugt?
- Weitere Subprocess- oder Monitoring-Beispiele gewünscht?
