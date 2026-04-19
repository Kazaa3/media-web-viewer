# Implementation Plan – Nuclear GUI Restoration (v1.41.142)

## Ziel
Sofortige, abhängigkeitsfreie Sichtbarkeitswiederherstellung der GUI durch ein „Nuclear Recovery Overlay“, das vor allen anderen Skripten ausgeführt wird und gegen CSS/JS-Fehler immun ist.

---

## 1. NUCLEAR RECOVERY OVERLAY
- **[MODIFY] app.html**
  - Immediate Script: Füge ein `<script>`-Tag direkt am Anfang des `<body>` (z.B. Zeile 94) ein, das:
    - `window.NUCLEAR_UNLOCK()` definiert, welches `document.body.className = ''; document.body.style.opacity = '1';` ausführt.
    - Einen globalen Error-Sniffer einbaut, der JS-Fehler am unteren Bildschirmrand anzeigt.
  - Floating Nuclear Toggle: Platziere einen auffälligen, `position: fixed`-Button (z.B. neon-grün, Label: [RECOVER]) ganz oben links, der immer sichtbar bleibt – unabhängig von Header- oder Cluster-Status.
  - Emergency CSS: Füge einen `<style>`-Block ein, der `.nav-cluster.secondary-cluster { display: flex !important; opacity: 1 !important; transform: none !important; width: auto !important; height: auto !important; }` erzwingt.

## 2. FRAGMENT REVEAL FAIL-SAFE
- **[MODIFY] fragment_loader.js**
  - Brute Reveal: Wenn ein `.loading-fragment`-Container länger als 4 Sekunden im DOM bleibt, setze `display: none` und zeige den darunterliegenden Container an.

## 3. Mock Status Fallback (optional)
- Im Nuclear-Skript kann ein „Mock Status“-Panel angezeigt werden, falls das STATUS-Fragment nicht geladen werden kann.

---

## Verification Plan
- **Manual Verification:**
  - Visual Check: Nach dem Refresh erscheint ein neon-grüner [RECOVER]-Button ganz oben links.
  - Action Check: Klick auf [RECOVER] löscht alle Body-Klassen und setzt Opazität auf 1 – die Shell wird sichtbar.
  - Fehleranzeige: JS-Fehler werden am unteren Bildschirmrand eingeblendet.

---

**Review erforderlich vor Umsetzung!**
