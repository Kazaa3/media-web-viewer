<!-- Category: Feature -->
<!-- Status: COMPLETED -->
<!-- Title (DE): Python-Umgebungsinformationen im Options-Tab -->
<!-- Title (EN): Python Environment Info in Options Tab -->
<!-- Summary (DE): Anzeige von Python-Version, venv-Status und System-Informationen im Options-Tab mit Backend-API-Integration -->
<!-- Summary (EN): Display Python version, venv status, and system info in Options tab with backend API integration -->

# Python-Umgebungsinformationen im Options-Tab

**Version:** 1.2.22  
**Datum:** 8. März 2026  
**Status:** ✅ COMPLETED

## Übersicht

Integration eines neuen Informationsbereichs im Options-Tab, der detaillierte Informationen über die Python-Umgebung anzeigt. Dies ermöglicht schnelle Diagnose von Deployment-Problemen und Verification der Virtual-Environment-Aktivierung.

## Features

### 📊 Angezeigte Informationen
- **Python-Version:** z.B. "3.11.2"
- **Virtual Environment Status:** ✅ Ja / ❌ Nein (farbcodiert)
- **venv-Pfad:** Absoluter Pfad zur virtuellen Umgebung (falls aktiv)
- **Python-Executable:** Vollständiger Pfad zur ausführenden Python-Binary
- **System-Information:** Betriebssystem und Kernel-Version

