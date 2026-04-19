# Logbuch: Bibliothek – Unterreiter "Datenbank" für Scraping-Daten

**Datum:** 26.03.2026

## Ziel
Integration eines neuen Unterreiters "Datenbank" in der Bibliothek, der als zentraler Speicher- und Verwaltungsort für Scraping-Daten dient.

---

## Konzept
- Erweiterung der Bibliotheksansicht um einen Tab "Datenbank".
- Zentrale Speicherung aller Scraping-Ergebnisse in einer eigenen Datenbanktabelle (z.B. `scraping_data`).
- Bereitstellung von API-Methoden zum Abrufen, Hinzufügen und Bearbeiten der Scraping-Daten.
- Frontend-Integration: Anzeige der Daten als Tabelle/Liste, ggf. mit Bearbeitungs- und Löschfunktion.

---

## Umsetzung
- **Frontend:**
  - Neuer Tab-Button "Datenbank" in der Bibliothek.
  - Panel zur Anzeige und Verwaltung der Scraping-Daten.
- **Backend:**
  - Neue Tabelle `scraping_data` in der Datenbank.
  - API-Methoden: `get_scraping_data`, `add_scraping_data`, `update_scraping_data`, `delete_scraping_data` (via Eel exposed).
- **Frontend-Logik:**
  - JS-Funktion zum Laden und Anzeigen der Scraping-Daten beim Öffnen des Tabs.
  - Optional: Formulare für neue Einträge und Bearbeitung.

---

## Status
Konzept und Grundstruktur stehen. Nächster Schritt: Implementierung der Datenbanktabelle und API, dann UI-Anbindung.

---

## Vorteile
- Zentrale, persistente Ablage aller Scraping-Daten.
- Einfache Verwaltung und Nachvollziehbarkeit.
- Erweiterbar für weitere Analyse- oder Exportfunktionen.

---

**Stand:** 26.03.2026
