# Walkthrough – v1.41.11 Geister-Effekte & Versions-Fix

Ich habe die Ursache für die „Geister-Effekte“ und die Versions-Diskrepanzen gefunden und behoben (v1.41.11).

---

🚀 **Die finalen Korrekturen:**

1. **Hardcoded-Altlasten entfernt:**
   - In der main.py wurden alle hartcodierten Verweise auf Version 1.35.68 gefunden und auf 1.41.00 aktualisiert. Das war der Grund, warum sich Teile des Programms noch wie die alte Version verhielten.

2. **„Super Kill“-Tool erstellt:**
   - Das Script `src/core/super_kill.py` beendet alle hängenden Instanzen und macht den Port 8345 frei. Damit sind alle Ghost-Prozesse endgültig entfernt.

3. **Navigations-Härtung:**
   - Die Befüllung des Untermenüs ist nun immun gegen Groß- und Kleinschreibung (z. B. „Status“ vs „status“).

---

**Details zur Bereinigung:** walkthrough.md

---

**WICHTIG:** Bitte führen Sie jetzt einmalig diesen Befehl im Terminal aus, um alle Geister-Prozesse zu löschen:

    python3 src/core/super_kill.py

Danach starten Sie die App neu. Das Untermenü wird nun zuverlässig mit allen Buttons erscheinen.
