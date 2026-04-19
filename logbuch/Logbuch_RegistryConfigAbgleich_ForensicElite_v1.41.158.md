# Forensic Elite Workstation – Registry/Config Abgleich (v1.41.158)

## Zentrale Steuerung aller UI-Elemente

| UI Element / Einstellung   | Python Registry (ui_settings)         | Status                    |
|---------------------------|---------------------------------------|---------------------------|
| Header Höhe               | "header_height": 48                   | Zentral gesteuert         |
| Sub-Nav Höhe              | "sub_nav_height": 35                  | Zentral gesteuert         |
| Footer Höhe               | "footer_height": 48                   | Zentral gesteuert         |
| Sidebar Breite            | "sidebar_width": 250                  | Zentral gesteuert         |
| Sub-Nav Force             | "force_sub_nav_visible": True         | Zentral gesteuert         |
| Zen Mode Toggle           | "enable_zen_mode": True               | Zentral gesteuert         |
| Visibility Matrix         | "ui_visibility_matrix": { ... }       | Vollständig zentralisiert |

---

## Warum das wichtig ist

- **Single Source of Truth:** Änderungen in der Python-Konfiguration (z.B. `header_height`) wirken sich sofort auf CSS und JS aus – keine manuellen Anpassungen im Frontend nötig.
- **Fallback Safe-Mode:** Die Notfall-Registry im JS (`registry.config = { ... }` im catch-Zweig) greift nur, wenn das Python-Backend (Eel) komplett ausfällt. So bleibt das GUI immer sichtbar.
- **Matrix-Steuerung:** Die `ui_visibility_matrix` in der Python-Config (ab Zeile 390) definiert für jeden Modul-Tab (media, library, database etc.), ob Header, Sub-Nav und Footer sichtbar sind.

---

## Fazit
Die JS-Logik ist jetzt rein deklarativ und folgt ausschließlich den Vorgaben aus der zentralen `config_master.py`. Das ist der Forensic Elite-Standard für eine robuste, wartbare und auditierbare Architektur.
