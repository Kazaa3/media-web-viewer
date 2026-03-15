# Testklassifizierung: Webplayer & Backend

**Datum:** 15.03.2026

## Ziel
Systematische Einteilung aller Tests nach Typ, Ziel und Abdeckung für den Media Web Viewer.

---

## Testklassen & Kategorien

### 1. **Unit-Tests**
- **Ziel:** Einzelne Backend-Funktionen, Parser oder Hilfsfunktionen isoliert prüfen (z. B. Metadaten-Parser, Format-Erkennung, Model-Logik).
- **Ort:** `tests/unit/`, `tests/core/`, `tests/parsers/`
- **Beispiele:**
  - Metadaten-Parser (z. B. extract_metadata)
  - Format-Erkennung (VIDEO_EXTENSIONS, AUDIO_EXTENSIONS)
  - Datenbank-Modelle (MediaItem)

### 2. **Integrationstests**
- **Ziel:** Zusammenspiel mehrerer Backend-Komponenten, Datenbank und API-Endpunkte testen. Prüft, ob die Backend-Logik und Datenflüsse korrekt funktionieren.
- **Ort:** `tests/integration/backend/`, `tests/integration/ui/`
- **Beispiele:**
  - API-Endpunkte (z. B. get_library, save_tags_to_file)
  - Medienimport & Metadatenfluss
  - End-to-End-Tests mit Mock- und Realdateien

### 3. **UI-/Frontend-Tests**
- **Ziel:** Die grafische Benutzeroberfläche (GUI) des Webplayers automatisiert testen: Tab-Wechsel, Sichtbarkeit, Interaktionen, Medien-Playback, Fehlerfälle und Workflows. Simuliert echte Nutzeraktionen im Browser.
- **Ort:** `tests/integration/ui/`, ggf. `tests/e2e/`
- **Beispiele:**
  - Navigation zwischen allen Tabs (Player, Bibliothek, Browser, Edit, Optionen, Parser, Debug, Tests, Logbuch, Playlist, Video)
  - Klicks auf Buttons, Drag & Drop, Formular-Interaktionen
  - Medien-Playback (Audio/Video) und Steuerung (Play, Pause, Seek, Lautstärke)
  - Anzeige und Aktualisierung von Metadaten, Cover, Playlists
  - Fehler- und Edge-Case-Handling (z. B. nicht unterstützte Formate, leere Listen)

### 4. **System-/Environment-Tests**
- **Ziel:** Die technische Umgebung, Python- und Venv-Konfiguration, Systemtools und Abhängigkeiten prüfen. Stellt sicher, dass die App in verschiedenen Setups stabil läuft.
- **Ort:** `tests/environment/`, `tests/test_environment_packages_fallback.py`
- **Beispiele:**
  - Python-/Venv-Erkennung
  - Requirements-Status, Tool-Checks (ffmpeg, vlc, mediainfo)
  - Multi-Venv-Konzept

### 5. **Performance-/Robustheitstests**
- **Ziel:** Geschwindigkeit, Stabilität und Fehlerresistenz der gesamten Anwendung und der GUI unter Last und bei großen Datenmengen prüfen.
- **Ort:** `tests/test_performance_probes.py`, eigene Suiten
- **Beispiele:**
  - Medien-Scan großer Verzeichnisse
  - Playback-Stabilität bei vielen Dateien
  - Latenz- und Health-Checks (API, UI)

---

## Testabdeckung & Zuordnung
- **Jeder Tab und jedes Feature der grafischen Oberfläche** (siehe Feature-Testplan) wird durch Unit-, Integrations- und UI-Tests abgedeckt.
- **Backend-APIs**: Unit + Integration
- **Frontend/Player (GUI)**: UI + Integration
- **System/Umgebung**: Environment-Tests
- **Playback/Codecs**: Integration + UI + Performance

---

