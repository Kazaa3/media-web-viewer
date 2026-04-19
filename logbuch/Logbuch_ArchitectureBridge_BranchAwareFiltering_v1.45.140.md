# Full-Stack Architecture Bridge: Branch-Aware Filtering (v1.45.140)

## Zielsetzung
Synchronisierung der Backend-Filterlogik in models.py und main.py mit den branch-spezifischen Einstellungen aus config_master.py. Ziel ist eine zentrale, konsistente Steuerung der Sichtbarkeit und Filterung aller Medientypen pro Branch.

## Änderungen & Komponenten

**[Component] BACKEND: MODELS REFACTOR (v1.45.140)**
- MASTER_CAT_MAP in models.py enthält jetzt alle granularen Stufen (z.B. audio_native, video_hd) und nutzt die SSOT-Constants aus config_master.py.
- Die alte, hardcodierte BRANCH_MAP wurde entfernt.
- Die Funktion audit_category_chain unterstützt jetzt capability-basierte IDs.

**[Component] BACKEND: FILTERING ENGINE BRIDGE**
- get_library_filtered akzeptiert einen neuen Parameter active_branch.
- Die erlaubten Typen für den Branch werden aus GLOBAL_CONFIG (branch_architecture_registry) geholt und an die Filterlogik übergeben.
- _apply_library_filters setzt einen strikten Architectural Guard: Nur Items, die im aktiven Branch erlaubt sind, werden zurückgegeben.

**[Component] FRONTEND: SYNC**
- Das Frontend (z.B. app_core.js/db.js) übergibt bei jeder Anfrage den aktiven Branch an das Backend.

## Entscheidungsnotiz
**Strict Enforcement:** Items, die nicht zum Branch gehören, werden auch bei Suche nicht angezeigt. (Globale Umschaltung pro Branch)

## Verifikationsplan
- **Automatisierte Tests:** get_library_filtered(active_branch='media') liefert keine Video-Items, selbst wenn sie in der DB sind.
- **Manuelle Prüfung:**
    - Suche und Kategorie-Filter in AUDIO- und MULTIMEDIA-Branch testen.
    - 'Bilder' erscheinen nur im MULTIMEDIA-Branch.

**Status:**
- Architektur ist branch-aware, zentral konfigurierbar und garantiert strikte Trennung der Sichtbarkeit pro Arbeitsmodus.
