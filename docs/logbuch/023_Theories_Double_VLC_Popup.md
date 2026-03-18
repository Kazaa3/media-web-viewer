## Logbuch Eintrag 023: Definitive Lösung für Double VLC Popups & UI Status

## Test-Verifizierung (18.03.2026 17:10)
Die Implementierung wurde durch automatisierte Integrationstests erfolgreich verifiziert.

### Testergebnisse (`test_dvd_image_handling.py`)
- `test_iso_file_routing`: **PASSED** (ISOs werden korrekt an VLC mit `dvd://` Prefix übergeben)
- `test_video_ts_folder_routing`: **PASSED** (VIDEO_TS Ordner werden als DVD erkannt und an VLC geroutet)
- `test_mpeg2_pal_fallback`: **PASSED** (MKVs mit MPEG-2 Codec triggern automatisch den VLC-Fallback)
- `test_debouncing_lock`: **PASSED** (Sperre von 2.0s verhindert erfolgreich Mehrfachstarts)

## Finale Architektur
- **Frontend**: Erkennt nun Kategorien (`movie`, `abbild`) als Video-Trigger.
- **Backend**: `open_video_smart` fungiert als intelligenter Gatekeeper mit Codec-Erkennung (PAL-Fix).
- **Subprozess-Management**: `start_vlc_guarded` erzwingt Singleton-Status via `pkill`.

Status: **COMPLETED**





 Logbuch Eintrag 023: Theorien zum doppelten VLC-Popup bei DVD-Objekten

## Datum: 2026-03-18
## Status: Research / Theory Phase

### Problemstellung
Beim Öffnen von DVD-Strukturen (ISO, VIDEO_TS, Mix-Ordner) öffnen sich auf dem System des Nutzers zwei VLC-Instanzen gleichzeitig, obwohl nur eine erwartet wird.

### 4 DVD-Objekt-Typen (nach Nutzerangabe)
1. **.iso Datei**: Einzelnes Image.
2. **Ordner mit Files**: Klassische VIDEO_TS Struktur.
3. **Ordner mit ISO und Film-Objekt**: Mischform (evtl. Sidecar-Files oder Metadaten-Objekte).
4. **Daten Image**: Rohes Disk-Image.

### Theorien zum "Double-Popup"

#### Theorie A: Overlapping Frontend Listeners
Obwohl ein `locking`-Mechanismus in JS implementiert wurde, könnten zwei verschiedene Events (z.B. ein `click` auf das Cover und ein `click` auf den Text) gleichzeitig feuern, wenn die DOM-Struktur verschachtelt ist und `stopPropagation()` fehlt.
*   *Status*: Teilweise durch Lock entschärft, aber bei extrem schnellen Events oder verschiedenen Event-Typen (mousedown vs click) noch möglich.

#### Theorie B: Backend-Fallback Loop
In `main.py` ruft `open_video_smart` am Ende `open_video` auf. Falls `open_video` wiederum einen Fallback auf `play_media` hat, könnte es zu einer Rekursion oder doppelten Ausführung kommen, falls die Rückgabewerte nicht sauber "verbraucht" werden.
*   *Status*: Code-Prüfung zeigt eigentlich saubere `return`-Ketten, aber Seiteneffekte in Sub-Funktionen (wie `open_with_vlc`) könnten existieren.

#### Theorie C: Multi-Format Detection
DVD-Ordner enthalten oft sowohl das Verzeichnis selbst als auch die darin liegenden Dateien. Falls der Parser für beide Einträge existiert, könnten zwei `play`-Befehle für das "gleiche" logische Objekt gefeiert werden (einmal für den Ordner, einmal für die erste .IFO/.ISO Datei).

#### Theorie D: VLC "dvd://" Prefix Redundanz
Wenn `open_video` erkennt, dass es ein DVD-Objekt ist, fügt es `dvd://` an. Falls VLC im System bereits so konfiguriert ist, dass es ISOs automatisch als DVD erkennt, und wir zusätzlich ein Subprocess-Argument mit dem Prefix schicken, könnte VLC intern eine zweite Instanz forken oder Eel triggert einen zweiten Call, weil der erste Call (mit Prefix) einen anderen Statuscode liefert als erwartet.

#### Theorie E: Mixed-Mode im open_video_smart
Für ISOs habe ich nun FragMP4 (Embedded) in `open_video_smart` aktiviert. Falls die Datenbank-ID gefunden wird, wird "play" (embedded) zurückgegeben. Falls *gleichzeitig* eine andere Logik (Fallback) greift, weil die ID vielleicht erst spät im Loop gefunden wird, könnten beide Pfade ausgeführt werden.

### Nächste Schritte
1.  **Trace-Logs prüfen**: Nutzer bitten, die `DEBUG: [Player-Trace]` Ausgaben des Terminals zu posten.
2.  **Explicit Mode Isolation**: Einführung von separaten Flags `cvlc`, `vlc`, `pyvlc` in den UI-Einstellungen, um die Pfade im Backend absolut zu trennen.
3.  **Folder-Play Safety**: Sicherstellen, dass bei Ordnern nur die Root-DVD-Funktion aufgerufen wird und keine Einzeldateien getriggert werden.



