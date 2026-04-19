# Logbuch: Technical Overlay Expansion & Versioning (v1.46.002)

## Ziel
Die Proof-Tags (DECK-LIFT, QUEUE-LIFT) werden konfigurierbar gemacht und das System auf Version v1.46.002 angehoben.

---

## Maßnahmen

### 1. Core Config (config_master.py)
- **Versionierung:**
  - `APP_VERSION_CORE` und verwandte Variablen auf v1.46.002 erhöht.
- **technical_overlay erweitert:**
  - `deck_tag_visible` (bool): Sichtbarkeit des DECK-LIFT-Tags.
  - `deck_tag_position` (dict: top, left): Positionierung des DECK-LIFT-Tags.
  - `queue_tag_visible` (bool): Sichtbarkeit des QUEUE-LIFT-Tags.
  - `queue_tag_position` (dict: top, right): Positionierung des QUEUE-LIFT-Tags.

### 2. Web Logistics (nuclear_recovery_pulse.js)
- **injectForensicAnchor():**
  - Respektiert die neuen Flags `deck_tag_visible` und `queue_tag_visible`.
  - Setzt die Positionen gemäß `deck_tag_position` und `queue_tag_position` beim Erstellen der Tags.
  - Rückwärtskompatibilität: Der globale `forensic_anchors_visible`-Master-Switch bleibt erhalten.

---

## Verifikation
- **Visibility Test:**
  - Umschalten von `deck_tag_visible` und `queue_tag_visible` in `config_master.py` → Tags erscheinen/verschwinden wie gewünscht.
- **Position Test:**
  - Änderung der `top/left/right`-Werte in der Config → Tags bewegen sich entsprechend im UI.
- **Version Check:**
  - UI zeigt die neue Version v1.46.002 korrekt an.

---

*Status: Overlay-Expansion und Versionierung erfolgreich umgesetzt, Proof-Tags sind jetzt granular steuerbar.*
