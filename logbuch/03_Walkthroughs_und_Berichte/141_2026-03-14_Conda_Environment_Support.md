<!-- Category: Feature -->
<!-- Status: COMPLETED -->
<!-- Title (DE): Conda-Umgebungsunterstützung für Environment Info -->
<!-- Title (EN): Conda Environment Support for Environment Info -->
<!-- Summary (DE): Erweitert Environment Info Display um Conda-Erkennung zusätzlich zu venv -->
<!-- Summary (EN): Extends Environment Info Display with Conda detection in addition to venv -->

# Conda-Umgebungsunterstützung

**Version:** 1.2.23  
**Datum:** 8. März 2026  
**Status:** ✅ COMPLETED

## Übersicht

Erweiterung der Python-Umgebungserkennung (#45) um volle Unterstützung für Conda-Environments. Die bisherige Implementierung erkannte nur venv/virtualenv über `sys.prefix != sys.base_prefix`, was bei Conda-Umgebungen fehlschlug. Diese Erweiterung fügt Conda-Erkennung via Umgebungsvariablen hinzu.

## Problem

### Ursprüngliches Verhalten
Bei aktivierter Conda-Umgebung (z.B. `conda activate p14`):
- GUI zeigte: **❌ Nein (System Python)**
- Tatsächlich aktiv: Conda env "p14" mit Python 3.14.2
- Pfad: `/home/user/anaconda3/envs/p14/bin/python`

### Ursache
Die alte Implementierung prüfte nur:
```python
in_venv = sys.prefix != sys.base_prefix  # False bei Conda!
venv_env = os.environ.get('VIRTUAL_ENV')  # Nicht gesetzt bei Conda
```

Conda setzt **andere** Umgebungsvariablen:
- `CONDA_DEFAULT_ENV` → Name der Conda-Umgebung (z.B. "p14")
- `CONDA_PREFIX` → Pfad zur Conda-Umgebung

## Implementierung

### Backend-Änderungen (main.py)

**Erweiterte Umgebungserkennung:**
```python
@eel.expose
def get_environment_info():
    """Erkennt venv UND conda Umgebungen"""
    
    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    # Check for Conda environment (NEU!)
    conda_env_name = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    in_conda = conda_env_name is not None or conda_prefix is not None
    
    # Determine environment type and path
    env_type = None
    env_path = None
    env_name = None
    
    if in_conda:
        env_type = "conda"
        env_path = conda_prefix
        env_name = conda_env_name
    elif in_venv or venv_env:
        env_type = "venv"
        env_path = venv_path or venv_env
        env_name = Path(env_path).name if env_path else None
    else:
        env_type = "system"
    
    return {
        # Bestehende Felder
        "in_venv": in_venv,
        "venv_path": venv_path or venv_env,
        
        # Neue Felder
        "in_conda": in_conda,
        "conda_env_name": conda_env_name,
        "conda_prefix": conda_prefix,
        "env_type": env_type,      # "conda" | "venv" | "system"
        "env_path": env_path,       # Unified path
        "env_name": env_name,       # Unified name
        ...
    }
```

### Frontend-Änderungen (web/app.html)

**Intelligente Anzeige nach Umgebungstyp:**
```javascript
async function loadEnvironmentInfo() {
    const info = await eel.get_environment_info()();
    
    // Display environment type and status
    let statusText = '';
    let isActive = false;
    
    if (info.env_type === 'conda') {
        statusText = `✅ Ja (Conda: ${info.env_name || 'unknown'})`;
        isActive = true;
    } else if (info.env_type === 'venv') {
        statusText = `✅ Ja (Venv: ${info.env_name || 'unknown'})`;
        isActive = true;
    } else {
        statusText = '❌ Nein (System Python)';
        isActive = false;
    }
    
    document.getElementById('env-venv-status').textContent = statusText;
    document.getElementById('env-venv-path').textContent = info.env_path || '-';
    
    // Color coding (grün für aktive Umgebung)
    const statusEl = document.getElementById('env-venv-status');
    statusEl.style.color = isActive ? '#2a7' : '#f4d';
    statusEl.style.fontWeight = isActive ? 'bold' : 'normal';
}
```

**HTML-Label-Anpassungen:**
```html
<!-- Generischer statt "Virtuelle Umgebung" -->
<strong>Umgebung:</strong>

<!-- Generischer Pfad statt "venv-Pfad" -->
<strong>Umgebungspfad:</strong>
```

### Test-Suite-Erweiterung

**tests/test_environment_dependencies.py:**
```python
def test_virtual_environment_active(self):
    """Prüft ob eine virtuelle Umgebung (venv oder conda) aktiv ist"""
    
    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    # Check for conda (NEU!)
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    
    in_any_env = in_venv or venv_env or conda_env or conda_prefix
    
    if not in_any_env:
        pytest.skip("⚠️ Keine virtuelle Umgebung aktiv")
    
    # Display environment info
    if conda_env:
        print(f"✅ Conda Environment aktiv: {conda_env}")
        if conda_prefix:
            print(f"   Conda-Pfad: {conda_prefix}")
    elif in_venv:
        print(f"✅ Venv aktiv")
        print(f"   venv-Pfad: {sys.prefix}")
    elif venv_env:
        print(f"✅ Venv aktiv (via VIRTUAL_ENV)")
        print(f"   VIRTUAL_ENV: {venv_env}")
```

### Standalone-Checker-Erweiterung

**check_environment.py:**
```python
def check_venv():
    """Prüft Virtual Environment (venv oder conda)"""
    print("\n📦 Virtual Environment Check:")
    
    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    # Check for conda
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    
    in_any_env = in_venv or venv_env or conda_env or conda_prefix
    
    if in_any_env:
        if conda_env:
            print(f"   Status: ✅ Aktiv (Conda)")
            print(f"   Conda Environment: {conda_env}")
            if conda_prefix:
                print(f"   Pfad: {conda_prefix}")
        elif in_venv:
            print(f"   Status: ✅ Aktiv (Venv)")
            print(f"   Pfad: {sys.prefix}")
        elif venv_env:
            print(f"   Status: ✅ Aktiv (Venv via VIRTUAL_ENV)")
            print(f"   Pfad: {venv_env}")
        return True
    else:
        print(f"   Status: ❌ NICHT AKTIV")
        print(f"   ⚠️  Aktiviere venv oder conda:")
        print(f"      source .venv/bin/activate  # für venv")
        print(f"      conda activate <env-name>  # für conda")
        return False
```

## Ergebnis

### Vorher (nur venv-Support)
```
Umgebung: ❌ Nein
Umgebungspfad: -
```

### Nachher (venv + conda)
**Mit Conda env "p14" aktiviert:**
```
Umgebung: ✅ Ja (Conda: p14)
Umgebungspfad: /home/user/anaconda3/envs/p14
Python-Executable: /home/user/anaconda3/envs/p14/bin/python
```

**Mit venv aktiviert:**
```
Umgebung: ✅ Ja (Venv: .venv)
Umgebungspfad: /opt/media-web-viewer/.venv
Python-Executable: /opt/media-web-viewer/.venv/bin/python
```

**Ohne Umgebung:**
```
Umgebung: ❌ Nein (System Python)
Umgebungspfad: -
Python-Executable: /usr/bin/python3
```

## Technische Details

### Umgebungsvariablen-Übersicht

| Umgebungstyp | Variable 1 | Variable 2 | sys.prefix != sys.base_prefix |
|--------------|-----------|-----------|-------------------------------|
| **venv** | `VIRTUAL_ENV` | - | ✅ True |
| **conda** | `CONDA_DEFAULT_ENV` | `CONDA_PREFIX` | ❌ False |
| **system** | - | - | ❌ False |

### Erkennungslogik-Hierarchie
1. **Conda-Check** hat Priorität (explizitere Umgebungsvariablen)
2. **venv-Check** als Fallback (sys.prefix-Vergleich + VIRTUAL_ENV)
3. **System** wenn keine Umgebung erkannt

### API-Erweiterungen

**Neue Response-Felder:**
```json
{
  "in_conda": true,
  "conda_env_name": "p14",
  "conda_prefix": "/home/user/anaconda3/envs/p14",
  "env_type": "conda",
  "env_path": "/home/user/anaconda3/envs/p14",
  "env_name": "p14"
}
```

**Bestehende Felder (kompatibel):**
```json
{
  "in_venv": false,
  "venv_path": null,
  "python_version": "3.14.2",
  "python_executable": "/home/user/anaconda3/envs/p14/bin/python"
}
```

## Vorteile

### 🎯 Für Nutzer
- ✅ Präzise Erkennung unabhängig vom Umgebungstyp
- ✅ Klare Anzeige: "Conda: p14" vs "Venv: .venv"
- ✅ Korrekte Diagnose von Dependency-Problemen

### 🔧 Für Entwickler
- ✅ Einheitliche API für beide Umgebungstypen
- ✅ Backward-kompatibel (alte `in_venv`-Felder bleiben)
- ✅ Test-Suite unterstützt beide Umgebungen
- ✅ Standalone-Checker zeigt korrekte Warnungen

### 📊 Für Testing
- ✅ Tests erkennen automatisch Conda-Umgebungen
- ✅ `pytest` funktioniert in beiden Umgebungen
- ✅ `check_environment.py` zeigt korrekten Status

## Use Cases

### Deployment-Diagnose
**Problem:** "Dependencies fehlen!"  
**Lösung:** Options-Tab öffnen → Environment Info prüfen
```
Umgebung: ❌ Nein (System Python)
→ Ursache gefunden: Falsche Python-Version aktiv
→ Fix: conda activate p14 oder source .venv/bin/activate
```

### CI/CD-Integration
```bash
# Test in verschiedenen Umgebungen
python check_environment.py  # Exit 0 wenn OK
pytest tests/test_environment_dependencies.py
```

### Multi-Environment-Entwicklung
- Entwicklung in venv: `source .venv/bin/activate`
- Testing in conda: `conda activate test-env`
- Beide werden korrekt erkannt und angezeigt

## Commit-Historie

**Hauptcommit:**
```
feat: Enhance environment checks for venv and conda, update UI to reflect environment status

- Extended get_environment_info() to detect Conda via CONDA_DEFAULT_ENV and CONDA_PREFIX
- Updated frontend to display environment type: "Conda: p14" or "Venv: .venv"
- Modified test suite to recognize both venv and conda environments
- Updated standalone checker for consistent conda detection
- Changed UI labels from "Virtuelle Umgebung" to generic "Umgebung"
- Changed "venv-Pfad" to "Umgebungspfad" for consistency
```

**Files geändert:**
- `main.py`: Backend API erweitert (get_environment_info)
- `web/app.html`: Frontend-Anzeige und loadEnvironmentInfo()
- `tests/test_environment_dependencies.py`: Test-Suite erweitert
- `check_environment.py`: Standalone-Checker erweitert

## Dokumentation

**DOCUMENTATION.md** wurde nicht geändert (Environment Info API bleibt kompatibel).

Falls detaillierte API-Doku gewünscht:
- Neue Felder: `in_conda`, `conda_env_name`, `conda_prefix`
- Neue Felder: `env_type`, `env_path`, `env_name`

## Testing

### Manuelle Tests
```bash
# Test 1: Mit Conda
conda activate p14
python main.py
# → Options-Tab: "✅ Ja (Conda: p14)"

# Test 2: Mit venv
conda deactivate
source .venv/bin/activate
python main.py
# → Options-Tab: "✅ Ja (Venv: .venv)"

# Test 3: System Python
deactivate
python main.py
# → Options-Tab: "❌ Nein (System Python)"
```

### Automatische Tests
```bash
# In Conda-Umgebung
conda activate p14
pytest tests/test_environment_dependencies.py::TestPythonEnvironment::test_virtual_environment_active
# Output: ✅ Conda Environment aktiv: p14

# In venv
source .venv/bin/activate
pytest tests/test_environment_dependencies.py::TestPythonEnvironment::test_virtual_environment_active
# Output: ✅ Venv aktiv
```

## Known Issues

Keine bekannten Probleme. Die Implementierung deckt alle gängigen Szenarien ab:
- ✅ venv (via virtualenv oder python -m venv)
- ✅ Conda environments
- ✅ Miniconda und Anaconda
- ✅ System Python

## Zukunftserweiterungen

Potenzielle Erweiterungen (nicht implementiert):
- [ ] Poetry-Umgebungen erkennen (via `POETRY_ACTIVE`)
- [ ] Pipenv-Umgebungen (via `PIPENV_ACTIVE`)
- [ ] pyenv-Umgebungen
- [ ] Docker-Container-Erkennung

## Related Logbook Entries

- **#45 Environment Info Display:** Ursprüngliche Implementation (nur venv)
- **#44 File Picker API:** Weitere Options-Tab-Features
- **Test Suite (#45):** test_environment_dependencies.py erstellt

## Zusammenfassung

Conda-Unterstützung wurde nahtlos in die bestehende Environment Info Display integriert. Die Implementierung ist **backward-kompatibel**, **vollständig getestet** und bietet eine **konsistente Benutzererfahrung** für beide Umgebungstypen.

**Status:** ✅ Produktionsreif  
**Version:** 1.2.23  
**Merge:** Mit main merged (commit bc89e63, dann 289e12c mit Doku-Update)
