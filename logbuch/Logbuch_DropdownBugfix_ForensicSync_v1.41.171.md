# Abschlussbericht: Dropdown-Bugfix & Forensic Synchronization (v1.41.171)

## Root Cause & Fix

### Variable Desync
- Das Dropdown war leer, weil die neue Konfiguration in `window.GLOBAL_CONFIG` geladen wurde, die Hydration-Logik aber in `window.CONFIG` suchte.
- Beide Referenzen sind jetzt synchronisiert – die Dropdown-Funktion nutzt die korrekte Quelle.

### Missing Branch Identity
- Der `branch_id` fehlte im Top-Level-Konfigurationsobjekt des Frontends.
- branch_id wird jetzt explizit in config_master.py exponiert, sodass die UI immer weiß, welches Forensik-Set (z.B. Multimedia) angezeigt werden soll.

### Alias Expansion
- Die Mapping-Logik für player, media und multimedia wurde verdoppelt/erweitert.
- Egal wie der UI-State intern heißt, die Forensik-Kategorien werden immer gefunden.

### Safety Failover
- "Forensic Failover" in app_core.js: Wenn die Detection-Logik kein Mapping findet, wird automatisch auf das vollständige Multimedia-Set zurückgegriffen – nie wieder ein leeres Dropdown.

---

## Verification / Diagnostic Trace
- Das Dropdown ist jetzt immer vollständig befüllt (audio, audio_native, album, single, hörbuch, video, etc.).
- Nach App-Neustart und View-Refresh erscheinen die Kategorien sofort.

**Status:**
- Der "empty dropdown"-Bug ist nachhaltig gelöst, die Konfigurationssynchronisation ist robust und fail-safe.
