# Logbuch: Perfect Video Player – Overhaul 6 & GUI Fixes (27.03.2026)

## Ziel
Die Mediathek wurde mit Stage 6 Features weiterentwickelt: umfassende Subtitle-/Audiotrack-Unterstützung, erweiterte Filtermöglichkeiten und Stabilitätsverbesserungen im GUI.

## Umsetzung

### Backend
- **main.py**: Erweiterte Filterlogik für Genre, Jahr und Qualität implementiert. `get_library` unterstützt jetzt serverseitige Pagination und dynamische Lade-Statistiken.
- **streams/mse_stream.py & hls_stream.py**: Sicherstellung, dass alle Audio- und Subtitle-Tracks korrekt gemappt und für das Umschalten im Player verfügbar sind.

### Frontend
- **app.html**:
  - Filterleiste um Jahr- und Genre-Filter (Dropdowns) sowie ein globales Suchfeld erweitert.
  - `renderLibrary` unterstützt jetzt alle neuen Filterzustände.
  - Video.js-Settings zeigen jetzt Sprachlabels und Codec-Infos für Audio-/Subtitle-Tracks an. Track-Umschaltung triggert Stream-Reload mit korrektem Index.
  - "Stats for Nerds" Overlay integriert jetzt die neuen Metadaten zu Audio- und Subtitle-Tracks.

### Testing
- **tests/gui/test_dynamic_loading.py**: Automatisierter GUI-Test (ohne Selenium) prüft dynamisches Rendering und "No Media"-Fallback.

## Verifikation
- Automatisierte Tests (`test_dynamic_loading.py`, `test_mode_router.py`) erfolgreich.
- Manuelle Prüfung: Track-Umschaltung, Filterfunktion, GPU-Auslastung und Direct Play (0% CPU) validiert.

## Fazit
Die Mediathek ist jetzt noch flexibler, stabiler und bietet eine moderne, filterbare und internationalisierte Benutzeroberfläche mit umfassender Hardware-Unterstützung.
