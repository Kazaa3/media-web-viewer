# Walkthrough - Navigation & Hydration Hardening (Media Viewer)

## Zusammenfassung
Die Navigation und Hydrierung des Media Viewers wurden weiter gehärtet, um die gemeldeten Unstimmigkeiten (Sidebar sichtbar, fehlende Untermenüs, schwarzes Hauptfenster) zu beheben.

---

## Durchgeführte Korrekturen

### Sidebar-Reset (Ausgetoggelt)
- Die Sidebar ist im Forensic Window Manager und in `app_core.js` standardmäßig auf geschlossen (`sidebarVisible = false`) gesetzt.
- Der Backend-Handshake wurde angepasst: Lokale Präferenzen haben Vorrang, die Sidebar springt nicht mehr ungefragt auf.

### Untermenü-Restaurierung (Global & Lokal)
- Die Visibility Matrix in `ui_nav_helpers.js` wurde gehärtet.
- Für die Kategorie `media` (Audio Player) sind Master Header und Contextual Sub-Nav jetzt fest als sichtbar definiert.
- Der WindowManager triggert bei jeder Fenster-Aktivierung einen Sichtbarkeits-Refresh, sodass die Menüleisten immer passend zum Inhalt erscheinen.

### Beseitigung des Black-Screen (Queue-Fragmente)
- Ein dedizierter Activation Hook im WindowManager für den Audio Player ruft beim Aktivieren explizit `switchPlayerView('warteschlange')` auf.
- Dadurch wird sichergestellt, dass das Fragment (Artwork, Metadaten, Warteliste) nicht nur im DOM existiert, sondern auch aktiv gerendert wird.

---

## Überprüfung der Hydrierung
- Im HYD-Tab (Forensik-Seitenleiste) können Sie den Status verfolgen.
- Beim Start des Audio Players sollten folgende Schritte als "SUCCESS" markiert sein:
  - `player` (Hauptfenster)
  - `player_queue.html` (Fragment-Hydrierung)
  - `warteschlange` (Sub-View Aktivierung)

---

Bitte Anwendung neu laden: Die Sidebar ist jetzt standardmäßig geschlossen und der Audio Player erscheint direkt mit allen Bedienelementen und Artwork.
