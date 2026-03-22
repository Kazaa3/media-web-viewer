# Logbuch: SVG-Icons (Up/Down) aus Google Fonts einbinden

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert, wie die Up/Down-SVG-Icons aus dem Google Fonts-Ordner im Projekt eingebunden und genutzt werden können.

---

## Icons im Projekt
- Im Ordner `web/icons/Google Fonts Material Icons/` befindet sich das Icon `swap_vert_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg`.
- Dieses Icon zeigt zwei Pfeile (hoch/runter) und eignet sich als Up/Down-Icon.

---

## Einbindung im HTML
- Beispiel für die Nutzung als Up/Down-Icon:

```html
<img src="icons/Google Fonts Material Icons/swap_vert_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg" alt="Up/Down" style="width:24px;height:24px;vertical-align:middle;">
```

- Für reine Up- oder Down-Icons kann das Icon per CSS rotiert werden:

```html
<!-- Up-Arrow -->
<img src="icons/Google Fonts Material Icons/swap_vert_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg" style="transform: rotate(180deg);" alt="Up">

<!-- Down-Arrow -->
<img src="icons/Google Fonts Material Icons/swap_vert_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg" alt="Down">
```

---

## Hinweise
- Die Icons können flexibel im UI verwendet werden.
- Größe und Farbe lassen sich per CSS anpassen.
- Für weitere Icons siehe den Google Fonts-Ordner im Projekt.
