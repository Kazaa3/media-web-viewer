# Logbuch – v1.41.07 Geister-Heilung & Transparenz

Ich habe den entscheidenden Fehler gefunden: Es liefen zwei Instanzen von main.py gleichzeitig (seit 18:04 Uhr). Ihr Browser war mit dem alten Prozess verbunden, weshalb keine meiner Änderungen einen Effekt hatte und Sie immer noch die veraltete Version v1.35.68 sahen.

---

🛠 **Die „Geister-Heilung“ v1.41.07:**

- **Ghost Purge:**
  - Alle alten Python-Prozesse wurden hart beendet. Damit greift beim nächsten Start garantiert der neue Code.

- **Cache-Busting:**
  - In der app.html haben alle Scripte und CSS-Dateien einen Zeitstempel (`?v=...`) erhalten. Das zwingt den Browser, die Dateien neu zu laden und keine alten Versionen aus dem Cache zu verwenden.

- **Transparenz-Check:**
  - **Struktur:** web/app.html Zeile 190 (`#sub-nav-container`)
  - **Position:** web/css/main.css Zeile 178 (top: 55px, min-height: 30px)
  - **Inhalt:** web/js/ui_nav_helpers.js Zeile 682 (Funktion `updateGlobalSubNav`)

---

**Details zur Synchronisierung:** walkthrough.md

---

Bitte starten Sie die Anwendung jetzt neu. Sie sollten nun sofort die korrekte Version v1.41.00 und das reparierte Untermenü (besonders unter STATUS) sehen.
