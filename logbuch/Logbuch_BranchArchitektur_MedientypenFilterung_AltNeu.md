# Branch-Architektur für Medientypen-Filterung: Alt (BRANCH_MAP) vs. Neu (branch_architecture_registry)

## Fokus: Medientypen-Filterung (Display- und Prozess-Branch)

**Nicht Thema:** Tab-Logik, UI-Navigation oder Submenüs – diese bleiben unverändert.

---

## Vorher: BRANCH_MAP (Legacy)

Die Filterung, welche Medientypen (z.B. Bilder, Audio, Video) im jeweiligen Prozess/Branch angezeigt oder verarbeitet werden, war fest im Code verdrahtet:

```python
BRANCH_MAP = {
    "audio": ["audio_native", "audio_transcode"],
    "multimedia": ["audio_native", "audio_transcode", "video_native", "video_hd", "video_pal", "bilder"],
    "extended": ["video_iso", "epub"]
}
```
- Die Branches steuerten, welche Items im jeweiligen Modus sichtbar/prozessiert wurden.
- Änderungen erforderten Code-Anpassungen.

---

## Jetzt: branch_architecture_registry (config_master.py)

Die Filterung, welche Medientypen pro Prozess/Branch angezeigt oder verarbeitet werden, ist jetzt zentral konfigurierbar:

```python
"branch_architecture_registry": {
    "media": ["all", "audio_native", "audio_transcode"],
    "library": ["all", "audio_native", "audio_transcode", "video_native", "video_hd", "video_pal", "video_iso", "bilder"],
    "database": ["all", "video_iso", "epub"]
}
```
- Die Backend-Filterlogik prüft für jeden Branch, welche Medientypen (z.B. "bilder") angezeigt oder verarbeitet werden dürfen.
- Änderungen sind sofort über die Konfiguration möglich, ohne Code-Anpassung.

---

## Vorteile der neuen Lösung
- **Zentrale Steuerung:** Medientypen-Filterung pro Prozess/Branch an einer Stelle.
- **Flexibilität:** Neue Medientypen oder Branches können einfach ergänzt werden.
- **Strikte Trennung:** Die Sichtbarkeit/Verarbeitung ist garantiert branch-spezifisch.

**Wichtig:**
- Die Tab-Logik und UI-Navigation bleiben davon unberührt und werden weiterhin separat gesteuert.
