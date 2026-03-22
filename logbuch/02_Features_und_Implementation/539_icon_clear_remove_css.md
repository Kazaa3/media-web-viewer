# Logbuch: SVG-Icon CSS-Klassen – .icon-clear & .icon-remove

**Datum:** 2026-03-15

## Übersicht
Dieses Logbuch dokumentiert die Integration und den CSS-Code für die SVG-basierten Icons `.icon-clear` (Papierkorb/Mülleimer) und `.icon-remove` (Kreuz/Entfernen) im Media Web Viewer.

---

## SVG-Integration per CSS-Mask
Die Icons werden als CSS-Masken direkt aus SVG-Data-URIs eingebunden. Dadurch sind sie flexibel einfärbbar und skalierbar.

### Beispiel: .icon-clear (Papierkorb)
```css
.icon-clear {
    -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>');
    mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>');
}
```

### Beispiel: .icon-remove (Kreuz)
```css
.icon-remove {
    -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>');
    mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>');
}
```

---

## Vorteile
- **Keine externen SVG-Dateien nötig** (alles inline)
- **Färbbar via `background`/`color`**
- **Skalierbar und performant**

## ToDo
- [ ] Einheitliche Nutzung der CSS-Klassen `.icon-clear` und `.icon-remove` in allen UI-Buttons
- [ ] Test auf Browser-Kompatibilität (Safari, Firefox, Chrome)

---

*Letzte Änderung: 2026-03-15*
