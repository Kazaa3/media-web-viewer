# Parser-Pipeline Test: Einzel- und Paralleltests, Performance & Visualisierung

## Ziel
Systematische Test-Suite für die Parser-Pipeline:
- Jeder Parser wird einzeln getestet
- Paralleltests (mit Dateizugriffs-Schutz)
- Timeout, Dateityp, Parser-Settings werden berücksichtigt
- Performance-Messung (Zeit pro Parser)
- Visualisierung der Ergebnisse (z.B. mit Pandas/Numpy/Matplotlib)

## Vorgehen
1. **Einzeltests:**
   - Jede Datei wird mit jedem Parser getestet
   - Dateityp und Parser-Settings werden protokolliert
2. **Paralleltests:**
   - Parser laufen parallel (ThreadPool/ProcessPool)
   - Dateizugriff wird synchronisiert (Lock/Queue)
   - Timeout pro Parser
3. **Performance:**
   - Zeitmessung pro Parser und Datei
   - Ergebnisse als Tabelle (Pandas DataFrame)
4. **Visualisierung:**
   - Grafiken: Balkendiagramm, Heatmap, Boxplot
   - Darstellung an einem Ort (z.B. logbuch/ParserPipeline_Performance.md)
   - Integration mit Data Science Tools (Pandas, Numpy, Matplotlib)

## Beispiel (Python/Pandas)
```python
import pandas as pd
import concurrent.futures
import time

def run_parser(parser_func, path, file_type, settings):
    t0 = time.time()
    try:
        result = parser_func(path, file_type, settings)
        duration = time.time() - t0
        return {"result": result, "duration": duration}
    except Exception as e:
        return {"error": str(e), "duration": time.time() - t0}

# ... Paralleltests mit ThreadPoolExecutor ...
```

## Performance-Messung
- Zeit pro Parser und Datei wird gemessen (z.B. mit time.time())
- Ergebnisse werden als Tabelle (Pandas DataFrame) gespeichert
- Vergleich von Einzel- und Paralleltests

## Visualisierung der Ergebnisse
- Grafiken: Balkendiagramm, Heatmap, Boxplot
- Darstellung der Laufzeiten und Fehler
- Integration mit Pandas/Numpy/Matplotlib
- Ergebnisse und Grafiken werden zentral im logbuch abgelegt

---

# Pandas/Numpy/Matplotlib/Seaborn: Performance-Visualisierung für ParserPipeline

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
