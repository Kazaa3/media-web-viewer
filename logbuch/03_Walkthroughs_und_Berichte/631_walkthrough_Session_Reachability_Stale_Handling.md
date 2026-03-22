# Walkthrough – Session Reachability & Stale Session Handling

**Datum:** 17. März 2026

## Ziel
Verbesserung der Backend-Logik zur Erkennung, Überprüfung und Behandlung von inaktiven oder nicht erreichbaren (stale) Sessions.

---

### Status Quo (vor Änderung)
- Session-Reachability wird über `is_session_url_reachable(url, timeout, retries)` geprüft (HTTP-Request, Rückgabe bei Erfolg).
- Aktive Sessions werden mit `check_running_sessions()` (Prozess- und Port-Scan) ermittelt.
- Es existieren Ping-Endpunkte (`api_ping`, `ping`) für Latenz- und Erreichbarkeitsprüfungen.
- Keine explizite Logik zur Markierung oder Bereinigung von "stale" Sessions (Sessions, die nicht mehr erreichbar sind).

---

## Geplante/Umgesetzte Verbesserungen
- Periodische Reachability-Checks für bekannte Sessions (z.B. alle 30s).
- Markierung von Sessions als "stale", wenn sie mehrfach nicht erreichbar sind (z.B. 3x Timeout).
- Optionale automatische Bereinigung oder Benachrichtigung bei stale Sessions.
- Erweiterung der Session-API um Status-Flags (active, stale, unreachable).

---

## Verifikation
- Testfälle für laufende, beendete und künstlich blockierte Sessions.
- Überprüfung, dass stale Sessions korrekt erkannt und markiert werden.
- Sicherstellung, dass keine false positives bei kurzzeitigen Timeouts auftreten.

---

**Nächste Schritte:**
- Implementierung der periodischen Checks und Status-Flags in `main.py`.
- Optional: UI-Anzeige für stale Sessions und Backend-Benachrichtigungen.
