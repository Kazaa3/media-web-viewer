# Walkthrough: Frequency-Master Steering & Refactored Hierarchy (v1.46.051)

Dieses Update hebt die PAL (50Hz) und NTSC (60Hz) Erkennung auf "Master Profile"-Status und ermöglicht eine granulare Orchestrierung, die Vorrang vor anderen Routing-Entscheidungen hat.

---

## 1. Frequency-Master Steering
- **frequency_steering**-Block in `config_master.py`:
    - PAL (50Hz): Kann gezielt auf einen Modus (z.B. mse) festgelegt werden, um optimale Synchronität zu gewährleisten.
    - NTSC (60Hz): Kann unabhängig gesteuert werden.
- Beispiel-Konfiguration:
```python
"frequency_steering": {
    "pal_50hz": "mse",    # FORCE PAL to MSE
    "ntsc_60hz": "auto"   # Standard-Heuristik
}
```

---

## 2. Flattened Decision Hierarchy
- Die Logik in `mode_router.py` wurde von einer verschachtelten 'else-if'-Struktur in eine flache, prioritätsgetriebene elif-Kette refaktoriert.
- Die Hierarchie ist jetzt strikt:
    1. Masters (Physical Media / ISO)
    2. Frequency Overrides (v1.46.051)
    3. Manual Overrides (Codec/Res)
    4. Policy Backups (HEVC HD)
    5. Heuristics (Standard Digital)
- Dies verbessert die Wartbarkeit und Nachvollziehbarkeit der Routing-Entscheidungen.

---

## 3. Enhanced Forensic Logging
- Jede Routing-Entscheidung enthält jetzt einen `Reason`-Key und wird mit vollem Kontext geloggt:
    - `[PLAY-PULSE] Final Routing: mse | Reason: Frequency Master Override (PAL -> mse) | Subtype: DVD-PAL-I`

---

## Verification
- **Konfiguration:**
    - Passe `config_master.py` an, um Frequency Overrides zu nutzen.
- **Test:**
    - Mit Mock-PAL/NTSC-Metadaten prüfen, dass die Frequency-Master-Logik greift und korrekt im Log erscheint.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
