# Logbuch: Low Bandwidth & Desktop-Modus – Pfadauswahl per Path-Objekt (2026-03-15)

**Datum:** 2026-03-15

## Ergänzung: Auswahl über Path-Objekt
- **Feature:** Die Auswahl und Verwaltung von Verzeichnissen/Dateien für Low Bandwidth- und Desktop-Modus erfolgt über ein zentrales `Path`-Objekt (z.B. Python `pathlib.Path`).
- **Vorteile:**
  - Einheitliche, plattformübergreifende Behandlung von Pfaden (Windows, Linux, macOS)
  - Erleichtert Validierung, Zugriff und Manipulation von Netzwerk- und lokalen Pfaden
  - Ermöglicht gezielte Optimierungen (z.B. Erkennung von Netzlaufwerken, SSDs, etc.)
- **Umsetzungsvorschlag:**
  - Alle Dateizugriffe, Scans und Bandbreitenlimits werden über Methoden des Path-Objekts abgewickelt
  - UI bietet eine Pfadauswahl, die direkt mit dem Path-Objekt verknüpft ist (z.B. für Netzwerkverzeichnisse, lokale Ordner)
  - Erweiterbar für zukünftige Features wie Favoriten, zuletzt verwendet, etc.

## Ergebnis
- Die Pfadverwaltung ist robuster, flexibler und besser wartbar.
- Low Bandwidth- und Desktop-Modus profitieren von einer konsistenten Pfadlogik.

---

*Letzte Änderung: 2026-03-15*
