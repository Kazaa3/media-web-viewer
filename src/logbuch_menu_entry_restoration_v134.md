# Logbuch – Menu Entry Restoration (v1.34)

## Datum
1. April 2026

## Ziel
Wiederherstellung der fehlenden Menüeinträge `Reporting` und `System Test` sowie Einführung einer globalen, dynamischen Sub-Navigation für tiefere Modulwechsel innerhalb der v1.34-Oberfläche.

## Zusammenfassung
Die fehlenden Einträge für Reporting und Testing wurden erfolgreich in die togglebare Programm-Menüleiste zurückgeführt. Zusätzlich wurde unterhalb des Headers eine globale Sub-Navigation als glassmorphische Pill-Bar ergänzt. Dadurch sind auch verschachtelte Unterbereiche wieder direkt sichtbar und erreichbar.

## Umgesetzte Änderungen

### 1. Erweiterung der Programm-Menüleiste
**[MODIFY]** `app.html`

- Das obere, per `Alt` einblendbare Menü spiegelt jetzt alle primären Sidebar-Kategorien.
- Wiederhergestellte bzw. klar sichtbare Bereiche:
  - `Editor`
  - `Core Tools`
  - `Reporting`
  - `System Test`

### 2. Dynamische globale Sub-Navigation
**[MODIFY]** `ui_nav_helpers.js`

- Neue Orchestrierung für eine kontextabhängige Sub-Navigationsleiste unterhalb des Headers.
- Die Einträge wechseln dynamisch je nach aktiver Hauptkategorie.
- Aktive Zustände werden automatisch mit dem aktuellen View synchronisiert.

Beispielhafte Sub-Module:
- **Reporting**: `Dashboard`, `DB Stats`, `Video Health`, `Parser Hub`
- **System Test**: `System Health`, `Debug DB`, `Latency Profile`
- **Media**: `Audio Player`, `Library Browser`, `Playlists`
- **Edit**: `Metadata Tags`, `Artwork Lab`, `Media Analysis`

### 3. Visuelle Verfeinerung im v1.34-Stil
**[MODIFY]** `main.css`

- Einführung einer glassmorphischen Pill-Darstellung für die Sub-Navigation.
- Deutliche Active-State-Markierung für die Orientierung beim Modulwechsel.
- Konsistente Einbindung in die bestehende Premium-Header-/Shell-Optik.

## Verifikation

### Manuell geprüft
- `Alt` blendet die obere Programm-Menüleiste zuverlässig ein und aus.
- `Reporting` und `System Test` sind dort wieder sichtbar und anwählbar.
- Nach Auswahl erscheinen die passenden Sub-Navigations-Pills im oberen Zentralbereich.
- Die Navigation zwischen Sub-Modulen aktualisiert die aktive Hervorhebung korrekt.
- Auch `Editor` und `Tools` befüllen die neue Sub-Navigation konsistent.

## Ergebnis
Die vormals „vergrabenen“ Unterbereiche sind jetzt als hochwertige, direkte Navigationsebene sichtbar. Damit sind sowohl klassische Menübedienung als auch schnelle Kontextwechsel über eine moderne, zentrale Sub-Navigation wieder vollständig verfügbar.

## Betroffene Dateien
- `app.html`
- `ui_nav_helpers.js`
- `main.css`

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4