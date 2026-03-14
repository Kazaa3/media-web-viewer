# Übersicht: Mock-Dateien für Parser- und File-Tests

Diese Dateien und Verzeichnisse dienen als Testdaten für die Entwicklung und Validierung der Parser- und File-Handling-Logik. Sie sind ausschließlich für automatisierte Tests und CI/CD bestimmt und enthalten keine urheberrechtlich geschützten Inhalte.

## Verzeichnisstruktur und Beispiel-Dateien

- **/media/archives/**
  - (Archivformate für Extraktionstests)
- **/media/Bilder/**
  - (Bildformate für Bildparser)
- **/media/disks/**
  - (Disk-Images für Mount-/ISO-Tests)
- **/media/DVD_FOLDER_TEST/**
  - VIDEO_TS/VIDEO_TS.IFO
  - VIDEO_TS/VTS_01_0.IFO
  - VIDEO_TS/VTS_01_1.VOB
- **/media/mock_files/**
  - (Ehemaliges Verzeichnis für Mock-Dateien, jetzt leer)
- **/media/Music/audiobook.m4b**
  - (Beispiel für Hörbuch-/Audio-Parser)
- **/media/Series/Staffel_1/**
  - (Serienstruktur für Video-/Episode-Tests)
- **/media/Videos/**
  - (Videoformate für Video-Parser)
- **/media/mock_movie.iso**
  - (ISO-Image für spezielle Mount-/Parser-Tests)

## Hinweise
- Alle Dateien dienen ausschließlich Test- und Entwicklungszwecken.
- Die Verzeichnisse können je nach Testfall gezielt befüllt oder geleert werden.
- Für neue Parser- oder File-Tests bitte die Struktur beibehalten und keine produktiven oder urheberrechtlich geschützten Medien verwenden.

---
Letzte Aktualisierung: 14.03.2026
