# Todo
## Funktionen
# File-Handling
# - Medien scannen (Ordner durchsuchen, Metadaten extrahieren)
# - Weitere Funktionen hinzufügen, z.B. zum Abspielen von Medien, Verwalten von Wiedergabelisten, etc.
##### GUI
# - Hauptfenster mit Navigation (Medienbibliothek, Wiedergabelisten, Einstellungen)
# - Medienbibliothek (Datei-Explorer, Drag & Drop)
##### Datenbank
# Wechsel zu:  pywebview oder Flask
# SQLite über sqlite3 oder SQLAlchemy
############ Datenmodel
# Datenstruktur für Medien
# class MediaItem(name, path, type, duration, tags, ...)


#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import os


class MediaItem:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        # Hier später weitere Metadaten hinzufügen (z.B. Dauer, Format, etc.)


# Testdateien
MEDIA_DIR = "./media"  # Ordner, in dem deine Dateien liegen


# Funktion, um Medien zu scannen und an die GUI zu senden
@eel.expose("scan_media")
def scan_media():
    if not os.path.exists(MEDIA_DIR):
        return {"error": "Medienordner nicht gefunden"}
    files = [
        {"name": f, "path": os.path.join(MEDIA_DIR, f)}
        for f in os.listdir(MEDIA_DIR)
        if os.path.isfile(os.path.join(MEDIA_DIR, f))
    ]
    return {"media": files}




# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    eel.init("web")            # Ordner mit HTML/CSS/JS
    eel.start("index.html")    # Starte Seite
