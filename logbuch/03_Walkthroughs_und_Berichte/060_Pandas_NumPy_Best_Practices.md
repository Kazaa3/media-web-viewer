# Pandas DataFrames & NumPy – Best Practices

## Übersicht
Pandas und NumPy sind zentrale Bibliotheken für Datenanalyse und numerische Berechnungen in Python. Sie eignen sich für tabellarische Daten, Statistik, Transformationen und schnelle Berechnungen – auch in Media Web Viewer für Metadaten, Statistiken und Filter.

## Installation
```bash
pip install pandas numpy
```

## Pandas DataFrames
- Tabellarische Datenstruktur (ähnlich Excel/SQL-Tabelle)
- Ideal für Filter, Gruppierung, Aggregation, Statistik
- CSV, JSON, SQL, Excel, Parquet etc. importierbar

### Beispiel
```python
import pandas as pd

data = pd.DataFrame({
    'filename': ['song1.mp3', 'song2.mp3'],
    'duration': [180, 240],
    'tags': [['rock'], ['pop']]
})

# Filter
rock_songs = data[data['tags'].apply(lambda tags: 'rock' in tags)]

# Statistik
mean_duration = data['duration'].mean()
```

## NumPy
- Schnelle, effiziente Arrays und Matrizen
- Ideal für numerische Berechnungen, Statistik, Signalverarbeitung

### Beispiel
```python
import numpy as np

durations = np.array([180, 240, 210])
mean = np.mean(durations)
std = np.std(durations)
```

## Integration in Media Web Viewer
- Metadaten-Analyse: DataFrames für Filter, Sortierung, Statistik
- NumPy für schnelle Berechnungen (z.B. Histogramme, Audioanalyse)
- Kombinierbar mit SQLite: Daten aus DB als DataFrame laden

## Best Practices
- DataFrames für tabellarische Medien- und Metadaten
- NumPy für numerische Features (z.B. Audio, Bild, Video)
- Fehler robust abfangen (z.B. bei Import/Parsing)
- Für große Daten: chunkweise Verarbeitung, effiziente Datentypen
- Tests mit pytest und pandas/numpy

---
*Letzte Aktualisierung: 10. März 2026*
