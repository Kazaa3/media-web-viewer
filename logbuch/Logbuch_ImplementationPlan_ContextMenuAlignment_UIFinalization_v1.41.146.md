# Implementation Plan – Context Menu Alignment & UI Finalization (v1.41.146)

## Ziel
Fehlerbehebung beim Kontextmenü-Positioning und Entfernung aller temporären Notfall-Buttons, um die GUI wieder auf das professionelle v1.41-Niveau zu bringen.

---

## 1. CONTEXT MENU HANDLER (Deduplication)
- **[MODIFY] common_helpers.js**
  - Coordinate Logic: Nutze `e.clientX` und `e.clientY` (viewport-relativ) statt `pageX/pageY` für die Kontextmenü-Positionierung (passend zu `position: fixed`).
  - Robust ID Selection: Prüfe auf beide IDs (`context-menu` und `custom-context-menu`), um Legacy-Fragmente zu unterstützen.
- **[DELETE] browse.js**
  - Remove Duplicate Handler: Lösche die doppelten `showContextMenu`- und `hideContextMenu`-Funktionen, um Logik-Überschreibungen und fehlerhafte IDs zu vermeiden.

## 2. UI DE-CLUTTER (Header)
- **[MODIFY] app.html**
  - Remove Emergency Buttons: Entferne die [RECOVER]- und [FLASH]-Buttons aus der `primary-cluster`.
  - Remove Recovery Script: Lösche den nuclear-recovery-logic `<script>`-Block.
  - Restore Polish: Entferne alle pulsierten Animationen und Notfall-Style-Overrides, um das Premium-Layout wiederherzustellen.

---

## 3. Forensic Console
- Die Forensic Console bleibt für Debugging-Zwecke erhalten, kann aber standardmäßig ausgeblendet werden.

---

## Verification Plan
- **Manual Verification:**
  - Right-Click Check: Rechtsklick auf ein Medienobjekt in der Library → Menü erscheint exakt am Mauszeiger.
  - Layout Check: Header ist frei von roten/grünen Buttons und Notfall-Styles.

---

**Review erforderlich vor Umsetzung!**
