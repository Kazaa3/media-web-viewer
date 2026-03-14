# Plotly.js: Interaktive Visualisierungen im Browser

## Ziel
Plotly.js ermöglicht komplexe, interaktive Grafiken direkt im Browser. Es eignet sich für Dashboards, wissenschaftliche Visualisierungen und datengetriebene Anwendungen.

## Features
- Interaktive Plots: Zoom, Filter, Export als PNG/SVG
- Unterstützung für viele Diagrammtypen: Boxplot, Heatmap, Scatter, 3D, Zeitreihen
- Responsive Darstellung auf allen Geräten
- Einfache Einbindung per CDN oder npm
- Integration mit Python (Dash, Plotly-Python)

## Beispiel: Boxplot mit Plotly.js
```html
<div id="js-boxplot"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('js-boxplot', [{
    y: [1, 3, 2, 5, 4],
    type: 'box'
}]);
</script>
```

## Datenintegration
- Daten können per REST-API, WebSocket oder Eel-API vom Backend geladen werden.
- Plotly.js verarbeitet JSON-Daten direkt im Browser.

## Erweiterungen
- Dashboards mit mehreren Plots und interaktiven Komponenten
- Live-Daten und dynamische Updates
- Export als PNG/SVG für Berichte

## Hinweise
- Plotly.js ist Open Source und frei nutzbar.
- Für Python-Integration: Dash oder plotly-Python verwenden.

---

# Parser-Pipeline härten: Fehlerrobustheit und Performance

## Ziel
Die Parser-Pipeline wird so gestaltet, dass sie robust gegenüber Fehlern und Ausreißern ist. Typische Fehler werden früh abgefangen, die Pipeline kann bei kritischen Problemen kurzschließen und die Performance bleibt messbar.

## Maßnahmen
- **Early Exit:** Nicht verarbeitbare Dateien werden sofort übersprungen.
- **Fehler-Shortcircuit:** Typische Parser-Fehler werden abgefangen und führen nicht zum Abbruch der gesamten Pipeline.
- **Logging:** Fehler und Ausreißer werden protokolliert und für spätere Analyse gespeichert.
- **Performance-Messung:** Zeit pro Parser und Datei wird erfasst (z.B. mit time.time()).
- **Test-Suite:** Spezialfälle und Fehler werden gezielt getestet.

## Beispiel: Fehlerbehandlung im Python-Code
```python
def extract_metadata(path, file_type, tags, filename, mode):
    try:
        # Parser-Kette
        for parser in parser_list:
            result = parser.parse(path, file_type, tags, filename, mode)
            if result is not None:
                return result
    except (IOError, ValueError) as e:
        logger.error(f"Parser-Fehler: {e}")
        return None
```

## Hinweise
- Fehlerrobustheit ist Voraussetzung für Batch- und Parallelverarbeitung.
- Alle Fehler werden zentral geloggt und können im Dashboard visualisiert werden.
- Erweiterbar für weitere Fehlerklassen und Performance-Tests.

---

Letzte Aktualisierung: 11. März 2026
