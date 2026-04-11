# Logbuch: Analyse- und Write-Mode – Konzept & Umsetzung

## Datum
16. März 2026

## Übersicht
Dieser Logbuch-Eintrag dokumentiert das Konzept und die Umsetzung der Analyse- und Write-Modi im Videoplayer.

---

## Analyse-Mode
- Funktion: Nur Check/Analyse der Mediendatei (z.B. ffprobe, Metadaten auslesen).
- Keine Änderungen an der Datei, reine Auswertung.
- UI: Button "Analyse" oder Modus-Auswahl.
- Ergebnis: Anzeige der Metadaten, Codec-Info, Dauer, Tags.

---

## Write-Mode
- Funktion: Überarbeiten/Bearbeiten der Tags einer Mediendatei.
- Tags werden im UI angezeigt und können editiert werden.
- Änderungen werden per API/Backend gespeichert (z.B. mit tag_writer).
- Sicherheit: Write-Mode nur für unterstützte Formate, Schutzmechanismen für ISO/MKV.
- UI: Button "Write" oder Modus-Auswahl, Editierfeld für Tags.

---

## Tests
- Analyse-Mode: Datei analysieren, Metadaten korrekt angezeigt, keine Änderungen.
- Write-Mode: Tags editieren, speichern, Änderungen werden übernommen.
- Schutz: Write-Mode für ISO/MKV blockiert oder mit Warnung.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe walkthrough.md für vollständige Details und Proof of Work.*
