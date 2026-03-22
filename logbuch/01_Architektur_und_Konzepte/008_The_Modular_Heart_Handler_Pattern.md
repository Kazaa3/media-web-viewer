# 03 The Modular Heart: Handler-Pattern

**Datum:** 13.03.2026
**Kategorie:** Architektur, Refactoring
**Status:** ARCHIVED

---

## Modularisierung & main.py als Orchestrator

Die App wuchs über das Skeleton hinaus. Die zentrale Herausforderung: Wie verwalten wir Dutzende von Medienformaten, ohne `main.py` in ein 10.000-Zeilen-Monster zu verwandeln?

### Die Geburtsstunde des Handler-Patterns
Wir haben die Logik aus der `main.py` in spezialisierte Module extrahiert:
- **`media_handler.py`:** Die Basis-Klasse für alle Verarbeitungs-Schritte.
- **`audio_handler.py` / `video_handler.py`:** Formatspezifische Sub-Klassen.
- **`metadata_pipeline.py`:** Der Orchestrator, der die verschiedenen Parser (mutagen, ffmpeg) in einer Kette aufruft.

### Orchestrierung
`main.py` fungiert jetzt nur noch als Dispatcher zwischen der Eel-Ebene und den spezialisierten Backend-Modulen. Dies ermöglicht es, neue Formate oder Parser hinzuzufügen, indem man einfach einen neuen Handler registriert, anstatt den Kerncode anzupassen.

---

**Kommentar:**
Dieses "Modulare Herz" ist der Grund, warum "dict" so einfach auf neue Medientypen (wie E-Books oder ISO-Images) erweitert werden konnte.
