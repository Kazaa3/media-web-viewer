# Logbuch-Eintrag

Datum: 25.03.2026

## Fehlerbehebungen: isRepeat-Variable & Debug-Tab

### Zusammenfassung
- Fehler mit der isRepeat-Variable im Player-Logic behoben.
- Debug-Tab zeigt wieder Python Dict Details korrekt an.
- Dropdown-Übersetzungen und Update-Loop repariert.
- UX-Verbesserungen für Dict-Viewer.

### Details
1. **Repeat-Button & JS-Fehler (isRepeat)**
   - Variable vereinheitlicht: Alle Referenzen auf isRepeat umgestellt (vorher: is_repeat/repeatStatus-Mix).
   - Audio-Logik: onended-Handler prüft jetzt korrekt auf Repeat-Modus "one" mit isRepeat.

2. **Debug-Tab: Python Dict (Details)**
   - Fehlende ID debug-items-json wiederhergestellt, damit loadDebugLogs funktioniert.
   - i18n-Keys für Dropdown und Header ergänzt, Labels werden wieder korrekt angezeigt.
   - Update-Loop läuft wieder stabil, da das Ziel-Element im DOM existiert.

3. **UX-Verbesserungen**
   - Dict-Viewer nutzt jetzt Fira Code und pre-wrap für bessere Lesbarkeit.
   - Split-View im Debug-Tab bleibt bei 50/50.

### Ergebnis
- Player- und Debug-Tab sind wieder voll funktionsfähig und stabil.
- Verbesserte Lesbarkeit und Benutzererlebnis.

---

*Automatisch generierter Logbucheintrag zu den heutigen Bugfixes und UI-Verbesserungen.*
