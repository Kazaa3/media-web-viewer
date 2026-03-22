# JSON-Serialisierung und Umwandlung im Projekt

## Von dict zu JSON (Serialisierung)
- Mit `json.dumps()` wird ein dict, dict of dicts oder list of dicts in einen JSON-String umgewandelt.
- Beispiel:
  ```python
  import json
  d = {"name": "Song1", "tags": {"genre": "Rock"}}
  json_str = json.dumps(d)  # Ergebnis: '{"name": "Song1", "tags": {"genre": "Rock"}}'
  ```
- Für Listen:
  ```python
  l = [{"name": "A"}, {"name": "B"}]
  json_str = json.dumps(l)  # Ergebnis: '[{"name": "A"}, {"name": "B"}]'
  ```
- Für dict of dicts:
  ```python
  d2 = {"a": {"x": 1}, "b": {"y": 2}}
  json_str = json.dumps(d2)
  ```

## Von JSON zu dict (Deserialisierung)
- Mit `json.loads()` wird ein JSON-String zurück in ein dict, dict of dicts oder list of dicts gewandelt.
- Beispiel:
  ```python
  import json
  s = '{"name": "Song1", "tags": {"genre": "Rock"}}'
  d = json.loads(s)  # Ergebnis: dict
  ```

## list of dicts und JSON
- Eine list of dicts (z.B. mehrere Media Items) kann direkt mit `json.dumps()` in einen JSON-String umgewandelt werden.
- Beispiel:
  ```python
  import json
  media_list = [
      {"name": "Song1", "tags": {"genre": "Rock"}},
      {"name": "Song2", "tags": {"genre": "Pop"}}
  ]
  json_str = json.dumps(media_list)
  # Ergebnis: '[{"name": "Song1", "tags": {"genre": "Rock"}}, {"name": "Song2", "tags": {"genre": "Pop"}}]'
  # Rückumwandlung:
  media_list2 = json.loads(json_str)
  # media_list2 ist wieder eine list of dicts
  ```
- Dieses Format wird für API-Responses, Exporte und die Übergabe an die UI verwendet.

## Anpassen der Anführungszeichen
- JSON verlangt **doppelte Anführungszeichen** (`"`) für Schlüssel und Werte.
- Python-dicts können mit einfachen (`'`) oder doppelten (`"`) Anführungszeichen geschrieben werden, aber beim Serialisieren zu JSON werden automatisch doppelte verwendet.
- Beispiel:
  ```python
  d = {'a': 1, 'b': 2}
  json_str = json.dumps(d)  # Ergebnis: '{"a": 1, "b": 2}'
  ```
- Beim Einlesen mit `json.loads()` werden die Anführungszeichen automatisch korrekt interpretiert.

## Hinweise
- Für die Speicherung in der DB oder den Austausch mit der UI/Frontend immer `json.dumps()` verwenden.
- Für das Einlesen von JSON aus Dateien oder API-Antworten immer `json.loads()` verwenden.
- Fehlerquelle: Einzelne Anführungszeichen (`'`) sind in echtem JSON nicht erlaubt!

---

**Siehe auch:**
- Logbuch: JSONs Beschreibung
- Python-Doc: https://docs.python.org/3/library/json.html
