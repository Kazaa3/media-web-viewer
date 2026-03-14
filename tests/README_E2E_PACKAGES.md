# E2E Package Display Tests - Dokumentation

## Übersicht

Diese Test-Suite validiert den vollständigen Datenfluss für die Package-Anzeige im Options-Tab der Media Web Viewer Anwendung.

## Test-Architektur

### 📦 Test-Dateien

```
tests/
├── test_e2e_packages_bidirectional_async.py  # Haupt-E2E-Tests (22 Tests)
├── test_e2e_packages_backend_to_frontend.py   # Backend→Frontend (unidirektional)
├── test_e2e_packages_frontend_to_backend.py   # Frontend→Backend (unidirektional)
├── test_e2e_packages_async_only.py            # Reine Async-Tests
└── test_e2e_packages_data_sources.py          # Multi-Source Mock-Tests
```

## Datenfluss-Richtungen

### 1️⃣ Backend → Frontend (Downstream)

**Pipeline:**
```
subprocess.run (pip)
    ↓
Backend Parser (_get_installed_packages)
    ↓
get_environment_info() [@eel.expose]
    ↓
JSON Response
    ↓
Frontend: await eel.get_environment_info()
    ↓
normalizeInstalledPackages()
    ↓
DOM Rendering (installed-packages-list)
```

**Datenquellen (mit Fallback-Chain):**
1. **pip_list_json** - `pip list --format=json` (primär)
2. **pip_list_columns** - `pip list --format=columns` (fallback 1)
3. **importlib_or_pkg_resources** - Python importlib/pkg_resources (fallback 2)
4. **conda_list** - Conda environment packages (zukünftig)
5. **poetry_lock** - Poetry lock file parsing (zukünftig)
6. **pipfile_lock** - Pipenv lock file (zukünftig)

**Getestete Aspekte:**
- ✅ Subprocess-Aufruf und Parsing
- ✅ Multi-Stage-Fallback-Mechanismus
- ✅ JSON/Columns Format-Parsing
- ✅ Error-Handling und Timeouts
- ✅ Quellen-Metadaten (`installed_packages_source`)
- ✅ Frontend-Normalisierung für multiple Formate
- ✅ DOM-Element-Population
- ✅ Package-Count-Display
- ✅ Source-Display für Debugging

### 2️⃣ Frontend → Backend (Upstream)

**Pipeline:**
```
User Interaction (Package Search Input)
    ↓
Event Listener (input/change)
    ↓
Frontend Filtering Logic
    ↓
Optional: Backend Request (force_refresh)
    ↓
Updated Data Rendering
```

**Getestete Aspekte:**
- ✅ Search Input Event-Binding
- ✅ Real-time Filtering (debounced)
- ✅ Force-Refresh-Parameter (bidirektional)
- ✅ Case-insensitive Search
- ✅ Version-Number-Search

### 3️⃣ Bidirektional (Full Round-Trip)

**Scenario:**
```
1. User öffnet Options Tab
2. Frontend: loadEnvironmentInfo() async
3. Backend: get_environment_info() execution
4. Backend: _get_installed_packages() mit Fallback
5. Response: {installed_packages, source, count}
6. Frontend: Normalisierung + Rendering
7. User: Suche eingeben
8. Frontend: Filtering + DOM Update
9. Optional: Force-Refresh bei leerer Liste
10. Backend: Re-execution mit force_refresh=True
```

**Getestete Aspekte:**
- ✅ Complete Flow-Simulation mit Mocks
- ✅ Datenstruktur-Konsistenz (Backend ↔ Frontend)
- ✅ Retry-Mechanismus bei leeren Packages
- ✅ Concurrent Async Calls

### 4️⃣ Async Operations

**Getestete Patterns:**
- ✅ `async function loadEnvironmentInfo()`
- ✅ `await eel.get_environment_info()`
- ✅ Try-Catch Error-Handling
- ✅ Promise Chain Integrität
- ✅ Concurrent Call Isolation
- ✅ Async Timeout Handling

## Mock-Strategien

### Backend Mocks

```python
# Subprocess Mock für pip JSON
mock_result = Mock()
mock_result.returncode = 0
mock_result.stdout = json.dumps([
    {"name": "bottle", "version": "0.12.25"},
    {"name": "Eel", "version": "0.16.0"}
])

with patch('subprocess.run', return_value=mock_result):
    # Test execution
```

### Frontend Simulation

```python
# JavaScript Normalization → Python Simulation
def normalize_packages(raw_packages):
    normalized = []
    if isinstance(raw_packages, list):
        for pkg in raw_packages:
            name = str(pkg.get("name") or "").strip()
            version = str(pkg.get("version") or "-").strip()
            if name:
                normalized.append({"name": name, "version": version})
    return normalized
```

## Datenquellen-Tests

### Format-Varianten

