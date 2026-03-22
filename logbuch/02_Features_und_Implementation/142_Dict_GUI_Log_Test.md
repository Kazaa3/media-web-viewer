# Dict direkt aus Python in GUI & Log schicken – Test

## Ziel
Sende ein Python-Dict direkt an die GUI (Frontend) und ins Log – ideal für Debugging, Tests und dynamische Anzeige.

## Beispiel (main.py)
```python
import eel
import logging

def send_dict_to_gui_and_log(data: dict):
    logging.info(f"Dict für GUI: {data}")
    eel.show_dict_in_gui(data)  # Eel-expose im JS

@eel.expose
def test_send_dict():
    test_dict = {
        'status': 'ok',
        'message': 'Test-Dict aus Python',
        'timestamp': time.time()
    }
    send_dict_to_gui_and_log(test_dict)
    return test_dict
```

## JS-Frontend (Eel-expose)
```javascript
window.show_dict_in_gui = function(data) {
    console.log('Dict aus Python:', data);
    // Render im Debug/Log-Tab
    document.getElementById('debug').innerText = JSON.stringify(data, null, 2);
}
```

## Test
- Python: `eel.test_send_dict()` aufrufen
- JS: Dict wird im Debug-Tab angezeigt und im Log ausgegeben

## Vorteile
- Direkte Dict-Kommunikation, kein JSON-Parsing nötig
- Logging für Nachvollziehbarkeit
- Ideal für Tests, Debugging, dynamische UI

---
*Letzte Aktualisierung: 10. März 2026*
