# Tag-Scanner & Barcodes für neue Media Items

## 1. Zielsetzung
Für die effiziente Erfassung und Verwaltung neuer Media Items im System wird ein Tag-Scanner-Workflow mit Barcode-Unterstützung eingeführt. Dies ermöglicht eine schnelle, fehlerarme Zuordnung und Inventarisierung von Medienobjekten.

## 2. Funktionsweise
- **Tag-Scanner:**
  - Erfasst Metadaten (z.B. Titel, Künstler, Album, Jahr) automatisch beim Hinzufügen neuer Medien.
  - Nutzt bestehende Parser (z.B. ffprobe, mutagen) zur Extraktion von Dateiinformationen.
- **Barcode-Unterstützung:**
  - Medien können mit Barcodes (z.B. EAN, QR) versehen werden.
  - Beim Scannen eines Barcodes wird das zugehörige Media Item im System gesucht oder neu angelegt.
  - Barcode kann als eindeutiger Schlüssel für physische Medien (CDs, DVDs, Bücher) dienen.

## 3. Vorteile
- Beschleunigte und automatisierte Medienerfassung
- Reduzierung von Tippfehlern und Dubletten
- Verbesserte Nachverfolgbarkeit und Inventarisierung
- Einfache Integration in bestehende Workflows (z.B. UI, API)

## 4. Umsetzungsideen
- Integration eines Barcode-Scanner-Moduls in die UI (z.B. per Webcam oder USB-Scanner)
- Erweiterung der MediaItem-Modelle um Barcode-Feld
- Automatische Verknüpfung von Barcode und Metadaten beim Import
- Optionale Validierung gegen externe Datenbanken (z.B. MusicBrainz, Discogs)

## 5. ToDo
- Barcode-Feld in Datenmodell und DB ergänzen
- UI-Workflow für Barcode-Scan und Tag-Import implementieren
- Dokumentation und Beispiel-Workflows im Logbuch ergänzen

---

**Hinweis:**
Die Barcode- und Tag-Scanner-Funktionalität ist besonders für physische Medienarchive, Bibliotheken und größere Sammlungen relevant, kann aber auch für digitale Medien zur eindeutigen Identifikation genutzt werden.
