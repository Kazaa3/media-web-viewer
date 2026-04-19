# Branch Architecture Registry: Vergleich Alt (BRANCH_MAP) vs. Neu (branch_architecture_registry)

## Vorher: BRANCH_MAP (Legacy)

Früher wurde die Branch-Logik über eine hartcodierte BRANCH_MAP in models.py oder main.py gesteuert. Beispiel:

```python
BRANCH_MAP = {
    "audio": ["audio_native", "audio_transcode"],
    "multimedia": ["audio_native", "audio_transcode", "video_native", "video_hd", "video_pal", "bilder"],
    "extended": ["video_iso", "epub"]
}
```
- Die Branches und ihre erlaubten Medientypen waren fest im Code verdrahtet.
- Änderungen erforderten Code-Anpassungen und Deployments.

## Jetzt: branch_architecture_registry (Zentral in config_master.py)

Heute wird die Branch-Logik zentral und flexibel über die Konfiguration gesteuert:

```python
"branch_architecture_registry": {
    "media": ["all", "audio_native", "audio_transcode"],
    "library": ["all", "audio_native", "audio_transcode", "video_native", "video_hd", "video_pal", "video_iso", "bilder"],
    "database": ["all", "video_iso", "epub"]
}
```
- Die Branches und ihre erlaubten Capability-IDs sind in GLOBAL_CONFIG (config_master.py) definiert.
- Änderungen sind sofort und ohne Code-Änderung möglich.
- Die Backend-Filterlogik liest die erlaubten Typen dynamisch aus der Registry und filtert strikt nach Branch.

## Vorteile der neuen Architektur
- **Zentrale Steuerung:** Alle Branches und deren Medientypen sind an einer Stelle konfigurierbar.
- **Flexibilität:** Neue Branches oder Medientypen können ohne Code-Änderung hinzugefügt werden.
- **Wartbarkeit:** Kein Risiko von Inkonsistenzen durch verteilte, hartcodierte Maps.
- **Strikte Trennung:** Die Sichtbarkeit und Filterung ist garantiert branch-spezifisch und konsistent.

**Status:**
- Die alte BRANCH_MAP ist entfernt.
- Die branch_architecture_registry ist die einzige Quelle für Branch-Logik im System.
