# Logbuch: Modularization Phase 1 – Library API Extraction

## Ziel
Reduktion des Kontextdrucks im Backend durch Auslagerung der Bibliothekslogik aus main.py in ein eigenes Modul.

---

## Maßnahmen
- **api_library.py**
    - Extraktion von get_library, get_library_audit_summary und apply_library_filters (vormals _apply_library_filters) aus main.py.
    - apply_library_filters wird exportiert, um von anderen Modulen (z.B. Reporting) genutzt zu werden.
- **main.py**
    - Importiert die Bibliotheksfunktionen aus api_library.py und exponiert sie via @eel.expose.
    - Entfernt die monolithische Bibliothekslogik.
- **Forensische Hygiene**
    - 0-Byte-Altdateien media_library.db und media_viewer.db gelöscht.

---

## Verifikation
- Eel-Bridge-Check: Bibliotheksfunktionen funktionieren weiterhin.
- SCAN/Refresh löst [FE-AUDIT]-Logs aus.
- Kein ReferenceError mehr in isAudioItem.

---

*Letztes Update: 18.04.2026*
