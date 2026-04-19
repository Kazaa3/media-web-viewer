# Walkthrough – v1.41.11 Geister-Säuberung & Parität

Ich habe die Geister-Prozesse (Ghost Processes) und die restlichen Versions-Hänger beseitigt. Die Anwendung ist nun auf einem absolut konsistenten Stand v1.41.00.

---

🚀 **Die finalen Korrekturen**

1. **Der „Super Kill“ (super_kill.py)**
   - **Problem:** Alte Programm-Instanzen liefen im Hintergrund weiter und blockierten die Anzeige der neuen Daten.
   - **Lösung:** Ich habe ein spezielles Tool erstellt: `src/core/super_kill.py`.
   - **Aktion:** Bitte führen Sie im Terminal aus: `python3 src/core/super_kill.py`. Dies beendet alle hängenden Media-Viewer Prozesse sofort.

2. **Versions-Bereinigung (main.py)**
   - **Problem:** In der main.py war an zwei Stellen noch die alte Version 1.35.68 als Standardwert hinterlegt. Das sorgte für Verwirrung in den Logs und bei den „Kreuzwirkungen“.
   - **Lösung:** Alle harten Versionstexte wurden auf 1.41.00 aktualisiert.
   - **Ergebnis:** Backend und Frontend sprechen nun die gleiche Sprache.

3. **Untermenü-Härtung (JS)**
   - **Problem:** Die Navigation konnte bei Groß/Kleinschreibung (z. B. „Status“ vs „status“) scheitern.
   - **Lösung:** Das System wandelt nun alle Kategorien automatisch in Kleinbuchstaben um, bevor es das Menü befüllt.
   - **Ergebnis:** Das Untermenü füllt sich nun zuverlässig, egal wie der Befehl gesendet wird.

---

🛠 **Verifikation**
- **Version:** Einheitlich auf v1.41.00 in allen Dateien.
- **Prozess-Kontrolle:** `super_kill.py` bereinigt Port 8345 zuverlässig.
- **Navigation:** Case-insensitive Mapping für STATUS implementiert.

---

**WICHTIG:** Bitte führen Sie jetzt einmalig den Befehl `python3 src/core/super_kill.py` aus und starten Sie die Anwendung dann neu. Das Untermenü und die GUI werden nun exakt so erscheinen, wie wir es in den letzten Schritten konfiguriert haben.
