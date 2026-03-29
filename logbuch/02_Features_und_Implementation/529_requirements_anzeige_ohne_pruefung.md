# Änderung: requirements.txt-Prüfung entfernt – Nur noch Anzeige

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert die Änderung, dass requirements.txt-Pakete nicht mehr automatisch im Backend geprüft oder abgeglichen werden. Stattdessen werden die Pakete nur noch im Optionen-Tab unter "venv" aufgelistet.

---

## 1. Bisheriges Verhalten
- Das Backend prüfte beim Start und/oder im Optionen-Tab, ob alle in requirements.txt gelisteten Pakete installiert sind.
- Fehlende Pakete wurden als "missing" angezeigt und ggf. mit Fehler gemeldet.
- Die Funktion `_get_requirements_status()` ermittelte installierte/fehlende Pakete und gab Status/Listen an das Frontend weiter.

---

## 2. Neues Verhalten (ab 15.03.2026)
- Die automatische Prüfung und der Abgleich mit requirements.txt entfallen komplett.
- Im Optionen-Tab unter "venv" wird nur noch die Liste der in requirements.txt aufgeführten Pakete angezeigt – ohne Statusprüfung.
- Es gibt keine Fehlermeldung oder Statusanzeige mehr zu fehlenden Paketen.

---

## 3. Motivation & Vorteile
- Reduziert Komplexität und potentielle Fehlerquellen im Backend.
- Verhindert unnötige Konsolen- oder UI-Fehlermeldungen bei optionalen/extern installierten Paketen.
- Die Verantwortung für das Installieren der Pakete liegt wieder klar beim Nutzer/der Entwicklerin.

---

## 4. Hinweise
- Die Änderung betrifft alle requirements.txt-Varianten (Haupt-, Infra-, Run-, Core-Requirements).
- Die Backend-Logik zur Paketprüfung kann entfernt/auskommentiert werden.
- Die UI zeigt weiterhin die Paketliste an, aber ohne Status.

---

**Siehe auch:**
- [Debug-Log-Level & Parser-Logging – Status & offene Fragen](2026-03-15_debug_log_level_status.md)
- [Shutdown/KeyboardInterrupt – Logbuch](2026-03-15_shutdown_keyboardinterrupt.md)
