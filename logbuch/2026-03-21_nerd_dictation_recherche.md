# Logbuch: Recherche & Bewertung – nerd-dictation (Vosk Speech-to-Text)

## Projektüberblick
[nerd-dictation](https://github.com/ideasman42/nerd-dictation) ist ein Open-Source-Tool für Offline-Spracherkennung unter Linux. Es nutzt Vosk (Python-Bibliothek) und ermöglicht Diktat sowie Sprachsteuerung ohne Cloud-Anbindung. Zielgruppe sind Entwickler und Power-User mit Fokus auf Datenschutz und lokale Verarbeitung.

---

## Technische Eckdaten
- **Sprache:** Python
- **Backend:** Vosk (Offline Speech Recognition)
- **Features:**
  - Diktat in beliebige Anwendungen (X11, Wayland)
  - Hotkey-Start/Stopp
  - Anpassbare Sprachmodelle (mehrsprachig)
  - Keine Internetverbindung nötig
  - Skriptbare Steuerung (Shell, Python)
- **Installation:**
  - Abhängigkeiten: Python 3, vosk, pyaudio, xdotool, sox, optional: notify-send
  - Setup: `pip install vosk` und weitere Pakete laut README

---

## Bewertung für Integration
- **Vorteile:**
  - Datenschutzfreundlich (keine Cloud)
  - Einfache CLI-Integration
  - Erweiterbar durch eigene Skripte
- **Nachteile:**
  - Erfordert lokale Sprachmodelle (mehr Speicherbedarf)
  - Qualität und Geschwindigkeit abhängig von Modell und Hardware

---

## Mögliche Anwendungsfälle im Projekt
- Sprachsteuerung für die Media Web Viewer UI
- Diktat-Funktion für Metadaten-Eingabe
- Automatisierte Steuerung (z.B. Play/Pause, Suche) per Sprache

---

## Ergänzung: Vosk Speech Recognition API

- [Vosk-API (https://github.com/alphacep/vosk-api)] ist die zugrundeliegende Open-Source-Spracherkennungsbibliothek für nerd-dictation.
- **Features:**
  - Offline-Spracherkennung für viele Sprachen (u.a. Deutsch, Englisch, Französisch)
  - Plattformübergreifend: Linux, Windows, macOS, Raspberry Pi, Android
  - Geringe Systemanforderungen, läuft auch auf schwacher Hardware
  - Unterstützt Echtzeit- und Datei-Transkription
  - Python-API: `pip install vosk`
- **Typische Anwendungsfälle:**
  - Sprachsteuerung
  - Diktat/Text-Transkription
  - Voice-UI für Desktop- und Mobile-Apps
- **Integration:**
  - nerd-dictation nutzt Vosk als Backend für die Spracherkennung.
  - Für eigene Projekte kann Vosk direkt per Python-API oder über nerd-dictation als Wrapper genutzt werden.

---

## Nächste Schritte (optional)
- Testinstallation und Funktionsprüfung auf Zielsystem
- Evaluierung der API/CLI-Anbindung für Integration in die bestehende App
- UI-Konzept für Sprachsteuerung/Feedback

---

*Logbuch-Eintrag erstellt: 21. März 2026*