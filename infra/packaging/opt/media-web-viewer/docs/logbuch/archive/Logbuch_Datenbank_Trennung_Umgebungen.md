# Logbuch: Datenbank-Trennung der Umgebungen

## Ziel
Dokumentation der sauberen Trennung und Isolation der Datenbanken für Core-, Parser-, Testbed-, UI- und Build-Umgebungen im Media Web Viewer.

---

## Konzept
- Jede Umgebung nutzt eine eigene SQLite-Datenbank (z.B. media_library_core.db, media_library_parser.db, media_library_testbed.db)
- Keine Vermischung von Daten, Logs oder Metadaten zwischen den Umgebungen
- Eigene Konfigurationsdateien und Pfade pro Umgebung
- Testumgebungen nutzen Mock- oder Testdatenbanken

---

## Umsetzung
- Automatisierte Bereinigung und Migration (cleanup_legacy_databases())
- Zugriff nur über die jeweilige Umgebung (db.py, API)
- Backup- und Restore-Strategien für jede Datenbank
- Validierung und Monitoring der Isolation

---

## Alternative: Datenbank löschen statt migrieren/bereinigen

### Ansatz
- Statt Migration oder Bereinigung von Einträgen wird die Datenbank bei Bedarf komplett gelöscht und neu erstellt.
- Gilt für Test-, Parser-, UI- und Build-Datenbanken, wenn Isolation oder Fehler auftreten.

### Vorteile
- Absolute Isolation und saubere Umgebung
- Keine Altlasten, keine Konflikte durch alte Daten
- Schnell und einfach (besonders für Tests und Entwicklung)

### Nachteile
- Datenverlust, wenn keine Backups vorhanden
- Nicht geeignet für produktive Umgebungen mit wichtigen Daten

### Umsetzung
- Automatisiertes Löschen und Neu-Erstellen der Datenbank (z.B. via Skript oder db.py)
- Backup vor Löschung optional
- Dokumentation im Logbuch und Testprotokoll

### Status
- Löschen statt migrieren/bereinigen ist für Test- und Entwicklungsdatenbanken sinnvoll und wird empfohlen
- Für Core- und produktive Datenbanken weiterhin Migration/Bereinigung und Backup

---

## Resume: Bisherige Migration und Probleme

### Ausgangslage
- Ursprünglich wurden Datenbanken migriert und bereinigt, um Altlasten und Konflikte zu vermeiden.
- Migrationstools und Skripte (cleanup_legacy_databases()) wurden eingesetzt.

### Probleme
- Migration und Bereinigung waren fehleranfällig: Alt-Einträge, Inkonsistenzen, Konflikte blieben bestehen.
- Test- und Entwicklungsdatenbanken enthielten unerwünschte oder veraltete Einträge.
- Datenbankstruktur und Pfade waren nicht immer sauber getrennt.

### Erkenntnisse
- Für Test-, Parser-, UI- und Build-Umgebungen ist das Löschen und Neu-Erstellen der Datenbank meist effektiver und sicherer.
- Migration/Bereinigung ist nur für produktive Core-Datenbanken mit wichtigen Daten sinnvoll.
- Klare Trennung und Isolation der Datenbanken ist essenziell für saubere Workflows und Tests.

### Status
- Löschen statt migrieren/bereinigen wird für Test- und Entwicklungsdatenbanken empfohlen und umgesetzt.
- Migration/Bereinigung bleibt für Core- und produktive Datenbanken erhalten.
- Weitere Automatisierung und Monitoring sind geplant.

---

## Vorteile
- Maximale Isolation und Nachvollziehbarkeit
- Keine Konflikte oder Datenverluste durch parallele Nutzung
- Flexible Erweiterung und Skalierung (z.B. Multi-Standort, Docker)
- Einfache Backup- und Restore-Strategien

---

## Anforderungen für Tests zur Datenbank-Trennung und Schutzmechanismen

### Pflichtanforderungen
- Tests für Löschung, Neu-Erstellung, Migration und Bereinigung der Datenbank
- Validierung der Isolation: Keine Vermischung von Daten zwischen Umgebungen
- Fehlerhandling: Tests für fehlerhafte, inkonsistente und veraltete Einträge
- Backup- und Restore-Prozesse testen
- Automatisierte Tests für alle Schutzmechanismen

### Minimalanforderungen
- Testfälle für Löschung und Neu-Erstellung der Testdatenbank
- Validierung, dass nach Löschung keine Alt-Einträge mehr existieren
- Logging und Fehlerberichte bei fehlerhaften Daten

### Maximalanforderungen
- Tests für Multi-Standort- und Docker-Betrieb
- Automatisierte Regressionstests für alle Datenbankoperationen
- Integration in CI/CD Pipeline
- Tests für Backup, Restore und Monitoring

### Optionale Anforderungen
- Tests für Performance und Skalierbarkeit bei paralleler Nutzung
- Tests für Synchronisation und Export/Import von Daten
- Tests für Usability und Dokumentation der Schutzmechanismen

---

## Status
- Datenbank-Trennung ist geplant und teilweise umgesetzt
- Weitere Automatisierung und Validierung erforderlich

**Stand:** 12. März 2026

---

## Empfehlung: Schutzmechanismen testen solange unsaubere DB existiert

### Ziel
- Schutzmechanismen (Fehlerhandling, Isolation, Bereinigung, Backup) sollten explizit getestet werden, solange die Datenbank noch unsauber ist.
- Perfekte Testdaten und saubere DB sind erst nach erfolgreicher Validierung und Automatisierung sinnvoll.

### Vorgehen
- Testszenarien mit absichtlich fehlerhaften, inkonsistenten oder veralteten Einträgen durchführen
- Fehlerhandling, Logging, Bereinigung und Isolation validieren
- Backup- und Restore-Prozesse testen
- Automatisierte Tests für Migration, Löschung und Neu-Erstellung

### Vorteile
- Frühzeitige Erkennung und Behebung von Schwachstellen
- Robustere Schutzmechanismen und Workflows
- Nachweis, dass das System auch mit unsauberen Daten stabil und sicher bleibt

### Status
- Schutzmechanismen werden getestet, solange unsaubere DB existiert
- Nach erfolgreicher Validierung werden perfekte Testdaten und saubere DB genutzt
