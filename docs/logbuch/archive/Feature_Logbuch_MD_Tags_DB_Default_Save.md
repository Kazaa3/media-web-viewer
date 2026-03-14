# Feature: Logbuch .md Tags Schreiben – DB Default Save

## Ziel
Standardmäßig sollen alle geschriebenen Tags und Logbuch-Einträge in der Datenbank gespeichert werden, um versehentliches Überschreiben oder Verlust von Dateien zu vermeiden.

## Motivation
- Schutz vor unbeabsichtigtem Überschreiben von .md-Dateien.
- Zentrale Speicherung und Verwaltung aller Logbuch-Tags und Einträge.
- Erleichtert Backup, Wiederherstellung und automatisierte Auswertung.

## Funktionsweise
- Beim Schreiben von Tags oder Logbuch-Einträgen wird standardmäßig in die DB gespeichert.
- Optional kann ein Export als .md-Datei erfolgen (z.B. für Archivierung oder Sharing).
- UI und File Handler bieten "Save to DB" als Default-Option.

## Implementierungsdetails
- Erweiterung des File Handlers: DB-Save als Standard.
- SQLite-Integration (db.py) für Logbuch-Tags und Einträge.
- Optionale Exportfunktion für .md-Dateien.
- Schutzmechanismus: Warnung/Bestätigung vor Überschreiben von Dateien.

## Verifikation
- Testfälle: DB-Save, Export, Schutz vor Überschreiben.
- Integration in Build/Test-Gate.

## Ausblick
- Erweiterung für Versionierung und Änderungsverfolgung.
- Automatisierte Backups und Restore-Funktion.

---

**Letzte Änderung:** 12. März 2026