# Logbuch Eintrag 023: Theorien zum doppelten VLC-Popup bei DVD-Objekten

## Datum: 2026-03-18
## Status: Research / Theory Phase

### Problemstellung
Beim Öffnen von DVD-Strukturen (ISO, VIDEO_TS, Mix-Ordner) öffnen sich auf dem System des Nutzers zwei VLC-Instanzen gleichzeitig, obwohl nur eine erwartet wird.

### 4 DVD-Objekt-Typen (nach Nutzerangabe)
1. **.iso Datei**: Einzelnes Image.
2. **Ordner mit Files**: Klassische VIDEO_TS Struktur.
3. **Ordner mit ISO und Film-Objekt**: Mischform (evtl. Sidecar-Files oder Metadaten-Objekte).
4. **Daten Image**: Rohes Disk-Image.

### Theorien zum "Double-Popup"

#### Theorie A: Overlapping Frontend Listeners
Obwohl ein `locking`-Mechanismus in JS implementiert wurde, könnten zwei verschiedene Events (z.B. ein `click` auf das Cover und ein `click` auf den Text) gleichzeitig feuern, wenn die DOM-Struktur verschachtelt ist und `stopPropagation()` fehlt.
*   *Status*: Teilweise durch Lock entschärft, aber bei extrem schnellen Events oder verschiedenen Event-Typen (mousedown vs click) noch möglich.

#### Theorie B: Backend-Fallback Loop
In `main.py` ruft `open_video_smart` am Ende `open_video` auf. Falls `open_video` wiederum einen Fallback auf `play_media` hat, könnte es zu einer Rekursion oder doppelten Ausführung kommen, falls die Rückgabewerte nicht sauber "verbraucht" werden.
*   *Status*: Code-Prüfung zeigt eigentlich saubere `return`-Ketten, aber Seiteneffekte in Sub-Funktionen (wie `open_with_vlc`) könnten existieren.

#### Theorie C: Multi-Format Detection
DVD-Ordner enthalten oft sowohl das Verzeichnis selbst als auch die darin liegenden Dateien. Falls der Parser für beide Einträge existiert, könnten zwei `play`-Befehle für das "gleiche" logische Objekt gefeiert werden (einmal für den Ordner, einmal für die erste .IFO/.ISO Datei).

#### Theorie F: VLC Pathing and Protocol Conflict (`dvd://`)
Die Logs zeigen, dass VLC versucht, `dvd:///path/to/VIDEO_TS` zu öffnen und scheitert (`dvdnav demux error`). Das Protokoll `dvd://` erwartet oft das Device oder den Parent-Ordner. Wenn wir den Pfad falsch formatieren, könnte VLC abstürzen oder in einer Schleife versuchen, alternative Demuxer zu laden, was wie mehrere Fenster aussieht.

#### Theorie G: Triple VLC Presence
Das System verfügt über `pyvlc`, `vlc` und `cvlc`. Da diese teilweise unterschiedliche Pfad-Prioritäten oder Configs haben, könnten sie sich beim Öffnen von Protokollen wie `dvd://` gegenseitig triggern oder blockieren, falls ein "Default Player" für das DVD-Protokoll existiert.

### Nächste Schritte
1.  **VLC-Protokoll Pfad-Korrektur**: Pfad für DVD-Ordner auf den Parent-Ordner normalisieren.
2.  **Strict Mode Isolation**: "VLC Extern" als sauberen Fallback vom "Embedded" Mode trennen.
3.  **Kein Video ausgewählt**: Die Status-Meldung verbessern, wenn ein externer Player übernimmt.

# Logbuch Eintrag 023: Definitive Lösung für Double VLC Popups & UI Status

## Problem-Analyse (Status 18.03.2026 17:05)
Es kam weiterhin zu zwei VLC-Instanzen beim Öffnen von "Film-Objekten" (DVD-Ordner/ISO).
Zusätzlich blieb der Video-Player auf "Kein Video ausgewählt" stehen, obwohl VLC korrekt (aber doppelt) startete.

### Ursachen-Identifikation
1. **Deadlock in der Sperrlogik**: Der `open_video_smart` Router setzte eine Sperre und rief dann `open_video` auf. `open_video` sah die Sperre und blockierte sich selbst oder verhielt sich inkonsistent.
2. **Fehlende Instanz-Verfolgung**: Es gab keine eindeutige Zuordnung, welcher Code-Pfad welche VLC-Instanz gestartet hat.
3. **Frontend ID Mismatch**: Das JavaScript suchte nach einer ID `video-placeholder-message`, die im HTML gar nicht existierte. Daher konnte der Status "Externer Player aktiv" nie angezeigt werden.
4. **Race Condition im Parser**: Der `vlc_parser` (libvlc) startete im Hintergrund Instanzen zur Metadaten-Extraktion während der Wiedergabe-Trigger lief.

## Implementierte Lösungen

