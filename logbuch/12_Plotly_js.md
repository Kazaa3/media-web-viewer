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