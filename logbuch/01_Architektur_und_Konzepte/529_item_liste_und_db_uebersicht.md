# Logbuch: Item-Liste straffen & Item-DB Übersicht

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert die geplante Straffung der Item-Liste in der Anwendung und gibt eine Übersicht zur Item-Datenbank (Item DB).

---

## 1. Item-Liste straffen
- Die aktuelle Item-Liste ist zu lang und unübersichtlich.
- Ziel: Die Item-Liste soll übersichtlicher werden, z.B. durch Gruppierung, Filterung oder Reduktion auf relevante Einträge.
- Unter den Kategorien steht aktuell oft nichts (leere Kategorien).
- Vorschlag: Leere Kategorien ausblenden oder dynamisch nur gefüllte Kategorien anzeigen.

---

## 2. Item-DB (Übersicht)
- Die Item-Datenbank (Item DB) enthält alle Medien- und Dateieinträge, die im System verwaltet werden.
- Struktur:
  - Jedes Item besitzt Attribute wie Name, Typ, Kategorie, Pfad, Metadaten etc.
  - Die Item-DB ist die zentrale Quelle für die Anzeige und Verwaltung der Medienobjekte.
- Aktuell werden alle Items ungefiltert gelistet, was zu Unübersichtlichkeit führen kann.
- Ziel: Bessere Übersicht durch Filter, Kategorien, Suchfunktionen und ggf. Pagination.

---

## 3. Nächste Schritte
- Implementierung einer dynamischen Anzeige: Nur Kategorien mit Einträgen werden angezeigt.
- Optionale Filter/Suchfunktionen für die Item-Liste.
- Dokumentation und UI-Update nach Umsetzung.

---

**Siehe auch:**
- [Debug-Log-Level & Parser-Logging – Status & offene Fragen](2026-03-15_debug_log_level_status.md)
- [requirements.txt-Anzeige ohne Prüfung – Logbuch](2026-03-15_requirements_anzeige_ohne_pruefung.md)
