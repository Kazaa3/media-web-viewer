# UI-Änderung: Video-Tab-Labeling & Struktur

**Datum:** 15.03.2026

## Änderung
- Der Tab für die Videowiedergabe heißt jetzt explizit "Video" (statt z. B. "VLC" oder generisch).
- Im HTML wurde der Bereich mit `<div id="vlc">` und verwandte Strukturen so angepasst, dass die Tab-Benennung und die UI-Logik klar und konsistent sind.
- Die einzelnen Player-Modi (VLC, Chrome Native, FFmpeg, Drag & Drop) sind jetzt klar als Unteroptionen im "Video"-Tab erkennbar und auswählbar.

## Ziel
- Einheitliche, sprechende Tab-Benennung für bessere Nutzerführung.
- Vermeidung von Verwirrung durch zu technische oder doppelte Tab-Namen.
- Klare Trennung zwischen Tab ("Video") und Player-Engine (VLC, Chrome, etc.).

## Ergebnis
- Der "Video"-Tab ist jetzt eindeutig als zentraler Einstiegspunkt für alle Videofunktionen erkennbar.
- Die Auswahl des gewünschten Players erfolgt innerhalb des Tabs, nicht über den Tabnamen selbst.