### 1. Hard-Reset Singleton-Pattern (`start_vlc_guarded`)
Jeder Start von VLC (egal ob direkt oder via Smart-Routing) durchläuft nun `start_vlc_guarded`.
- **Proaktiver Kill**: Vor jedem Start wird `pkill -9 -f vlc` ausgeführt. Dies garantiert, dass keine "Zombie"-Instanzen oder hängengebliebene Parser-Sessions überleben.
- **Instanz-Tagging**: Jede Instanz erhält eine ID wie `[smart_router_dvd|1234]`. Dies erlaubt im Log eine genaue Rückverfolgung: Wer hat den Prozess ausgelöst?

### 2. Deep Source Attribution
Die Funktionen `open_video` und `open_video_smart` akzeptieren nun ein `source` Argument.
- LOG-Meldung: `DEBUG: [Player-Trace] open_video called from smart_router_dvd for: ...`
- Dies verhindert "Bypass"-Starts über generische Funktionen wie `play_media`.

### 3. Frontend UI-Fix
Die HTML-Struktur wurde korrigiert:
- `<p id="video-placeholder-message" ...>` wurde hinzugefügt.
- Sobald VLC startet, zeigt der Player nun: **📺 Externer Player aktiv: VLC (DVD/ISO)**.

### 4. Parser-Isolation
Der VLC-Parser wurde für ISO- und DVD-Strukturen in `media_parser.py` deaktiviert, da `ffprobe` und `pymediainfo` für Basismetadaten ausreichen und die libvlc-Interferenz vermieden werden muss.

## Ergebnis
- **Ziel erreicht**: Nur noch 1 VLC Fenster.
- **Feedback**: Klarer Status im Browser-Tab statt "Kein Video ausgewählt".
- **H264 Fix**: Die "Black Screen" Problematik bei embedded MP4s wurde durch die Wiederherstellung des `PIPE-KIT` (Remux) Pfades gelöst.

# Logbuch Eintrag 023: Definitive Lösung für Double VLC Popups & UI Status

## Problem-Analyse (Status 18.03.2026 17:05)
Es kam weiterhin zu zwei VLC-Instanzen beim Öffnen von "Film-Objekten" (DVD-Ordner/ISO).
Zusätzlich blieb der Video-Player auf "Kein Video ausgewählt" stehen, obwohl VLC korrekt (aber doppelt) startete.

### Ursachen-Identifikation
1. **Deadlock in der Sperrlogik**: Der `open_video_smart` Router setzte eine Sperre und rief dann `open_video` auf. `open_video` sah die Sperre und blockierte sich selbst oder verhielt sich inkonsistent.
2. **Fehlende Instanz-Verfolgung**: Es gab keine eindeutige Zuordnung, welcher Code-Pfad welche VLC-Instanz gestartet hat.
3. **Frontend ID Mismatch**: Das JavaScript suchte nach einer ID `video-placeholder-message`, die im HTML gar nicht existierte. Daher konnte der Status "Externer Player aktiv" nie angezeigt werden.
4. **Race Condition im Parser**: Der `vlc_parser` (libvlc) startete im Hintergrund Instanzen zur Metadaten-Extraktion während der Wiedergabe-Trigger lief.

## Implementierte Lösungen

### 1. Hard-Reset Singleton-Pattern (`start_vlc_guarded`)
Jeder Start von VLC (egal ob direkt oder via Smart-Routing) durchläuft nun `start_vlc_guarded`.
- **Proaktiver Kill**: Vor jedem Start wird `pkill -9 -f vlc` ausgeführt. Dies garantiert, dass keine "Zombie"-Instanzen oder hängengebliebene Parser-Sessions überleben.
- **Instanz-Tagging**: Jede Instanz erhält eine ID wie `[smart_router_dvd|1234]`. Dies erlaubt im Log eine genaue Rückverfolgung: Wer hat den Prozess ausgelöst?

### 2. Deep Source Attribution
Die Funktionen `open_video` und `open_video_smart` akzeptieren nun ein `source` Argument.
- LOG-Meldung: `DEBUG: [Player-Trace] open_video called from smart_router_dvd for: ...`
- Dies verhindert "Bypass"-Starts über generische Funktionen wie `play_media`.

### 3. Frontend UI-Fix
Die HTML-Struktur wurde korrigiert:
- `<p id="video-placeholder-message" ...>` wurde hinzugefügt.
- Sobald VLC startet, zeigt der Player nun: **📺 Externer Player aktiv: VLC (DVD/ISO)**.

### 4. Parser-Isolation
Der VLC-Parser wurde für ISO- und DVD-Strukturen in `media_parser.py` deaktiviert, da `ffprobe` und `pymediainfo` für Basismetadaten ausreichen und die libvlc-Interferenz vermieden werden muss.

## Ergebnis
- **Ziel erreicht**: Nur noch 1 VLC Fenster.
- **Feedback**: Klarer Status im Browser-Tab statt "Kein Video ausgewählt".
- **H264 Fix**: Die "Black Screen" Problematik bei embedded MP4s wurde durch die Wiederherstellung des `PIPE-KIT` (Remux) Pfades gelöst.
