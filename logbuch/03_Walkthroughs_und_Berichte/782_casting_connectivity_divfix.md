# Erweiterung: Casting-Tests, Backend-Diagnose & DIV-Fix (21.03.2026)

## 1. Neuer "📺 Casting"-Sub-Tab im Tests-Menü
- **Funktionen:**
  - Chromecast & DLNA Discovery: UI-Scanner ruft discover_cast_devices() im Backend auf, zeigt gefundene Geräte (IP, Name) an
  - SWYH-RS Bridge: Toggle für "Stream-What-You-Hear" (Rust), systemweites Audio-Redirect
  - Spotify Connect: Platzhalter für Spotify-Bridge (Raspotify/Librespot)
- **Backend:**
  - discover_cast_devices(), start_cast(), toggle_swyh_rs() als @eel.expose registriert und aus UI aufrufbar

## 2. Backend Reachability Diagnostic
- **Feature:**
  - "Backend Reachability"-Karte im Base Connectivity-View
  - Prüft gezielt, ob Eel-Server auf 127.0.0.1:8345 erreichbar ist
  - Bei Fehler: Kompakter Troubleshooting-Report (Firewall, Prozess, Port)

## 3. HTML-Struktur & DIV-Tag-Rework
- **Fix:**
  - 5 fehlende </div>-Tags ergänzt, Hauptcontainer vor Skriptende sauber geschlossen
  - JS-Fehler (u.a. bei Zeile 11171) durch saubere IIFE- und Event-Listener-Kapselung behoben
  - Layout- und CSS-Fehler ("fucked up") beseitigt

## Status & Nutzung
- Alle Sub-Tabs und Tests integriert
- DIV-Balance und Connectivity-Diagnose live
- Casting-Discovery: Tests → Casting → "Scan for Devices"
- Verbindungstest: Tests → Base → "Check 127.0.0.1"

---

**Nächste Schritte:**
- Casting-Discovery und Backend-Check im UI testen
- Weitere Streaming-Integrationen (Spotify, DLNA) vorbereiten
