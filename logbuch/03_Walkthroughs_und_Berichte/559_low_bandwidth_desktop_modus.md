# Logbuch: Low Bandwidth & Desktop Performance-Modi (2026-03-15)

**Datum:** 2026-03-15

## Feature-Idee: Low Bandwidth / 20 MB Modus
- **Ziel:** Effizientes Suchen und Browsen von Mediendateien auf langsamen Netzlaufwerken (z.B. WLAN-Verzeichnis).
- **Vorschlag:**
  - Limitierung der maximalen Lese-/Transfergröße pro Datei (z.B. 20 MB) beim Scannen und Seeken.
  - Optionale Vorschau/Metadaten-Extraktion nur auf die ersten X MB beschränken.
  - Fortschrittsanzeige und Warnung bei Überschreitung der Bandbreite.

## Feature-Idee: Desktop-Modus mit Performance-Stufen
- **Ziel:** Optimale Anpassung der Anwendung an verschiedene Desktop-Hardware (HDD, SSD, PCIe3, PCIe4).
- **Vorschlag:**
  - Auswahl des Modus im UI: "HDD", "SSD", "PCIe3", "PCIe4".
  - Je nach Modus werden Timeouts, Prefetch-Strategien und parallele Lesezugriffe angepasst.
  - Automatische Erkennung der Hardware möglich (z.B. via OS-API oder Benchmark beim Start).

## Vorteile
- Bessere Nutzererfahrung auf langsamen Netzwerken und älteren Systemen.
- Optimale Performance auf modernen Desktops mit schnellen SSDs/PCIe-Laufwerken.
- Flexible Anpassung an verschiedene Einsatzszenarien (z.B. Medienserver vs. Laptop im WLAN).

## Nächste Schritte
- Konzept im Team diskutieren und Anforderungen spezifizieren.
- Prototyp für Bandbreitenlimitierung und Hardwareerkennung entwickeln.
- UI-Optionen und Dokumentation vorbereiten.

---

*Letzte Änderung: 2026-03-15*
