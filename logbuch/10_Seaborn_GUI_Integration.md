# Seaborn-Grafiken in der Eel-GUI (Vanilla JS)
# Backend

## Ziel
Seaborn-Grafiken, die in Python erzeugt werden, sollen dynamisch in der Eel-basierten GUI (Vanilla JS) angezeigt werden.

## Workflow
1. **Plot-Erzeugung (Backend/Python):**
   - Seaborn-Grafik wird als PNG/SVG im Web-Ordner gespeichert.
   - Eel-API liefert den Pfad zum Bild.

2. **Bildanzeige (Frontend/JS):**
   - Vanilla JS lädt das Bild per `<img>`-Tag.
   - Dynamisches Nachladen über Eel-API.

## Beispiel Backend (Python)
```python
import eel
import seaborn as sns
import matplotlib.pyplot as plt

@eel.expose
def generate_seaborn_plot():
    sns.barplot(x=['A', 'B', 'C'], y=[1, 2, 3])
    plt.savefig('web/images/seaborn_plot.png')
    plt.close()
    return '/images/seaborn_plot.png'
```

## Beispiel Frontend (JS)
```javascript
eel.generate_seaborn_plot()().then(function(imgPath) {
    document.getElementById('plot').src = imgPath;
});
```

## Beispiel HTML
```html
<img id="plot" src="" alt="Seaborn Plot">
```

## Hinweise
- Der Web-Ordner muss für das Frontend zugänglich sein.
- Die Eel-API kann erweitert werden (z.B. für verschiedene Plot-Typen).
- PNG/SVG können direkt im Browser angezeigt werden.

---
Letzte Aktualisierung: 11. März 2026
