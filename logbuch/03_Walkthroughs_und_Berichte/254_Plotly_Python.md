# Plotly für Python: Interaktive Visualisierungen

## Ziel
Plotly für Python ermöglicht die Erstellung interaktiver, wissenschaftlicher und business-orientierter Grafiken direkt aus Python-Code. Ideal für Dashboards, Berichte und Datenanalyse.

## Features
- Unterstützung für viele Diagrammtypen: Boxplot, Heatmap, Scatter, 3D, Zeitreihen
- Interaktive Grafiken: Zoom, Filter, Export als PNG/SVG
- Integration mit Dash für Web-Dashboards
- Einfache API für schnelle Visualisierungen

## Beispiel: Boxplot mit Plotly-Python
```python
import plotly.express as px
fig = px.box(y=[1, 3, 2, 5, 4])
fig.show()
```

## Dash-Integration
- Dash nutzt Plotly-Grafiken für interaktive Web-Dashboards.
- Komponenten für Filter, Tabellen, Live-Updates.

### Dash: Python-Web-Dashboards mit Plotly
Dash ist ein Framework zur Erstellung interaktiver Web-Dashboards mit Python. Es nutzt Plotly für die Visualisierung und bietet Komponenten für Filter, Tabellen und Live-Updates.

- **Vorteile:**
  - Keine separate JS-Programmierung nötig
  - Interaktive Plotly-Grafiken direkt im Browser
  - Einfache Layouts mit HTML-Komponenten
  - Erweiterbar mit eigenen Modulen und Callback-Logik

#### Beispiel: Dash-App mit Plotly-Boxplot
```python
import dash
from dash import html, dcc
import plotly.express as px

app = dash.Dash(__name__)
fig = px.box(y=[1, 3, 2, 5, 4])

app.layout = html.Div([
    html.H1('Boxplot mit Dash'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Datenintegration
- Daten aus Pandas, Numpy, SQL, CSV, JSON etc. können direkt visualisiert werden.

## Export
- Grafiken können als PNG, SVG, PDF exportiert werden.
- Einbindung in Jupyter Notebooks, Web-Apps, Berichte.

## Hinweise
- Plotly für Python ist Open Source und frei nutzbar.
- Für komplexe Dashboards: Dash verwenden.

---
Letzte Aktualisierung: 11. März 2026
