# TODO & Fehlerprotokoll: Casting & GUI-Tests (21.03.2026)

## 1. Fehler: Website nicht erreichbar (ERR_CONNECTION_REFUSED)
- **Symptom:**
  - Beim Start: "Die Website ist nicht erreichbar"
  - 127.0.0.1 hat die Verbindung abgelehnt (ERR_CONNECTION_REFUSED)
- **ToDo:**
  - Kompakter GUI-Test, der prüft, ob die App nach dem Start erreichbar ist (Port offen, HTTP-Status 200)
  - Test in die Integrity Suite aufnehmen

## 2. Casting: Neuer Unterreiter in Tests
- **ToDo:**
  - Eigenen Sub-Tab "Casting" im Tests-Bereich anlegen
  - Tests für Spotify, Chromecast, swyh-rs (Stream What You Hear)
  - Geräte-Discovery und Cast-Start via Backend-API testen

### Beispiel-API (Backend, @eel.expose):
- discover_cast_devices(): Findet Chromecast/DLNA-Geräte
- start_cast(device_id, media_url): Startet Cast
- toggle_swyh_rs(enabled): Aktiviert/Deaktiviert swyh-rs

## 3. Aktueller JS/UI-Fehler
- **Fehler:**
  - JS-Error in Zeile 11171 (div-Balance/DOM-Fehler)
  - UI-Layout "fucked up", benötigt Überarbeitung
- **ToDo:**
  - Div-Balance-Check und Fehlerprotokoll im Test-Tab ergänzen
  - Fehlerursache analysieren und beheben

---

**Nächste Schritte:**
- GUI-Test für Erreichbarkeit implementieren
- Casting-Sub-Tab und zugehörige Tests anlegen
- Div-Balance/UI-Fehler beheben und dokumentieren
