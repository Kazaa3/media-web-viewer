# Picking-UX: Best Practices für Drag & Drop in der Playlist

## Ziel
Die Picking-UX (Drag & Drop) in der Playlist soll intuitiv, robust und visuell klar sein. Nutzer können Items einfach greifen, verschieben und an gewünschter Position ablegen.

## Best Practices
- **Greif-Icon:** Klar erkennbares Icon (z.B. ☰) für Drag & Drop, nur dort aktiv.
- **Hover-Effekt:** Item hebt sich beim Überfahren mit der Maus hervor.
- **Drag-Feedback:** Während des Ziehens wird das Item visuell "mitgenommen" (z.B. Schatten, Transparenz).
- **Drop-Zone:** Zielposition wird deutlich markiert (z.B. Linie, Highlight).
- **Reihenfolge-Update:** Nach dem Drop wird die Playlist sofort aktualisiert.
- **Tab-Wechsel:** Picking-Status wird beim Tab-Wechsel zurückgesetzt, keine "hängenden" Items.
- **Touch-Support:** Drag & Drop funktioniert auch auf Touch-Geräten.
- **Fehlerhandling:** Ungültige Drops werden abgefangen, Item bleibt an alter Position.

## Workflow
1. Item mit Maus oder Touch greifen (click-and-hold)
2. An gewünschte Position ziehen
3. Drop-Zone erscheint, Item ablegen
4. Reihenfolge wird aktualisiert, UI refreshed

## Status
- Picking-UX im Media Web Viewer dokumentiert
- Verbesserungen iterativ umsetzen und testen

---
Letzte Aktualisierung: 11. März 2026
