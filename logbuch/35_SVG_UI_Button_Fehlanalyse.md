# SVG-Grafiken und UI-Knöpfe: Fehleranalyse und Verbesserungsansätze

## Problemstellung
- Einige SVG-Grafiken fehlen oder werden nicht korrekt geladen/angezeigt.
- Bestimmte UI-Knöpfe (Buttons) sind unwirksam, d.h. sie lösen keine Aktion aus oder sind nicht mit Funktionen verbunden.

---

## Ursachenanalyse
1. **SVG-Grafiken:**
   - Pfadfehler oder fehlende Dateien im web/assets/svg/ Verzeichnis.
   - Falsche Referenzierung im HTML/JS (z.B. <img src="...">, <object>, <svg>).
   - Build-/Packaging-Probleme: SVGs werden nicht in das Artifact übernommen.
   - Browser-Kompatibilität oder CORS-Probleme.

2. **Unwirksame Knöpfe:**
   - Fehlende Event-Handler (onclick, eel.expose, etc.).
   - Buttons im HTML ohne zugehörige JS-Funktion.
   - Fehlerhafte oder nicht initialisierte JS-Module.
   - UI-Logik nicht mit Backend-Funktionen verbunden.

---

## Verbesserungsansätze
- SVG-Grafiken:
  - Sicherstellen, dass alle SVGs im web/assets/svg/ vorhanden und korrekt referenziert sind.
  - Pfade im HTML/JS prüfen und ggf. anpassen.
  - Build-System (PyInstaller, deb) so konfigurieren, dass SVGs ins Artifact übernommen werden (hidden-imports, --add-data).
  - Fallback-Grafiken oder Platzhalter einführen.

- UI-Knöpfe:
  - Alle Buttons mit Event-Handlern versehen und mit Backend-Funktionen verbinden (z.B. via eel.expose).
  - JS-Initialisierung und Modul-Importe prüfen.
  - UI-Tests automatisieren (z.B. mit Selenium), um nicht funktionierende Buttons zu erkennen.
  - Unwirksame oder redundante Buttons entfernen oder klar als deaktiviert kennzeichnen.

---

## Update: Fonts-Ordner und Google Material Fonts

- Im web/ Verzeichnis wurde ein fonts/ Unterordner hinzugefügt.
- Google Material Fonts sind jetzt eingebunden und stehen für das UI zur Verfügung.
- SVG-Grafiken werden lokal im Projekt gehalten und nicht mehr extern geladen.
- Alle SVG-Referenzen im UI wurden auf lokale Pfade angepasst.

Vorteile:
- Einheitliches, modernes UI durch Material Fonts.
- Keine externen Abhängigkeiten für SVGs und Fonts.
- Bessere Performance und Zuverlässigkeit beim Laden der Assets.

---

## Weiteres Vorgehen
- Audit aller SVG-Referenzen und UI-Buttons im web/ Verzeichnis.
- Fehlerhafte oder fehlende SVGs nachpflegen.
- Event-Handler und Backend-Verbindung für alle Buttons sicherstellen.
- Dokumentation und Troubleshooting-Abschnitt in STYLE_GUIDE_WEB.md ergänzen.

---

**Letzte Aktualisierung:** 13. März 2026
