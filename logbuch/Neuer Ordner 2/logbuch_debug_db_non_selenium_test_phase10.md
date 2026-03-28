# Logbuch: Debug & Datenbank – Non-Selenium Testintegration (Phase 10)

## Status: ToDo / Integration geplant

---

## Ziel
Die Debug & Datenbank-Ansicht ("Item DB (Übersicht)") soll regelmäßig im Rahmen der statischen Diagnostic Suite (non-Selenium) überprüft werden. Dies betrifft insbesondere die Anzeige und Integrität der Datenbank-Items und des Python-Item-Dictionaries.

---

## Empfehlungen zur Testintegration
- **Automatisierter Test:**
  - Prüfe, ob die Anzahl der Datenbank-Items (z.B. "Datenbank-Items:: 10") korrekt angezeigt wird.
  - Verifiziere, dass das Python Dict (Details) vollständig und fehlerfrei gerendert wird.
  - Stelle sicher, dass die Bibliothek (Media Items) das Item-Dictionary wie erwartet anzeigt (vor Übergabe an DB/Frontend).
- **Integration:**
  - Test in tests/engines/suite_ui_integrity.py oder einer dedizierten Debug-Diagnose-Suite implementieren.
  - Test sollte ohne Selenium (statisch, HTML/JS-Parsing) laufen.

---

*Dieses Logbuch dokumentiert die geplante Integration der Debug & Datenbank-Ansicht in die statische Diagnostic Suite für Phase 10.*
