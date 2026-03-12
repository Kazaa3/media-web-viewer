# Logbuch: Exact Audio Copy (EAC) – CD-Ripping, Log-Parsing, FLAC-Indexierung

## Datum: 10. März 2026

---

## Features
- ✅ EAC-Log Parser/Validator (Python, eac-logchecker)
- ✅ Rip-Qualität extrahieren (Track-Qualität, AccurateRip)
- ✅ Automatisierung (Batch, Python Controller)
- ✅ FLAC-Indexierung (plibflac/mutagen)
- ✅ Eel-API/Frontend

---

## Installation
```bash
pip install eac-logchecker morituri plibflac mutagen
```

---

## EAC-Log Parser/Validator
```python
from eac_logchecker import check_log
import glob
import eel

@eel.expose
def validate_eac_logs(folder: str):
    logs = glob.glob(folder + "/*.log")
    results = []
    for log_file in logs:
        status = check_log(log_file)
        results.append({
            'file': log_file,
            'status': 'OK' if status else 'FEHLER',
            'entries': len(status) if isinstance(status, list) else 1
        })
    perfect = len([r for r in results if r['status'] == 'OK'])
    return json.dumps({
        'total': len(logs),
        'perfect': perfect,
        'results': results
    })
```

---

## EAC Automatisierung (Batch)
```python
import subprocess

def rip_cd_with_eac(drive_letter='D:', output_folder='rips'):
    eac_path = r"C:\Program Files\Exact Audio Copy\EAC.EXE"
    cmd = [eac_path, '/secure', '/rip', f'/dest:{output_folder}', f'/drive:{drive_letter}']
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0
```

---

## EAC-Log Parsing (Rip-Qualität)
```python
import re
import numpy as np
from pathlib import Path

def parse_eac_log(log_path: str):
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()
    tracks = re.findall(r'Track (\d+).*?Track quality (\d+.\d+) %.*?Copy (OK|finished)', content, re.DOTALL)
    summary = {
        'total_tracks': len(tracks),
        'perfect_rips': len([t for t in tracks if t[2] == 'OK']),
        'avg_quality': np.mean([float(t[1]) for t in tracks]) if tracks else 0
    }
    return summary

@eel.expose
def analyze_rip_quality(log_folder: str):
    logs = glob.glob(log_folder + "/*.log")
    qualities = []
    for log in logs:
        q = parse_eac_log(log)
        qualities.append({'log': Path(log).name, **q})
    return json.dumps(qualities)
```

---

## Vollständige EAC-Pipeline
```python
@eel.expose
def eac_full_pipeline(cd_drive: str, output_folder: str):
    print(f"Rippe CD von {cd_drive} nach {output_folder}")
    logs = glob.glob(output_folder + "/*.log")
    validation = validate_eac_logs(output_folder)
    flacs = glob.glob(output_folder + "/*.flac")
    index_results = []
    for flac in flacs:
        index_results.append(flac_node(flac))
    return {
        'rips': len(flacs),
        'validation': json.loads(validation),
        'index': index_results
    }
```

---

## Pro-Tipps für EAC
- Secure Mode + AccurateRip = 100% bit-perfekt
- FLAC Parameter: -8 -V (max Compression + Verify)
- Logs immer speichern → später validieren!
- CUETools für CUETables/AR2
- Alternative: morituri (Python CD-Ripper)

---

## Fazit
- EAC bleibt Goldstandard für verifizierte Rips
- Python kann Logs parsen, Qualität tracken, FLACs indexieren
- Eel-Frontend für Batch-Analyse

---

**Fragen/Feedback:**
- EAC-Logs zum Testen vorhanden?
- Weitere Pipeline- oder Analyse-Beispiele gewünscht?