## Hinweise
- **Mock vs. Realdateien:** Für Playback/Parser werden beide Varianten genutzt.
- **Automatisierung:** Alle Tests laufen automatisiert (CI), kritische Pfade sind Gate-Tests.
- **Dokumentation:** Jeder Testtyp ist im Logbuch und in der Test-Suite dokumentiert.

---

## Testmatrix: Tabs, Features & Testarten

| Tab/Feature      | Unit-Test | Integration | UI/E2E | Env/System | Performance |
|------------------|:---------:|:-----------:|:------:|:----------:|:-----------:|
| Player           |     ✓     |      ✓      |   ✓    |            |      ✓      |
| Bibliothek       |     ✓     |      ✓      |   ✓    |            |      ✓      |
| Browser          |     ✓     |      ✓      |   ✓    |            |             |
| Edit             |     ✓     |      ✓      |   ✓    |            |             |
| Optionen         |     ✓     |      ✓      |   ✓    |     ✓      |             |
| Parser           |     ✓     |      ✓      |   ✓    |     ✓      |             |
| Debug            |           |      ✓      |   ✓    |     ✓      |             |
| Tests            |           |      ✓      |   ✓    |     ✓      |             |
| Logbuch          |           |      ✓      |   ✓    |            |             |
| Playlist         |     ✓     |      ✓      |   ✓    |            |             |
| VLC/Video        |     ✓     |      ✓      |   ✓    |     ✓      |      ✓      |

**Legende:** ✓ = Testart wird für Tab/Feature angewendet

Jede Zeile steht für einen Hauptreiter/Featurebereich der grafischen Oberfläche. Die Matrix zeigt, welche Testarten (Unit, Integration, UI/E2E, Environment/System, Performance) jeweils abgedeckt werden.

---

## Überblick: Tab- und Feature-Struktur der App

Der Media Web Viewer ist eine moderne Desktop- und Webanwendung zur Verwaltung und Wiedergabe von Mediendateien. Die App bietet eine übersichtliche, tab-basierte Benutzeroberfläche (GUI) mit folgenden Hauptbereichen:

- **Player:** Wiedergabe von Audio- und Videodateien, Steuerung (Play, Pause, Seek, Lautstärke, Shuffle, Repeat), Anzeige von Metadaten und Cover. Unterstützt verschiedene Playback-Engines (Browser, VLC, FFmpeg).
- **Bibliothek:** Übersicht und Verwaltung aller Medien, Filter- und Suchfunktionen, Anzeige von Details und Metadaten.
- **Browser:** Durchsuchen des Dateisystems, Hinzufügen neuer Medienverzeichnisse, Anzeige von Dateitypen und Icons.
- **Edit:** Bearbeiten von Metadaten, Umbenennen und Löschen von Medien, direkte Interaktion mit der Datenbank und den Dateien.
- **Optionen:** Konfiguration von Scan- und Library-Ordnern, App- und Parser-Modus, Debug-Flags, Anzeige von System- und Umgebungsinformationen.
- **Parser:** Verwaltung und Konfiguration der Metadaten-Parser-Kette, Anpassung parser-spezifischer Optionen.
- **Debug:** Anzeige von Logs, Systemstatus, Python- und DB-Informationen, Wechsel des Log-Levels.
- **Tests:** Ausführen und Anzeigen von Test-Suites, Testergebnissen und Logs.
- **Logbuch:** Dokumentation aller Änderungen, Features, Bugs und Testfälle, Filterung nach Kategorie und Status.
- **Playlist:** Erstellen, Bearbeiten und Abspielen von Playlists, Reihenfolge ändern, Shuffle, Speichern/Laden.
- **VLC/Video:** Erweiterte Videowiedergabe mit verschiedenen Engines (Browser, VLC, FFmpeg), Import/Export von VLC-Playlists, Drag & Drop.

Jeder Tab ist mit spezifischen Backend-APIs verbunden (z. B. Medienliste, Metadaten-Extraktion, Parser-Info, Debug-Logs, Test-Suites, Playback). Die Architektur ist modular, testbar und für Erweiterungen ausgelegt.
