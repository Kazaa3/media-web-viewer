# Logbuch MS: Project-Aware Cleanup & Finalisierung v1.35.68

## Zusammenfassung
Der Plan für die Wiederherstellung und Finalisierung von v1.35.68 steht. Ziel ist es, den "Old Ghost" (verwaiste Prozesse auf Port 8345) zu beseitigen, die Versionierung zu synchronisieren und die neue Diagnostik-Suite sowie die automatische Hydrierung zu aktivieren.

## Umsetzungsschritte
1. **Environment Cleanup:**
   - Ausführen von super_kill.py, um alle verwaisten Backend-Prozesse zu beenden und Port-Konflikte zu vermeiden.
2. **Version Sync:**
   - Aktualisierung von main.py und options_panel.html auf den Stand der version.js (v1.35.68), um "Old Ghost"-Versionen zu verhindern.
3. **Diagnostic Hub:**
   - Integration der Echtzeit-Log-Steuerung und DOM Health Auditor-Toggles in main.py und Options-Panel (update_parser_config).
4. **Atomic Hydration:**
   - Implementierung eines Watchdogs in audioplayer.js, der die Warteschlange nach 5 Sekunden Leergang automatisch mit Medien befüllt.

## Offene Fragen vor Ausführung
- **Direkt-Scan:** Soll der Scan nach dem Backend-Neustart automatisch getriggert werden oder erst manuell über den neuen Sync-Button?
- **DOM Auditor HUD:** Sollen die Kalk-grünen Ränder des Health-Auditors in dieser Version standardmäßig aktiviert sein?

## Verifikation
- Alle Zombie-Prozesse werden entfernt, nur ein Backend-Instance bleibt aktiv.
- UI und Backend zeigen beide v1.35.68 an.
- Die Bibliothek ist mit echten Mediendateien befüllt.
- Logging- und Diagnostik-Controls sind im Options-Panel verfügbar.
- Die Player-Warteschlange bleibt dank Atomic Hydration nie leer.

## Status
- **Bereit:** Plan und Implementierungsschritte sind dokumentiert.
- **Warten auf:** User-Feedback zu Scan- und Auditor-Default-Einstellungen vor Ausführung von Schritt 1 (SuperKill).
