# Pandas/Numpy/Matplotlib/Seaborn: Performance-Visualisierung für ParserPipeline
# Feature

## Ziel
Die Performance-Messung der ParserPipeline wird mit Pandas, Numpy, Matplotlib und Seaborn visualisiert. Ziel ist es, die Laufzeiten, Fehlerhäufigkeit und statistische Kennzahlen für jeden Parser übersichtlich darzustellen.

## Workflow
1. **Daten sammeln:**
   - Ergebnisse (Laufzeiten, Fehler, Dateityp) werden als Pandas DataFrame gespeichert.
2. **Statistik berechnen:**
   - Numpy für Mittelwert, Standardabweichung, Quantile.
3. **Visualisierung:**
   - Matplotlib für Basisplots (Balken, Linien, Scatter).
   - Seaborn für fortgeschrittene statistische Visualisierungen (Boxplot, Heatmap, Violin).

## Beispielcode
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Beispiel-Daten
parser_results = pd.DataFrame({
    'parser': ['ffprobe', 'mutagen', 'mediainfo'],
    'time_ms': [120, 95, 150],
    'errors': [0, 2, 1]
})

# Statistik mit Numpy
mean_time = np.mean(parser_results['time_ms'])
std_time = np.std(parser_results['time_ms'])

# Seaborn-Barplot
plt.figure(figsize=(8, 4))
sns.barplot(x='parser', y='time_ms', data=parser_results)
plt.title('Parser Performance (ms)')
plt.ylabel('Zeit (ms)')
plt.xlabel('Parser')
plt.tight_layout()
plt.savefig('parser_performance.png')
plt.show()
```

## Ergebnis
- Die Visualisierung zeigt die Performance der einzelnen Parser.
- Fehler und Ausreißer werden statistisch erfasst und grafisch dargestellt.
- Erweiterbar für Heatmaps, Boxplots, Violinplots (Seaborn).

## Hinweise
- Für große Datenmengen: DataFrame mit allen Testläufen.
- Erweiterung: Fehlerquoten, Dateitypen, parallele Ausführung, Zeitverläufe.
- Alle Visualisierungen können als PNG/SVG exportiert werden.

---

Letzte Aktualisierung: 11. März 2026