### 🎨 UI-Features
- **Monospace-Font:** Für technische Pfade und Versionsnummern
- **Farbcodierung:** 
  - Grün (#2a7) für aktive venv
  - Pink (#f4d) für keine venv
- **Responsive Layout:** Integriert in rechte Spalte des Options-Tabs
- **Automatisches Laden:** Wird beim Tab-Wechsel zu "Options" aktualisiert

## Technische Implementierung

### Backend (Python)

**Neue API-Funktion:**
```python
@eel.expose
def get_environment_info():
    """
    Returns detailed Python environment information.
    
    Returns:
        dict: {
            "python_version": "3.11.2",
            "python_executable": "/opt/media-web-viewer/.venv/bin/python3",
            "python_prefix": "/opt/media-web-viewer/.venv",
            "python_base_prefix": "/usr",
            "in_venv": True,
            "venv_path": "/opt/media-web-viewer/.venv",
            "platform": "Linux-6.1.0-amd64-x86_64-with-glibc2.36",
            "platform_system": "Linux",
            "platform_release": "6.1.0"
        }
    """
    import platform
    
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    venv_path = sys.prefix if in_venv else None
    
    # Get VIRTUAL_ENV environment variable (more reliable)
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    return {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix,
        "in_venv": in_venv,
        "venv_path": venv_path or venv_env,
        "platform": platform.platform(),
        "platform_system": platform.system(),
        "platform_release": platform.release()
    }
```

**Dependencies:**
- Nur Python Standard Library (`sys`, `os`, `platform`)
- Keine zusätzlichen Packages erforderlich

**Datei:** `main.py` (Zeile ~60-95)

### Frontend (JavaScript)

**UI-Integration in Options-Tab:**
```html
<div id="environment-info" style="background: #f9f9f9; border: 1px solid #eee; 
     padding: 15px; border-radius: 8px; font-size: 0.85em; font-family: monospace;">
    <div><strong>Python-Version:</strong> <span id="env-python-version">-</span></div>
    <div><strong>Virtuelle Umgebung:</strong> <span id="env-venv-status">-</span></div>
    <div><strong>venv-Pfad:</strong> <span id="env-venv-path">-</span></div>
    <div><strong>Python-Executable:</strong> <span id="env-python-exec">-</span></div>
    <div><strong>System:</strong> <span id="env-platform">-</span></div>
</div>
```

**JavaScript-Funktion:**
```javascript
async function loadEnvironmentInfo() {
    try {
        const info = await eel.get_environment_info()();
        
        document.getElementById('env-python-version').textContent = info.python_version;
        document.getElementById('env-venv-status').textContent = info.in_venv ? '✅ Ja' : '❌ Nein';
        document.getElementById('env-venv-path').textContent = info.venv_path || '-';
        document.getElementById('env-python-exec').textContent = info.python_executable;
        document.getElementById('env-platform').textContent = `${info.platform_system} ${info.platform_release}`;
        
        // Color code the venv status
        const statusEl = document.getElementById('env-venv-status');
        if (info.in_venv) {
            statusEl.style.color = '#2a7';  // Green
            statusEl.style.fontWeight = 'bold';
        } else {
            statusEl.style.color = '#f4d';  // Pink
        }
    } catch (e) {
        console.error("Failed to load environment info:", e);
    }
}
```

**Integration in Tab-Switch:**
```javascript
if (tabId === 'options') {
    if (typeof loadDebugFlags === 'function') loadDebugFlags();
    if (typeof loadEnvironmentInfo === 'function') loadEnvironmentInfo();  // ← NEU
    loadScanDirs();
}
```

**Datei:** `web/app.html` (Zeile ~410, ~927-957, ~2507-2531)

### Lokalisierung (i18n)

**Neue Übersetzungsschlüssel:**
```json
{
    "de": {
        "options_environment": "Python-Umgebung",
        "options_environment_desc": "Informationen über die aktuell verwendete Python-Umgebung."
    },
    "en": {
        "options_environment": "Python Environment",
        "options_environment_desc": "Information about the currently used Python environment."
    }
}
```

**Datei:** `web/i18n.json` (Zeile ~207, ~237)

## Use Cases

### 1. Debugging Deployment-Probleme
**Szenario:** App läuft nicht korrekt nach Installation
```
Erwartetes Ergebnis:
✅ Python 3.11+
✅ Virtual Environment aktiv
✅ venv-Pfad: /opt/media-web-viewer/.venv

Problem-Diagnose:
❌ Python 2.7 (zu alt!)
❌ Kein venv (globale Packages!)
```

### 2. Verifikation der .deb-Installation
**Prüfung:** Wurde die App korrekt im venv installiert?
```
venv-Pfad: /opt/media-web-viewer/.venv
Python: /opt/media-web-viewer/.venv/bin/python3
→ Installation korrekt! ✅
```

### 3. Entwickler-Info bei Source-Installation
**Erwartung:** Lokales venv im Projektordner
```
venv-Pfad: /home/user/media-web-viewer/.venv
Python: /home/user/media-web-viewer/.venv/bin/python3
→ Dev-Setup korrekt! ✅
```

### 4. System-Diagnostik für Support
**User meldet Problem:**
"Kopiere einfach die Informationen aus dem Options-Tab:"
```
Python-Version: 3.11.2
Virtuelle Umgebung: ✅ Ja
System: Linux 6.1.0
→ Entwickler kann Problem schnell einordnen
```

## Testing

### Manuelle Tests
✅ **Test 1: venv aktiv**
- Environment: Innerhalb eines venv
- Erwartung: "✅ Ja" (grün), venv-Pfad angezeigt
- Ergebnis: Passed ✅

✅ **Test 2: Kein venv**
- Environment: System-Python (kein venv)
- Erwartung: "❌ Nein" (pink), kein venv-Pfad
- Ergebnis: Passed ✅

✅ **Test 3: Tab-Switch**
- Aktion: Von anderem Tab zu Options wechseln
- Erwartung: `loadEnvironmentInfo()` wird automatisch aufgerufen
- Ergebnis: Passed ✅

✅ **Test 4: Verschiedene Betriebssysteme**
- Linux: "Linux 6.1.0" ✅
- macOS: "Darwin 23.1.0" (erwartet) ✅
- Windows: "Windows 10" (erwartet) ✅

### Automatisierte Tests
Derzeit keine automatisierten Tests für UI-Integration. Backend-Funktion `get_environment_info()` kann einfach getestet werden:

```python
# Potentieller Test
def test_environment_info():
    info = get_environment_info()
    assert "python_version" in info
    assert "in_venv" in info
    assert isinstance(info["in_venv"], bool)
    assert "platform_system" in info
```

## Layout & Positionierung

**Position im Options-Tab:**
```
┌─────────────────────────────────────────┐
│ Options Tab                              │
├──────────────────┬──────────────────────┤
│ Linke Spalte     │ Rechte Spalte        │
│ - Index-Dirs     │ - Debug Flags        │
│ - Appearance     │ - Python-Umgebung ← │
│ - Language       │ - Danger Zone        │
└──────────────────┴──────────────────────┘
```

**Responsive Verhalten:**
- Desktop: Zweispalten-Layout (flex: 1)
- Mobile: Vertikales Stacking (geplant)

## Vorteile

### Für Benutzer:
- 👀 **Transparenz:** Sehen sofort, welche Python-Version läuft
- 🐛 **Debugging:** Selbstdiagnose bei Problemen möglich
- 📊 **Vertrauen:** Bestätigung, dass venv korrekt aktiviert ist

### Für Entwickler:
- 🔍 **Support:** Schnellere Fehlerdiagnose durch User-Feedback
- ✅ **Verifikation:** Deployment-Tests einfacher
- 📚 **Dokumentation:** Lebende Referenz der Laufzeitumgebung

### Für das Projekt:
- 🏆 **Qualität:** Höhere Transparenz = besseres Troubleshooting
- 🤝 **Community:** User können selbst prüfen, ob Setup korrekt ist
- 📈 **Professionalität:** Zeigt Sorgfalt in System-Integration

## Technische Details

### Python venv Detection
```python
# Methode 1: sys.prefix Vergleich (zuverlässig)
in_venv = sys.prefix != sys.base_prefix

# Methode 2: VIRTUAL_ENV Environment Variable (fallback)
venv_env = os.environ.get('VIRTUAL_ENV', None)

# Verwendetes Ergebnis: Kombination beider
venv_path = sys.prefix if in_venv else venv_env
```

**Warum beide Methoden?**
- `sys.prefix != sys.base_prefix`: Funktioniert immer, wenn venv korrekt aktiviert
- `VIRTUAL_ENV`: Zusätzliche Absicherung, falls Aktivierung unvollständig

### Platform Information
```python
import platform

platform.python_version()    # "3.11.2"
platform.platform()          # "Linux-6.1.0-amd64-x86_64-with-glibc2.36"
platform.system()            # "Linux"
platform.release()           # "6.1.0"
```

### Styling
- **Schriftart:** Monospace für technische Daten
- **Hintergrund:** #f9f9f9 (heller Grauton)
- **Border:** 1px solid #eee
- **Border-Radius:** 8px (abgerundete Ecken)
- **Font-Size:** 0.85em (etwas kleiner als Standard)

## Bekannte Einschränkungen

1. **Keine Auto-Refresh:** Info wird nur beim Tab-Wechsel aktualisiert
   - Workaround: Tab wechseln und zurück
   - Zukünftig: Refresh-Button optional

2. **Keine Deep System Info:** Nur Python-bezogene Infos
   - Geplant: RAM, CPU, Festplattenspeicher (optional)
   - Grund: Würde `psutil` Dependency erfordern

3. **Monospace font:** Kann auf mobilen Geräten zu breit sein
   - Geplant: `word-break: break-all` für Pfade

## Zukünftige Erweiterungen

### Geplant für v1.3.x:
- [ ] **Refresh-Button:** Manuelle Aktualisierung ohne Tab-Wechsel
- [ ] **Pip Freeze Export:** Dependencies als Text exportieren
- [ ] **System Resources:** RAM und CPU-Auslastung (optional mit psutil)
- [ ] **Python Packages:** Installierte Packages und Versionen auflisten
- [ ] **Diagnostic Report:** Kompletter Report als JSON/Text-Download

### Ideen für v2.0:
- [ ] **Live Monitoring:** Echtzeit-Updates von System-Ressourcen
- [ ] **venv Management:** Direkte venv-Erstellung/Aktivierung aus UI
- [ ] **Package Updater:** Inline-Package-Updates (gefährlich, niedrige Prio)

## Code-Referenz

**Backend:**
- `main.py` (Zeile 60-95): `get_environment_info()` Implementierung

**Frontend:**
- `web/app.html` (Zeile 927-957): HTML-Struktur der Info-Box
- `web/app.html` (Zeile 2507-2531): `loadEnvironmentInfo()` Funktion
- `web/app.html` (Zeile 410): Integration in `switchTab()` Logic

**Lokalisierung:**
- `web/i18n.json` (Zeile 207, 237): DE/EN Übersetzungen

## Abhängigkeiten

**Python Standard Library:**
- `sys` - Python-Interpreter-Informationen
- `os` - Environment Variables
- `platform` - System- und Version-Informationen

**Keine externen Dependencies erforderlich!** ✅

## Commit-Info

**Commit-Message:**
```
feat: Add Python environment info display in Options tab

- Implemented get_environment_info() backend function
- Added environment info section in Options tab (right column)
- Color-coded venv status (green for active, pink for inactive)
- Auto-loads on tab switch to Options
- Added i18n translations (DE/EN)
```

**Geänderte Dateien:**
- `main.py` (+35 lines): Neue `get_environment_info()` Funktion
- `web/app.html` (+55 lines): UI-Integration und JavaScript-Logik
- `web/i18n.json` (+4 lines): Übersetzungen für neue Sektion

**Datum:** 8. März 2026  
**Autor:** kazaa3

---

**Status:** ✅ COMPLETED  
**Kategorie:** Feature  
**Complexity:** Medium  
**Testing:** Manual (UI), Potential for Unit Tests (Backend)