| Source | Format | Priority | Status |
|--------|--------|----------|--------|
| pip JSON | `[{"name": "pkg", "version": "1.0"}]` | 1 | ✅ Implemented |
| pip Columns | `Package    Version\npkg         1.0.0` | 2 | ✅ Implemented |
| importlib | Python Metadata | 3 | ✅ Implemented |
| pkg_resources | Legacy API | 3 | ✅ Implemented |
| conda list | JSON/YAML | - | 🔄 Future |
| poetry.lock | TOML | - | 🔄 Future |
| Pipfile.lock | JSON | - | 🔄 Future |
| requirements.txt | Text | - | 🔄 Future |

### Error-Szenarien

- ✅ Subprocess Timeout → Fallback
- ✅ JSON Parse Error → Fallback
- ✅ Empty Package List → Force-Refresh
- ✅ Invalid Backend Response → Error Display
- ✅ Missing DOM Elements → Graceful Degradation

## Test-Execution

```bash
# Alle E2E-Tests
pytest tests/test_e2e_*.py -v

# Nur bidirektionale Tests
pytest tests/test_e2e_packages_bidirectional_async.py -v

# Mit Coverage
pytest tests/test_e2e_*.py --cov=. --cov-report=html

# Einzelner Test
pytest tests/test_e2e_packages_bidirectional_async.py::TestE2EPackagesBidirectionalAsync::test_20_e2e_complete_flow_simulation -v
```

## Metriken (Stand: 9. März 2026)

### test_e2e_packages_bidirectional_async.py
- **Tests:** 22
- **Coverage:** Backend Parser, API, Frontend Normalization, DOM
- **Runtime:** 0.11s
- **Status:** ✅ Alle Tests bestehen

### Abdeckung nach Kategorie

```
Backend Parsing:         Tests 01-02  (2 Tests)
Backend API:             Tests 03-04  (2 Tests)
Frontend Async:          Tests 05-10  (6 Tests)
Error Handling:          Tests 11-13  (3 Tests)
Bidirektional:           Tests 14-19  (6 Tests)
E2E Flow:                Tests 20-22  (3 Tests)
```

## Code-Referenzen

### Backend
- **Datei:** `main.py`
- **Funktion:** `_get_installed_packages()` (Lines ~353-430)
- **API:** `get_environment_info(force_refresh=False)` (Lines ~188+)

### Frontend
- **Datei:** `web/app.html`
- **Funktion:** `normalizeInstalledPackages(rawPackages)` (Lines ~3088-3110)
- **Loader:** `loadEnvironmentInfo()` (Lines ~3112-3320)
- **Renderer:** `renderPackages(packages)` (Lines ~3322+)

## Erweiterungen (Roadmap)

### Phase 1: Multi-Source Support (✅ Basis vorhanden)
- [x] pip JSON/Columns
- [x] importlib/pkg_resources
- [ ] conda list integration
- [ ] poetry.lock parsing
- [ ] requirements.txt reading

### Phase 2: Advanced Testing
- [ ] UI Integration Tests mit Selenium
- [ ] Performance Tests (>1000 packages)
- [ ] Memory Leak Detection
- [ ] Race Condition Testing

### Phase 3: Real-World Scenarios
- [ ] Network Timeout Simulation
- [ ] Corrupted Package Database
- [ ] Mixed Environment (venv + conda)
- [ ] Permissions Issues

## Wartung

### Test-Updates bei Code-Änderungen

**Backend-Änderung (_get_installed_packages):**
→ Update: test_01, test_02, test_14, test_15, test_20

**Frontend-Änderung (normalizeInstalledPackages):**
→ Update: test_06, test_07, test_16, test_20

**API-Änderung (get_environment_info):**
→ Update: test_03, test_18, test_20

**Neue Datenquelle hinzufügen:**
1. Backend: Fallback-Chain in `_get_installed_packages()` erweitern
2. Backend: Neuen Source-String hinzufügen (z.B. `"conda_list"`)
3. Tests: Mock für neue Quelle in `test_e2e_packages_data_sources.py`
4. Tests: Fallback-Test in test_14 erweitern

## Debugging

### Test-Failures analysieren

```bash
# Verbose Output
pytest tests/test_e2e_*.py -vv

# Mit Print-Statements
pytest tests/test_e2e_*.py -s

# Einzelner Test mit Debugger
pytest tests/test_e2e_*.py::TestClass::test_name --pdb
```

### Häufige Probleme

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Regex Match Failure | HTML-Struktur geändert | Regex Pattern anpassen |
| Mock nicht wirksam | Import-Path falsch | Patch-String verifizieren |
| Async Test hängt | Await fehlt | Promise Chain prüfen |
| False Positive | Mock zu breit | Spezifischere Mock-Conditions |

## Kontakt & Maintenance

**Dokumentation:** `tests/README_E2E_PACKAGES.md`
**Summary:** `TEST_SUITE_SUMMARY.md` (Root)
**Kategorie:** UI / E2E / Async / Integration
**Letzte Aktualisierung:** 9. März 2026
