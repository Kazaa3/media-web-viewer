# Hörbuch-GUI-Fix: Kein eigener Item-Typ

## Ziel
Hörbücher werden in der Media Web Viewer-GUI nicht als eigener Typ geführt, sondern wie andere Audio-Medien behandelt.

## Umsetzung
- Hörbücher erscheinen in den allgemeinen Medienlisten (Audio, Musik, etc.).
- Es gibt keinen separaten Tab oder Typ für Hörbücher.
- Filter und Sortierung ermöglichen gezielte Anzeige von Hörbüchern.
- Spezialbehandlung (z.B. Cover, Kapitel) erfolgt über Metadaten, nicht über einen eigenen Typ.

## Typfilterung für Hörbücher in der GUI

### Backend
- Beim Laden der Medienliste werden Metadaten (z.B. Genre, Albumtyp, Tags) ausgewertet.
- Hörbücher werden anhand typischer Merkmale (z.B. Tag "audiobook", Genre "Hörbuch") markiert.
- API liefert eine gefilterte Liste, wenn der Filter "Hörbuch" aktiv ist.

### Frontend (GUI)
- Checkbox oder Dropdown "Nur Hörbücher anzeigen" im Audio-Bereich.
- Beim Aktivieren des Filters wird die Medienliste neu geladen und nur Hörbücher angezeigt.
- Filter kann mit anderen Optionen kombiniert werden (z.B. Sortierung, Suche).

### Beispiel (Pseudo-Code)
```python
# Backend: Filterfunktion

def filter_audiobooks(media_list):
    return [item for item in media_list if 'audiobook' in item.tags or item.genre == 'Hörbuch']
```

```javascript
// Frontend: Filter-Checkbox
// <input type="checkbox" id="audiobook-filter"> Nur Hörbücher anzeigen

document.getElementById('audiobook-filter').addEventListener('change', function() {
    eel.get_media_list(this.checked ? 'audiobook' : null)(function(filteredList) {
        renderMediaList(filteredList);
    });
});
```

## Erweiterung: GUI-Option für Hörbücher

- Eine zusätzliche Filter-Option "Hörbücher" kann in der GUI angeboten werden.
- Diese Option filtert die Medienliste nach Metadaten (z.B. Genre, Albumtyp, Tags), um Hörbücher gezielt anzuzeigen.
- Kein eigener Tab, sondern als Filter/Checkbox im Audio-Bereich.
- Beispiel: Checkbox "Nur Hörbücher anzeigen" oder Dropdown "Medientyp: Hörbuch".
- Die Option nutzt vorhandene Metadaten und bleibt kompatibel mit der bestehenden Medienstruktur.

## Hinweise
- Backend und Parser-Pipeline behandeln Hörbücher wie andere Medien.
- GUI bleibt konsistent und übersichtlich.
- Erweiterungen für Hörbuch-spezifische Features erfolgen über Metadaten und Filter.

---
Letzte Aktualisierung: 11. März 2026
