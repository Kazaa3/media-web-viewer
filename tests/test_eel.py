# Kategorie: Eel / Bottle Integration
# Eingabewerte: Pfade zu Mediendateien
# Ausgabewerte: Statische Dateien über HTTP
# Testdateien: Keine (Benötigt lokales /media Verzeichnis)
# Kommentar: Prüft ob Bottle-Routen innerhalb der Eel-Umgebung korrekt registriert und aufgelöst werden.

import eel
import bottle

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    return bottle.static_file(filepath, root='./media')

print("Bottle route added")
