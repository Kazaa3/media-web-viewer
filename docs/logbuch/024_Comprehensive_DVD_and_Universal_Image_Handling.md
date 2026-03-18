# Logbuch Eintrag 024: Umfassendes DVD- und Universal-Image Handling (V1.35)

## Datum: 2026-03-18
## Status: COMPLETED / VERIFIED

### Zielstellung
Nach hartnäckigen Problemen mit doppelten Player-Instanzen und inkompatiblen DVD-Formaten (MPEG-2 PAL) im Browser wurde eine neue, gehärtete Wiedergabe-Architektur implementiert. Ziel war es, "Film-Objekte" (Ordner ohne Endung), ISO-Abbilder und binäre Disk-Images konsistent und in einer einzigen Instanz wiederzugeben.

---

### Implementierte Kern-Komponenten

#### 1. Singleton VLC-Guard (`start_vlc_guarded`)
Um das "Double-Popup" Problem final zu lösen, wurde ein proaktives Prozess-Management eingeführt:
- **Proaktive Terminierung**: Vor jedem Start eines externen Players wird ein `pkill -9 -f vlc` ausgeführt. Dies verhindert, dass hängende Parser-Prozesse oder alte Instanzen koexistieren.
- **Deep Tracing**: Jeder Startvorgang wird mit einer `instance_id` und der `source` (z.B. `smart_router_dvd`) getaggt. Dies ermöglicht im Logbuch eine exakte Rückverfolgung: Wer hat den Prozess ausgelöst?
- **stdout/stderr Isolation**: Subprozesse werden nun mit `DEVNULL` gestartet, um Terminal-Interferenzen zu minimieren.

#### 2. Smart Router mit Codec-Awareness (`open_video_smart`)
Der Router entscheidet nun dynamisch zwischen "Embedded" und "Gezieltem Fallback":
- **MPEG-2 PAL Fix**: Browser (Chrome) können MPEG-1/2 nativ nicht dekodieren. Der Router erkennt diesen Codec nun in MKV-Containern und leitet sie automatisch an VLC weiter, anstatt einen "Black Screen" im Browser zu riskieren.
- **Universal Image Support**: Unterstützung für `.iso`, `.bin` und DVD-Ordnerstrukturen (`VIDEO_TS`) wurde konsolidiert.
- **Mix-Objekt Erkennung**: Ordner, die Filme als ISO-Sidecar enthalten, werden nun korrekt als DVD-Struktur erkannt.

#### 3. Frontend "Firewall" & UI Sync
Die Wiedergabe-Logik in `app.html` wurde gehärtet:
- **Kategorie-Aware Trigger**: Items der Kategorien `movie` oder `abbild` werden nun IMMER als Video erkannt, auch wenn sie keine Dateiendung haben (Ordner-Objekte).
- **Audio-Firewall**: Die Backend-Funktion `play_media` (Audio) weist nun Video-Pfade explizit ab, um Bypässe zu verhindern.
- **Status feedback**: Die UI-ID `video-placeholder-message` wurde korrigiert. Der Nutzer sieht nun sofort den Status: `📺 Externer Player aktiv: VLC (DVD/ISO)`.

---

### Verifizierung durch Integrationstests
Ein neuer Test-Suite `tests/integration/category/video/test_dvd_image_handling.py` wurde erstellt und deckt folgende Szenarien ab:
- **Test 1**: `.iso` Datei-Routing (VLC-Force).
- **Test 2**: `VIDEO_TS` Ordner-Strukturen (Automatische Erkennung).
- **Test 3**: MPEG-2 (PAL) MKV Fallback (Codec-basierte Entscheidung).
- **Test 4**: Debouncing / Locking-Mechanismus (Vermeidung von Mehrfach-Clicks).
- **Test 5**: BIN-Images und Mix-Ordner (Umfassende Image-Erkennung).

### Fazit
Mit der Version 1.35 verfügt der Media-Web-Viewer über eine industrietaugliche Handhabung von Disk-Images. Der "Double VLC Popup" Bug wurde durch die Kombination aus Frontend-Härtung, Backend-Firewall und Singleton-Prozess-Guard dauerhaft eliminiert.

**Dokumentation**:
- [main.py](file:///home/xc/%23Coding/gui_media_web_viewer/src/core/main.py): Zentrale Routing-Logik.
- [app.html](file:///home/xc/%23Coding/gui_media_web_viewer/web/app.html): Event-Handling und UI-Status.
- [test_dvd_image_handling.py](file:///home/xc/%23Coding/gui_media_web_viewer/tests/integration/category/video/test_dvd_image_handling.py): Verifizierungsskript.
