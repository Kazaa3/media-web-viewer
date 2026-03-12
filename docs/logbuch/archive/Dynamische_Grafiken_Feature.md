# Dynamische Grafiken: Python-Backend mit JS-Oberfläche in Chrome

## Ziel
Dynamisch generierte Grafiken (z.B. Seaborn, Matplotlib) aus dem Python-Backend werden in der Chrome-Oberfläche (Vanilla JS) angezeigt.

## Workflow
1. **Backend (Python):**
   - Grafik wird mit Seaborn/Matplotlib erzeugt und als PNG/SVG gespeichert.
   - Eel-API generiert die Grafik bei Bedarf und liefert den Pfad.

2. **Frontend (JS/Chrome):**
   - JS ruft die Eel-API auf und lädt das Bild dynamisch.
   - `<img>`-Tag zeigt die Grafik im Browser an.
   - Optional: Automatische Aktualisierung bei neuen Daten.

## Beispiel Backend (Python)
```python
import eel
import seaborn as sns
import matplotlib.pyplot as plt

@eel.expose
def generate_dynamic_plot():
    # Daten dynamisch generieren
    sns.lineplot(x=[1,2,3,4], y=[4,3,2,1])
    plt.savefig('web/images/dynamic_plot.png')
    plt.close()
    return '/images/dynamic_plot.png'
```

## Beispiel Frontend (JS)
```javascript
eel.generate_dynamic_plot()().then(function(imgPath) {
    document.getElementById('dynamic-plot').src = imgPath;
});
```

## Beispiel HTML
```html
<img id="dynamic-plot" src="" alt="Dynamische Grafik">
```

## Hinweise
- Grafiken werden bei jedem Aufruf neu generiert (z.B. für Live-Daten).
- Erweiterbar für interaktive Visualisierungen und mehrere Plot-Typen.
- PNG/SVG können direkt im Chrome-Browser angezeigt werden.

---
Letzte Aktualisierung: 11. März 2026
