# Bug-Logbuch: MediaItem Drag-and-Drop – .grab-icon nicht erreichbar

## Fehlerbeschreibung
Beim Drag-and-Drop von MediaItems im Web-Frontend tritt regelmäßig der Fehler auf, dass das Element `.grab-icon` nicht im DOM gefunden wird. Dies führt zu `NoSuchElementException` in den Selenium-Tests und verhindert das Verschieben von MediaItems.

---

### Symptome
- Drag-and-Drop-Test schlägt fehl: `.grab-icon` nicht erreichbar.
- 10x Robust Action Retry, keine Besserung.
- Playlist kann nicht per Drag-and-Drop sortiert werden.
- Up/Down-Buttons funktionieren als Alternative.

---

### Ursachenanalyse
- `.grab-icon` wird nicht immer im DOM erzeugt (z.B. leerer Playlist, falscher Zustand, Timing-Probleme).
- Drag-and-Drop-Logik ist auf `.grab-icon` angewiesen, aber nicht robust gegen fehlende Elemente.
- Up/Down-Buttons sind immer sichtbar und ermöglichen das Verschieben.

---

### Empfehlungen & Workaround
- Prüfen, ob `.grab-icon` zuverlässig im DOM ist, wenn MediaItems angezeigt werden.
- Drag-and-Drop-Logik im Frontend robuster gestalten (z.B. Fallback auf Up/Down-Buttons).
- Tests auf Up/Down-Buttons umstellen, um das Verschieben zu validieren.
- Fehlerhafte Testfälle und Screenshots dokumentieren.

---

### ToDos
- UI/Frontend-Code für `.grab-icon` und Drag-and-Drop überprüfen.
- Testfälle mit alternativen Move-Controls ausstatten.
- Nachbesserung und erneute Testausführung.

---

**Letzte Aktualisierung:** 12. März 2026
