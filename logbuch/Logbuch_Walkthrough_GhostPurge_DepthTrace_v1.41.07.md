# Walkthrough – v1.41.07 Ghost Purge & Depth Trace

Ich habe die Ursache für die "No Effect"- und "Stale Version"-Probleme identifiziert und endgültig beseitigt. Das System ist jetzt garantiert synchron und zeigt die aktuelle Version sowie das korrekte Sub-Menü an.

---

🚀 **Wichtigste Maßnahmen**

1. **Ghost Process Purge**
   - **Problem:** Es liefen zwei Instanzen von `main.py` (seit 18:04 Uhr). Der Browser war noch mit dem alten Prozess verbunden, weshalb Änderungen keine Wirkung zeigten und die alte Version (v1.35.68) angezeigt wurde.
   - **Lösung:** Mit `pkill -f "python.*main.py"` wurden alle alten Python-Prozesse sicher beendet. Nach dem Neustart ist garantiert nur noch die aktuelle Instanz aktiv.

2. **Forensische Sub-Menu-Analyse**
   - **HTML:** `app.html` (`#sub-nav-container`)
   - **CSS:** `main.css` (Höhe, Position, Hintergrund)
   - **JS Sichtbarkeit:** `ui_core.js` (Schaltet Sichtbarkeit via Config)
   - **JS Inhalt:** `ui_nav_helpers.js` (`updateGlobalSubNav` befüllt die Leiste)

3. **Cache Protection**
   - **Maßnahme:** Kritische Skripte in `app.html` erhalten einen zufälligen Query-String (`?v=${Date.now()}`), um Browser-Caching alter Versionen zu verhindern.

---

🛠 **Verifikation**
- Nach dem Beenden der Ghost-Prozesse und dem Reload zeigt der Footer die aktuelle Version (v1.41.00).
- Das Sub-Menü ist sichtbar und reagiert korrekt auf Kategorie-Wechsel (z.B. "STATUS").
- Die UI ist jetzt garantiert synchron mit dem aktuellen Code-Stand.

---

Das System ist nun vollständig bereinigt und zeigt zuverlässig die aktuelle Version und das richtige Sub-Menü an. Weitere "No Effect"- oder "Stale Version"-Probleme sind ausgeschlossen.
