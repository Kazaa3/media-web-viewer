# JavaScript-Grafik-Frameworks für die GUI

## Ziel
Visualisierungen und dynamische Grafiken direkt im Browser mit JavaScript, unabhängig vom Python-Backend.

## Workflow
1. **Datenbereitstellung:**
   - Daten werden vom Backend (z.B. Python/Eel, REST-API) an das JS-Frontend übergeben.
2. **Visualisierung (JS):**
   - Grafiken werden mit JavaScript-Frameworks wie Chart.js, Plotly.js oder D3.js erzeugt.
   - Interaktive und dynamische Darstellung direkt im Browser.

## Beispiel: Chart.js (Balkendiagramm)
```html
<canvas id="js-bar-chart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('js-bar-chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
            label: 'Werte',
            data: [12, 19, 7],
            backgroundColor: ['#4e79a7', '#f28e2b', '#e15759']
        }]
    }
});
</script>
```

## Beispiel: Plotly.js (Boxplot)
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

## Beispiel: D3.js (Individuelle Visualisierung)
```html
<div id="js-d3-visualization"></div>
<script src="https://d3js.org/d3.v6.min.js"></script>
<script>
// Code für individuelle Visualisierung
</script>
```

## Hinweise
- Daten können per Eel-API, WebSocket oder REST-API vom Backend geladen werden.
- JS-Grafikframeworks bieten interaktive und responsive Visualisierungen.
- Erweiterbar für Heatmaps, Scatterplots, Zeitreihen, etc.

## Python-Module zum Ausliefern von JS-Grafiken

- **Eel:** Ermöglicht das Ausliefern von HTML/JS-GUIs und das einfache Verbinden von Python-Backend und JS-Frontend. Ideal für Desktop-Apps mit dynamischen JS-Grafiken.
- **Flask/FastAPI:** Webframeworks, mit denen HTML/JS-Seiten (inkl. Chart.js, Plotly.js, D3.js) als Webserver ausgeliefert werden können. REST-API für Daten, JS-Frontend für Visualisierung.
- **Dash (Plotly):** Speziell für interaktive Dashboards, kombiniert Python-Backend mit Plotly.js im Browser. Sehr einfach für komplexe Visualisierungen.
- **Streamlit:** Für schnelle, interaktive Web-Apps, kann auch JS-Grafiken einbinden (z.B. über Komponenten).

Typischer Workflow:
- Python-Backend bereitet Daten auf und stellt sie per API bereit.
- JS-Frontend (Chart.js, Plotly.js, D3.js) visualisiert die Daten im Browser.
- Eel, Flask, FastAPI, Dash oder Streamlit liefern die HTML/JS-Seiten aus.

### Dash (Plotly)
Dash ist ein Python-Framework für interaktive Web-Dashboards. Es nutzt Plotly.js für die Visualisierung im Browser und ermöglicht komplexe, dynamische Grafiken mit minimalem Python-Code.

- **Vorteile:**
  - Einfache Erstellung von Dashboards mit Python.
  - Plotly-Grafiken direkt im Browser, interaktiv und responsiv.
  - Komponenten für Filter, Tabellen, Live-Updates.
  - Keine separate JS-Programmierung nötig, aber Erweiterung mit JS möglich.

#### Beispiel: Dash-App mit Plotly-Grafik
```python
import dash
from dash import html, dcc
import plotly.express as px

app = dash.Dash(__name__)
fig = px.box([1, 3, 2, 5, 4], y=[1, 3, 2, 5, 4])

app.layout = html.Div([
    html.H1('Boxplot mit Dash'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Übersicht: Standard-Konfiguration für JS-Grafik-Frameworks

| Framework   | Einbindung         | Standard-Element | Interaktivität | Backend-Kompatibilität | Exportmöglichkeiten |
|-------------|--------------------|------------------|----------------|-----------------------|--------------------|
| Chart.js    | CDN, npm           | <canvas>         | Hoch           | REST, Eel, Flask      | PNG                |
| Plotly.js   | CDN, npm           | <div>            | Sehr hoch      | REST, Dash, Flask     | PNG, SVG           |
| D3.js       | CDN, npm           | <div>, <svg>     | Maximal        | REST, Flask           | SVG                |
| Dash        | Python-Package     | <div> (Browser)  | Sehr hoch      | Python (Plotly)       | PNG, SVG           |
| Eel         | Python-Package     | <html/JS>        | Hoch           | Python (Desktop)      | PNG                |
| Flask/FastAPI | Python-Package   | <html/JS>        | Hoch           | Python (Webserver)    | PNG, SVG           |
| Streamlit   | Python-Package     | <div> (Browser)  | Hoch           | Python (Web-App)      | PNG                |

**Hinweise:**
- Alle Frameworks können per CDN oder npm eingebunden werden (außer Dash, Streamlit, Eel: Python-Package).
- Interaktivität und Exportmöglichkeiten variieren je nach Framework.
- Backend-Kompatibilität: REST-API, Python-Webserver oder Desktop-App.
- Standard-Element: Canvas, Div oder SVG je nach Framework.

---
Letzte Aktualisierung: 11. März 2026

- **Chart.js:** Einfaches, flexibles Framework für Balken-, Linien-, Kreisdiagramme. Ideal für schnelle, interaktive Visualisierungen.
- **Plotly.js:** Leistungsstark für komplexe, interaktive Plots (Boxplot, Heatmap, Scatter, 3D). Sehr gute Integration für Dashboards.
- **D3.js:** Extrem flexibel, geeignet für individuelle, datengetriebene Visualisierungen und Animationen. Erfordert mehr Code, bietet maximale Kontrolle.
